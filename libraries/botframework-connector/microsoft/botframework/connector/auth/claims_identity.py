class Claim:
    def __init__(self, claim_type, value):
        self.type = claim_type
        self.value = value

class ClaimsIdentity:
    def __init__(self, claims, isAuthenticated):
        self.claims = claims
        self.isAuthenticated = isAuthenticated

    def get_claim_value(self, claim_type):
        return self.claims.get(claim_type)
