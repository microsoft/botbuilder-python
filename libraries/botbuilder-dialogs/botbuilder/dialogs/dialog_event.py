# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.


class DialogEvent:
    def __init__(self, bubble: bool = False, name: str = "", value: object = None):
        self.bubble = bubble
        self.name = name
        self.value: object = value
