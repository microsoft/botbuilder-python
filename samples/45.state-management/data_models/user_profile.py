# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import Dict, List, Union


class UserProfile:
    def __init__(self, name: str = None):
        self.name = name

    @staticmethod
    def user_profile_serializer(value: "UserProfile") -> Dict[str, Union[str, float, List]]:
        return dict(
            name=value.name
        )

    @staticmethod
    def user_profile_deserializer(value: Dict[str, Union[str, float, List]]) -> "UserProfile":
        return UserProfile(
            name=value["name"]
        )
