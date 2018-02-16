import asyncio
import jwt
import requests
from datetime import datetime, timedelta

class JwtTokenExtractor:
    metadataCache = {}

    def __init__(self, validationParams, allowedAlgorithms, metadataUrl, validator):
        self.validationParameters = validationParams
        self.validationParameters.algorithms = allowedAlgorithms
        self.openIdMetadata = JwtTokenExtractor.get_open_id_metadata(metadataUrl)
        self.validator = validator

    @staticmethod
    def get_open_id_metadata(metadataUrl):
        metadata = JwtTokenExtractor.metadataCache.get(metadataUrl, None)
        if metadata is None:
            metadata = _OpenIdMetadata(metadataUrl)
            JwtTokenExtractor.metadataCache.setdefault(metadataUrl, metadata)
        return metadata

    async def get_identity_from_auth(self, authHeader):
        if not authHeader:
            return None
        parts = authHeader.split(".")
        if len(parts) is 2:
            return await asyncio.ensure_future(self.get_identity(parts[0], parts[1]))
        return None

    async def get_identity(self, schema, parameter):
        # No header in correct scheme or no token
        if schema is not "Bearer" or not parameter:
            return None
        
        # Issuer isn't allowed? No need to check signature
        if not self._has_allowed_issuer(parameter):
            return None
        
        try:
            return await asyncio.ensure_future(self._validate_token(parameter))
        except:
            raise

    def _has_allowed_issuer(self, jwtToken):
        decoded = jwt.decode(jwtToken, verify=False)
        issuer = decoded.iss
        if issuer in self.validationParameters.issuer:
            return True
        
        return issuer is self.validationParameters.issuer

    async def _validate_token(self, jwtToken):
        decoded = jwt.decode(jwtToken, verify=False)
        headers = jwt.get_unverified_header(jwtToken)

        # Update the signing tokens from the last refresh
        keyId = headers["kid"]
        metadata = await asyncio.ensure_future(self.openIdMetadata.get(keyId))
        return

class _OpenIdMetadata:
    def __init__(self, url):
        self.url = url
        self.keys = []
        self.lastUpdated = datetime.min

    async def get(self, keyId):
        # If keys are more than 5 days old, refresh them
        if self.lastUpdated < (datetime.now() + timedelta(days=5)):
            await asyncio.ensure_future(self._refresh())
        return self._find(keyId)

    async def _refresh(self):
        response = requests.get(self.url)
        response.raise_for_status()
        keysUrl = response.json()["jwks_uri"]
        responseKeys = requests.get(keysUrl)
        responseKeys.raise_for_status()
        self.lastUpdated = datetime.now()
        self.keys = responseKeys.json()

    def _find(self, keyId):
        pass