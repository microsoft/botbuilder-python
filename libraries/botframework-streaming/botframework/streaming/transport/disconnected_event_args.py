# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.


class DisconnectedEventArgs:
    def __init__(self, *, reason: str = None):
        self.reason = reason


DisconnectedEventArgs.empty = DisconnectedEventArgs()
