# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

class ConversationData:
    def __init__(self, timestamp: str = None, channel_id: str = None, prompted_for_user_name: bool = False):
        self._timestamp = timestamp
        self._channel_id = channel_id
        self._prompted_for_user_name = prompted_for_user_name

    @property
    def timestamp(self) -> str:
        return self._timestamp

    @timestamp.setter
    def timestamp(self, value: str) -> None:
        self._timestamp = value
    
    @property
    def channel_id(self) -> str:
        return self._channel_id

    @channel_id.setter
    def channel_id(self, value: str) -> None:
        self._channel_id = value
    
    @property
    def prompted_for_user_name(self) -> bool:
        return self._prompted_for_user_name

    @prompted_for_user_name.setter
    def prompted_for_user_name(self, value: bool) -> None:
        self._prompted_for_user_name = value
