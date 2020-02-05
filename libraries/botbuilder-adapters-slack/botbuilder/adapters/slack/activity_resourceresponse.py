# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.schema import ResourceResponse, ConversationAccount


class ActivityResourceResponse(ResourceResponse):
    def __init__(self, activity_id: str, conversation: ConversationAccount, **kwargs):
        super().__init__(**kwargs)
        self.activity_id = activity_id
        self.conversation = conversation
