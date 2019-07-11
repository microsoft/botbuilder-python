class Claim:
    def __init__(self, claim_type: str, value):
        self.type = claim_type
        self.value = value


class ClaimsIdentity:
    def __init__(self, claims: dict, is_authenticated: bool):
        self.claims = claims
        self.is_authenticated = is_authenticated

    def get_claim_value(self, claim_type: str):
        return self.claims.get(claim_type)
