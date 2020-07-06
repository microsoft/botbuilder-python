# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from msrest.serialization import Model


class HealthResults(Model):
    _attribute_map = {
        "success": {"key": "success", "type": "bool"},
        "authorization": {"key": "authorization", "type": "str"},
        "user_agent": {"key": "user-agent", "type": "str"},
        "messages": {"key": "messages", "type": "[str]"},
        "diagnostics": {"key": "diagnostics", "type": "object"},
    }

    def __init__(
        self,
        *,
        success: bool = None,
        authorization: str = None,
        user_agent: str = None,
        messages: [str] = None,
        diagnostics: object = None,
        **kwargs
    ) -> None:
        super(HealthResults, self).__init__(**kwargs)
        self.success = success
        self.authorization = authorization
        self.user_agent = user_agent
        self.messages = messages
        self.diagnostics = diagnostics
