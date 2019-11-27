# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from datetime import timedelta
from typing import Dict, Union

import jwt

from .authentication_configuration import AuthenticationConfiguration
from .authentication_constants import AuthenticationConstants
from .claims_identity import ClaimsIdentity
from .credential_provider import CredentialProvider
from .government_constants import GovernmentConstants
from .verify_options import VerifyOptions
from .jwt_token_extractor import JwtTokenExtractor
from .channel_provider import ChannelProvider


class SkillValidation:
    # TODO: Remove circular dependcies after C# refactor
    # pylint: disable=import-outside-toplevel

    """
    Validates JWT tokens sent to and from a Skill.
    """

    _token_validation_parameters = VerifyOptions(
        issuer=[
            "https://sts.windows.net/d6d49420-f39b-4df7-a1dc-d59a935871db/",  # Auth v3.1, 1.0 token
            "https://login.microsoftonline.com/d6d49420-f39b-4df7-a1dc-d59a935871db/v2.0",  # Auth v3.1, 2.0 token
            "https://sts.windows.net/f8cdef31-a31e-4b4a-93e4-5f571e91255a/",  # Auth v3.2, 1.0 token
            "https://login.microsoftonline.com/f8cdef31-a31e-4b4a-93e4-5f571e91255a/v2.0",  # Auth v3.2, 2.0 token
            "https://sts.windows.net/cab8a31a-1906-4287-a0d8-4eef66b95f6e/",  # Auth for US Gov, 1.0 token
            "https://login.microsoftonline.us/cab8a31a-1906-4287-a0d8-4eef66b95f6e/v2.0",  # Auth for US Gov, 2.0 token
        ],
        audience=None,
        clock_tolerance=timedelta(minutes=5),
        ignore_expiration=False,
    )

    @staticmethod
    def is_skill_token(auth_header: str) -> bool:
        """
        Determines if a given Auth header is from from a skill to bot or bot to skill request.
        :param auth_header: Bearer Token, in the "Bearer [Long String]" Format.
        :return bool:
        """
        from .jwt_token_validation import JwtTokenValidation

        if not JwtTokenValidation.is_valid_token_format(auth_header):
            return False

        bearer_token = auth_header.split(" ")[1]

        # Parse the Big Long String into an actual token.
        token = jwt.decode(bearer_token, verify=False)
        return SkillValidation.is_skill_claim(token)

    @staticmethod
    def is_skill_claim(claims: Dict[str, object]) -> bool:
        """
        Checks if the given list of claims represents a skill.
        :param claims: A dict of claims.
        :return bool:
        """
        if AuthenticationConstants.VERSION_CLAIM not in claims:
            return False

        audience = claims.get(AuthenticationConstants.AUDIENCE_CLAIM)

        # The audience is https://api.botframework.com and not an appId.
        if (
            not audience
            or audience == AuthenticationConstants.TO_BOT_FROM_CHANNEL_TOKEN_ISSUER
        ):
            return False

        from .jwt_token_validation import JwtTokenValidation

        app_id = JwtTokenValidation.get_app_id_from_claims(claims)

        if not app_id:
            return False

        # Skill claims must contain and app ID and the AppID must be different than the audience.
        return app_id != audience

    @staticmethod
    async def authenticate_channel_token(
        auth_header: str,
        credentials: CredentialProvider,
        channel_service_or_provider: Union[str, ChannelProvider],
        channel_id: str,
        auth_configuration: AuthenticationConfiguration,
    ) -> ClaimsIdentity:
        if auth_configuration is None:
            raise Exception(
                "auth_configuration cannot be None in SkillValidation.authenticate_channel_token"
            )

        from .jwt_token_validation import JwtTokenValidation

        if isinstance(channel_service_or_provider, ChannelProvider):
            is_gov = channel_service_or_provider.is_government()
        else:
            is_gov = JwtTokenValidation.is_government(channel_service_or_provider)

        open_id_metadata_url = (
            GovernmentConstants.TO_BOT_FROM_EMULATOR_OPEN_ID_METADATA_URL
            if is_gov
            else AuthenticationConstants.TO_BOT_FROM_EMULATOR_OPEN_ID_METADATA_URL
        )

        token_extractor = JwtTokenExtractor(
            SkillValidation._token_validation_parameters,
            open_id_metadata_url,
            AuthenticationConstants.ALLOWED_SIGNING_ALGORITHMS,
        )

        identity = await token_extractor.get_identity_from_auth_header(
            auth_header, channel_id, auth_configuration.required_endorsements
        )
        await SkillValidation._validate_identity(identity, credentials)

        return identity

    @staticmethod
    async def _validate_identity(
        identity: ClaimsIdentity, credentials: CredentialProvider
    ):
        if not identity:
            # No valid identity. Not Authorized.
            raise PermissionError("Invalid Identity")

        if not identity.is_authenticated:
            # The token is in some way invalid. Not Authorized.
            raise PermissionError("Token Not Authenticated")

        version_claim = identity.claims.get(AuthenticationConstants.VERSION_CLAIM)
        if not version_claim:
            # No version claim
            raise PermissionError(
                f"'{AuthenticationConstants.VERSION_CLAIM}' claim is required on skill Tokens."
            )

        # Look for the "aud" claim, but only if issued from the Bot Framework
        audience_claim = identity.claims.get(AuthenticationConstants.AUDIENCE_CLAIM)
        if not audience_claim:
            # Claim is not present or doesn't have a value. Not Authorized.
            raise PermissionError(
                f"'{AuthenticationConstants.AUDIENCE_CLAIM}' claim is required on skill Tokens."
            )

        if not await credentials.is_valid_appid(audience_claim):
            # The AppId is not valid. Not Authorized.
            raise PermissionError("Invalid audience.")

        from .jwt_token_validation import JwtTokenValidation

        app_id = JwtTokenValidation.get_app_id_from_claims(identity.claims)
        if not app_id:
            # Invalid AppId
            raise PermissionError("Invalid app_id.")
