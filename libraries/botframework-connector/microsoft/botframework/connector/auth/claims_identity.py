class Claim:
    def __init__(self, cType, value):
        self.cType = cType
        self.value = value



class ClaimsIdentity:
    def __init__(self, claims, isAuthenticated):
        self.claims = claims
        self.isAuthenticated = isAuthenticated

    def get_claim_value(self, cType):
        return self.claims.get(cType)