# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from msrest.serialization import Model


class ReferrInfo(Model):
    KEY = "botbuilder.skills.ReferrInfo"

    _attribute_map = {
        "from_bot_id": {"key": "fromBotId", "type": "str"},
        "to_bot_id": {"key": "toBotId", "type": "str"},
        "conversation_id": {"key": "conversationId", "type": "str"},
        "service_url": {"key": "serviceUrl", "type": "str"},
    }

    def __init__(
        self,
        *,
        from_bot_id: str = None,
        to_bot_id: str = None,
        conversation_id: str = None,
        service_url: str = None,
        **kwargs
    ):
        super(ReferrInfo, self).__init__(**kwargs)
        self.from_bot_id = from_bot_id
        self.to_bot_id = to_bot_id
        self.conversation_id = conversation_id
        self.service_url = service_url
