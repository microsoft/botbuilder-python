# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from uuid import uuid4, UUID


class ResponseMessageStream:
    # pylint: disable=invalid-name
    def __init__(self, *, id: UUID = None, content: object = None):
        self.id = id or uuid4()
        self.content = content
