# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from abc import ABC


class TransportConstants(ABC):
    MAX_PAYLOAD_LENGTH = 4096
    MAX_HEADER_LENGTH = 48
    MAX_LENGTH = 999999
    MIN_LENGTH = 0
