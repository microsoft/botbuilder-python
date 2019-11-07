from typing import List


class AuthenticationConfiguration:
    def __init__(self, required_endorsements: List[str] = None):
        self.required_endorsements = required_endorsements or []
