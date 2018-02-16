import asyncio
import requests
import jwt
from jwt.algorithms import RSAAlgorithm
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
        parts = authHeader.split(" ")
        if len(parts) == 2:
            return await self.get_identity(parts[0], parts[1])
        return None

    async def get_identity(self, schema, parameter):
        # No header in correct scheme or no token
        if schema != "Bearer" or not parameter:
            return None
        
        # Issuer isn't allowed? No need to check signature
        if not self._has_allowed_issuer(parameter):
            return None
        
        try:
            return await self._validate_token(parameter)
        except:
            raise

    def _has_allowed_issuer(self, jwtToken):
        decoded = jwt.decode(jwtToken, verify=False)
        issuer = decoded.get("iss", None)
        if issuer in self.validationParameters.issuer:
            return True
        
        return issuer is self.validationParameters.issuer

    async def _validate_token(self, jwtToken):
        headers = jwt.get_unverified_header(jwtToken)

        # Update the signing tokens from the last refresh
        keyId = headers.get("kid", None)
        metadata = await self.openIdMetadata.get(keyId)

        options = {'verify_aud': False}
        decodedPayload = jwt.decode(jwtToken, metadata.publicKey, options=options)
        return

class _OpenIdMetadata:
    def __init__(self, url):
        self.url = url
        self.keys = []
        self.lastUpdated = datetime.min

    async def get(self, keyId):
        # If keys are more than 5 days old, refresh them
        if self.lastUpdated < (datetime.now() + timedelta(days=5)):
            await self._refresh()
        return self._find(keyId)

    async def _refresh(self):
        response = requests.get(self.url)
        response.raise_for_status()
        keysUrl = response.json()["jwks_uri"]
        responseKeys = requests.get(keysUrl)
        responseKeys.raise_for_status()
        self.lastUpdated = datetime.now()
        self.keys = responseKeys.json()["keys"]

    def _find(self, keyId):
        if  len(self.keys) == 0:
            return None
        key = next(x for x in self.keys if x["kid"] == keyId)
        publicKey = RSAAlgorithm.from_jwk(json.dumps(key))
        endorsements = key.get("endorsements", [])
        return _OpenIdConfig(publicKey, endorsements)
        
class _OpenIdConfig:
    def __init__(self, publicKey, endorsements):
        self.publicKey = publicKey
        self.endorsements = endorsements