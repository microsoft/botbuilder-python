# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from .header import Header


class PayloadTypes:
    REQUEST = "A"
    RESPONSE = "B"
    STREAM = "S"
    CANCEL_ALL = "X"
    CANCEL_STREAM = "C"

    @staticmethod
    def is_stream(header: Header) -> bool:
        return header.type == PayloadTypes.STREAM
