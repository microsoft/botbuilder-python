# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import asyncio
from typing import Union

import jwt

from .jwt_token_extractor import JwtTokenExtractor
from .verify_options import VerifyOptions
from .authentication_constants import AuthenticationConstants
from .credential_provider import CredentialProvider
from .claims_identity import ClaimsIdentity
from .government_constants import GovernmentConstants
from .channel_provider import ChannelProvider


class EmulatorValidation:
    APP_ID_CLAIM = "appid"
    VERSION_CLAIM = "ver"

    TO_BOT_FROM_EMULATOR_TOKEN_VALIDATION_PARAMETERS = VerifyOptions(
        issuer=[
            # Auth v3.1, 1.0 token
            "https://sts.windows.net/d6d49420-f39b-4df7-a1dc-d59a935871db/",
            # Auth v3.1, 2.0 token
            "https://login.microsoftonline.com/d6d49420-f39b-4df7-a1dc-d59a935871db/v2.0",
            # Auth v3.2, 1.0 token
            "https://sts.windows.net/f8cdef31-a31e-4b4a-93e4-5f571e91255a/",
            # Auth v3.2, 2.0 token
            "https://login.microsoftonline.com/f8cdef31-a31e-4b4a-93e4-5f571e91255a/v2.0",
            # ???
            "https://sts.windows.net/72f988bf-86f1-41af-91ab-2d7cd011db47/",
            # Auth for US Gov, 1.0 token
            "https://sts.windows.net/cab8a31a-1906-4287-a0d8-4eef66b95f6e/",
            # Auth for US Gov, 2.0 token
            "https://login.microsoftonline.us/cab8a31a-1906-4287-a0d8-4eef66b95f6e/v2.0",
        ],
        audience=None,
        clock_tolerance=5 * 60,
        ignore_expiration=False,
    )

    @staticmethod
    def is_token_from_emulator(auth_header: str) -> bool:
        """ Determines if a given Auth header is from the Bot Framework Emulator

        :param auth_header: Bearer Token, in the 'Bearer [Long String]' Format.
        :type auth_header: str

        :return: True, if the token was issued by the Emulator. Otherwise, false.
        """
        from .jwt_token_validation import (  # pylint: disable=import-outside-toplevel
            JwtTokenValidation,
        )

        if not JwtTokenValidation.is_valid_token_format(auth_header):
            return False

        bearer_token = auth_header.split(" ")[1]

        # Parse the Big Long String into an actual token.
        token = jwt.decode(bearer_token, verify=False)
        if not token:
            return False

        # Is there an Issuer?
        issuer = token["iss"]
        if not issuer:
            # No Issuer, means it's not from the Emulator.
            return False

        # Is the token issues by a source we consider to be the emulator?
        issuer_list = (
            EmulatorValidation.TO_BOT_FROM_EMULATOR_TOKEN_VALIDATION_PARAMETERS.issuer
        )
        if issuer_list and not issuer in issuer_list:
            # Not a Valid Issuer. This is NOT a Bot Framework Emulator Token.
            return False

        # The Token is from the Bot Framework Emulator. Success!
        return True

    @staticmethod
    async def authenticate_emulator_token(
        auth_header: str,
        credentials: CredentialProvider,
        channel_service_or_provider: Union[str, ChannelProvider],
        channel_id: str,
    ) -> ClaimsIdentity:
        """ Validate the incoming Auth Header

        Validate the incoming Auth Header as a token sent from the Bot Framework Service.
        A token issued by the Bot Framework emulator will FAIL this check.

        :param auth_header: The raw HTTP header in the format: 'Bearer [longString]'
        :type auth_header: str
        :param credentials: The user defined set of valid credentials, such as the AppId.
        :type credentials: CredentialProvider

        :return: A valid ClaimsIdentity.
        :raises Exception:
        """
        # pylint: disable=import-outside-toplevel
        from .jwt_token_validation import JwtTokenValidation

        if isinstance(channel_service_or_provider, ChannelProvider):
            is_gov = channel_service_or_provider.is_government()
        else:
            is_gov = JwtTokenValidation.is_government(channel_service_or_provider)

        open_id_metadata = (
            GovernmentConstants.TO_BOT_FROM_EMULATOR_OPEN_ID_METADATA_URL
            if is_gov
            else AuthenticationConstants.TO_BOT_FROM_EMULATOR_OPEN_ID_METADATA_URL
        )

        token_extractor = JwtTokenExtractor(
            EmulatorValidation.TO_BOT_FROM_EMULATOR_TOKEN_VALIDATION_PARAMETERS,
            open_id_metadata,
            AuthenticationConstants.ALLOWED_SIGNING_ALGORITHMS,
        )

        identity = await token_extractor.get_identity_from_auth_header(
            auth_header, channel_id
        )
        if not identity:
            # No valid identity. Not Authorized.
            raise Exception("Unauthorized. No valid identity.")

        if not identity.is_authenticated:
            # The token is in some way invalid. Not Authorized.
            raise Exception("Unauthorized. Is not authenticated")

        # Now check that the AppID in the claimset matches
        # what we're looking for. Note that in a multi-tenant bot, this value
        # comes from developer code that may be reaching out to a service, hence the
        # Async validation.
        version_claim = identity.get_claim_value(EmulatorValidation.VERSION_CLAIM)
        if version_claim is None:
            raise Exception('Unauthorized. "ver" claim is required on Emulator Tokens.')

        app_id = ""

        # The Emulator, depending on Version, sends the AppId via either the
        # appid claim (Version 1) or the Authorized Party claim (Version 2).
        if not version_claim or version_claim == "1.0":
            # either no Version or a version of "1.0" means we should look for
            # the claim in the "appid" claim.
            app_id_claim = identity.get_claim_value(EmulatorValidation.APP_ID_CLAIM)
            if not app_id_claim:
                # No claim around AppID. Not Authorized.
                raise Exception(
                    "Unauthorized. "
                    '"appid" claim is required on Emulator Token version "1.0".'
                )

            app_id = app_id_claim
        elif version_claim == "2.0":
            # Emulator, "2.0" puts the AppId in the "azp" claim.
            app_authz_claim = identity.get_claim_value(
                AuthenticationConstants.AUTHORIZED_PARTY
            )
            if not app_authz_claim:
                # No claim around AppID. Not Authorized.
                raise Exception(
                    "Unauthorized. "
                    '"azp" claim is required on Emulator Token version "2.0".'
                )

            app_id = app_authz_claim
        else:
            # Unknown Version. Not Authorized.
            raise Exception(
                "Unauthorized. Unknown Emulator Token version ", version_claim, "."
            )

        is_valid_app_id = await asyncio.ensure_future(
            credentials.is_valid_appid(app_id)
        )
        if not is_valid_app_id:
            raise Exception("Unauthorized. Invalid AppId passed on token: ", app_id)

        return identity
