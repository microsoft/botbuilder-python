# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.


class QnAMakerEndpoint:
    def __init__(self, knowledge_base_id: str, endpoint_key: str, host: str):
        if not knowledge_base_id:
            raise TypeError("QnAMakerEndpoint.knowledge_base_id cannot be empty.")

        if not endpoint_key:
            raise TypeError("QnAMakerEndpoint.endpoint_key cannot be empty.")

        if not host:
            raise TypeError("QnAMakerEndpoint.host cannot be empty.")

        self.knowledge_base_id = knowledge_base_id
        self.endpoint_key = endpoint_key
        self.host = host
