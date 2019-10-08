# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import Dict, List, Union


class ConversationData:
    def __init__(
        self,
        timestamp: str = None,
        channel_id: str = None,
        prompted_for_user_name: bool = False,
    ):
        self.timestamp = timestamp
        self.channel_id = channel_id
        self.prompted_for_user_name = prompted_for_user_name

    @staticmethod
    def conversation_data_serializer(value: "ConversationData") -> Dict[str, Union[str, float, List]]:
        return dict(
            timestamp=value.timestamp,
            channel_id=value.channel_id,
            prompted_for_user_name=value.prompted_for_user_name
        )

    @staticmethod
    def conversation_data_deserializer(value: Dict[str, Union[str, float, List]]) -> "ConversationData":
        return ConversationData(
            timestamp=value["timestamp"],
            channel_id=value["channel_id"],
            prompted_for_user_name=value["prompted_for_user_name"]
        )
