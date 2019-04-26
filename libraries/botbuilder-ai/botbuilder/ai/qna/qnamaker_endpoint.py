# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

class QnAMakerEndpoint:
    def __init__(self, knowledge_base_id: str, endpoint_key: str, host: str):
        self.knowledge_base_id = knowledge_base_id
        self.endpoint_key = endpoint_key
        self.host = host