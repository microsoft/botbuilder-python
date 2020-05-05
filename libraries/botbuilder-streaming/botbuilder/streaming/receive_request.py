# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import List

from botbuilder.streaming.payloads import ContentStream


class ReceiveRequest:
    def __init__(
        self, *, verb: str = None, path: str = None, streams: List[ContentStream]
    ):
        self.verb = verb
        self.path = path
        self.streams: List[ContentStream] = streams or []

    def read_body_as_str(self) -> str:
        try:
            content_stream = self.streams[0] if self.streams else None

            if not content_stream:
                return ""

            # TODO: encoding double check
            return bytes(content_stream.stream).decode("utf8")
        except Exception as error:
            raise error
