# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from enum import IntEnum


class WebSocketCloseStatus(IntEnum):
    NORMAL_CLOSURE = 1000
    ENDPOINT_UNAVAILABLE = 1001
    PROTOCOL_ERROR = 1002
    INVALID_MESSAGE_TYPE = 1003
    EMPTY = 1005
    INVALID_PAYLOAD_DATA = 1007
    POLICY_VIOLATION = 1008
    MESSAGE_TOO_BIG = 1009
    MANDATORY_EXTENSION = 1010
    INTERNAL_SERVER_ERROR = 1011
