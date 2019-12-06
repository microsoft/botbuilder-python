# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import json
from datetime import datetime, timedelta
from typing import List
import requests
from jwt.algorithms import RSAAlgorithm
import jwt
from .claims_identity import ClaimsIdentity
from .verify_options import VerifyOptions
from .endorsements_validator import EndorsementsValidator


class JwtTokenExtractor:
    metadataCache = {}

    def __init__(
        self,
        validation_params: VerifyOptions,
        metadata_url: str,
        allowed_algorithms: list,
    ):
        self.validation_parameters = validation_params
        self.validation_parameters.algorithms = allowed_algorithms
        self.open_id_metadata = JwtTokenExtractor.get_open_id_metadata(metadata_url)

    @staticmethod
    def get_open_id_metadata(metadata_url: str):
        metadata = JwtTokenExtractor.metadataCache.get(metadata_url, None)
        if metadata is None:
            metadata = _OpenIdMetadata(metadata_url)
            JwtTokenExtractor.metadataCache.setdefault(metadata_url, metadata)
        return metadata

    async def get_identity_from_auth_header(
        self, auth_header: str, channel_id: str, required_endorsements: List[str] = None
    ) -> ClaimsIdentity:
        if not auth_header:
            return None
        parts = auth_header.split(" ")
        if len(parts) == 2:
            return await self.get_identity(
                parts[0], parts[1], channel_id, required_endorsements
            )
        return None

    async def get_identity(
        self,
        schema: str,
        parameter: str,
        channel_id: str,
        required_endorsements: List[str] = None,
    ) -> ClaimsIdentity:
        # No header in correct scheme or no token
        if schema != "Bearer" or not parameter:
            return None

        # Issuer isn't allowed? No need to check signature
        if not self._has_allowed_issuer(parameter):
            return None

        try:
            return await self._validate_token(
                parameter, channel_id, required_endorsements
            )
        except Exception as error:
            raise error

    def _has_allowed_issuer(self, jwt_token: str) -> bool:
        decoded = jwt.decode(jwt_token, verify=False)
        issuer = decoded.get("iss", None)
        if issuer in self.validation_parameters.issuer:
            return True

        return issuer == self.validation_parameters.issuer

    async def _validate_token(
        self, jwt_token: str, channel_id: str, required_endorsements: List[str] = None
    ) -> ClaimsIdentity:
        required_endorsements = required_endorsements or []
        headers = jwt.get_unverified_header(jwt_token)

        # Update the signing tokens from the last refresh
        key_id = headers.get("kid", None)
        metadata = await self.open_id_metadata.get(key_id)

        if key_id and metadata.endorsements:
            # Verify that channelId is included in endorsements
            if not EndorsementsValidator.validate(channel_id, metadata.endorsements):
                raise Exception("Could not validate endorsement key")

            # Verify that additional endorsements are satisfied.
            # If no additional endorsements are expected, the requirement is satisfied as well
            for endorsement in required_endorsements:
                if not EndorsementsValidator.validate(
                    endorsement, metadata.endorsements
                ):
                    raise Exception("Could not validate endorsement key")

        if headers.get("alg", None) not in self.validation_parameters.algorithms:
            raise Exception("Token signing algorithm not in allowed list")

        options = {
            "verify_aud": False,
            "verify_exp": not self.validation_parameters.ignore_expiration,
        }

        decoded_payload = jwt.decode(
            jwt_token,
            metadata.public_key,
            leeway=self.validation_parameters.clock_tolerance,
            options=options,
        )

        claims = ClaimsIdentity(decoded_payload, True)

        return claims


class _OpenIdMetadata:
    def __init__(self, url):
        self.url = url
        self.keys = []
        self.last_updated = datetime.min

    async def get(self, key_id: str):
        # If keys are more than 5 days old, refresh them
        if self.last_updated < (datetime.now() + timedelta(days=5)):
            await self._refresh()
        return self._find(key_id)

    async def _refresh(self):
        response = requests.get(self.url)
        response.raise_for_status()
        keys_url = response.json()["jwks_uri"]
        response_keys = requests.get(keys_url)
        response_keys.raise_for_status()
        self.last_updated = datetime.now()
        self.keys = response_keys.json()["keys"]

    def _find(self, key_id: str):
        if not self.keys:
            return None
        key = [x for x in self.keys if x["kid"] == key_id][0]
        public_key = RSAAlgorithm.from_jwk(json.dumps(key))
        endorsements = key.get("endorsements", [])
        return _OpenIdConfig(public_key, endorsements)


class _OpenIdConfig:
    def __init__(self, public_key, endorsements):
        self.public_key = public_key
        self.endorsements = endorsements
