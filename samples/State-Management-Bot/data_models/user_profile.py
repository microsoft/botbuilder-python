# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

class UserProfile:
    def __init__(self, name: str = None):
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value
