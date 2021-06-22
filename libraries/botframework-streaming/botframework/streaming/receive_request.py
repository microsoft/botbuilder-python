# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import List

from botframework.streaming.payloads import ContentStream


class ReceiveRequest:
    def __init__(
        self, *, verb: str = None, path: str = None, streams: List[ContentStream] = None
    ):
        self.verb = verb
        self.path = path
        self.streams: List[ContentStream] = streams or []

    async def read_body_as_str(self) -> str:
        try:
            content_stream = self.streams[0] if self.streams else None

            if not content_stream:
                # TODO: maybe raise an error
                return ""

            # TODO: encoding double check
            stream = await content_stream.stream.read_until_end()
            return bytes(stream).decode("utf-8-sig")
        except Exception as error:
            raise error
