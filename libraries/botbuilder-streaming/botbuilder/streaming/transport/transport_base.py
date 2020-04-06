# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.


class TransportBase:
    def __init__(self):
        self.is_connected: bool = None

    def close(self):
        return
