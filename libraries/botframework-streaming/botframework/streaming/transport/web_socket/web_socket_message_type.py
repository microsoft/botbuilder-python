# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from enum import IntEnum


class WebSocketMessageType(IntEnum):
    # websocket spec types
    CONTINUATION = 0
    TEXT = 1
    BINARY = 2
    PING = 9
    PONG = 10
    CLOSE = 8
