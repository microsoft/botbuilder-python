# HowTo: Block all Skill Claims

Write a class that conforms to the `ValidateClaims` interface and throws an exception if the claims are skill claims:
```python
class AllowedSkillsClaimsValidator:

    config_key = "ALLOWED_CALLERS"

    def __init__(self, config: DefaultConfig):
        if not config:
            raise TypeError(
                "AllowedSkillsClaimsValidator: config object cannot be None."
            )

        # ALLOWED_CALLERS is the setting in config.py file
        # that consists of the list of parent bot ids that are allowed to access the skill
        # to add a new parent bot simply go to the AllowedCallers and add
        # the parent bot's microsoft app id to the list
        caller_list = getattr(config, self.config_key)
        if caller_list is None:
            raise TypeError(f'"{self.config_key}" not found in configuration.')
        self._allowed_callers = caller_list

    @property
        def claims_validator(self) -> Callable[[List[Dict]], Awaitable]:
            async def allow_callers_claims_validator(claims: Dict[str, object]):
                if skillValidation.is_skill_claim(claims):
                    raise PermissionError(
                        "Invalid call from a skill."
                    )

                return

        return allow_callers_claims_validator
```

Update `BotFrameworkAdapter` instantiation, to pass the `AuthenticationConfiguration` constructor the function defined above:
```python
AUTH_CONFIG = AuthenticationConfiguration(
    claims_validator=AllowedSkillsClaimsValidator(CONFIG).claims_validator
)
SETTINGS = BotFrameworkAdapterSettings(
    ...,
    auth_configuration=AUTH_CONFIG,
)
ADAPTER = BotFrameworkAdapter(
    ...,
    SETTINGS,
)
```
