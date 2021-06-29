# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import List
from uuid import uuid4

import aiounittest

from botframework.streaming import PayloadStream, StreamingRequest
from botframework.streaming.payloads import SendOperations
from botframework.streaming.payloads.assemblers import PayloadStreamAssembler
from botframework.streaming.payload_transport import PayloadSender
from botframework.streaming.transport import TransportSenderBase


class MockTransportSender(TransportSenderBase):
    # pylint: disable=unused-argument
    def __init__(self):
        super().__init__()
        self.is_connected = True
        self.buffers = []

    async def send(self, buffer: List[int], offset: int, count: int) -> int:
        self.buffers.append(buffer.copy())

        return count


class TestSendOperations(aiounittest.AsyncTestCase):
    async def test_request_dissasembler_with_variable_stream_send(self):
        sender = PayloadSender()
        transport = MockTransportSender()
        sender.connect(transport)

        sut = SendOperations(sender)

        request = StreamingRequest.create_post("/a/b")
        stream = PayloadStream(PayloadStreamAssembler(None, uuid4(), "blah", 100))
        stream.write([0] * 100, 0, 100)
        request.add_stream(await stream.read_until_end())

        await sut.send_request(uuid4(), request)
        self.assertEqual(4, len(transport.buffers))

    async def test_request_dissasembler_with_json_stream_send(self):
        sender = PayloadSender()
        transport = MockTransportSender()
        sender.connect(transport)

        sut = SendOperations(sender)

        request = StreamingRequest.create_post("/a/b")
        request.add_stream(bytes("abc", "ascii"))

        await sut.send_request(uuid4(), request)
        self.assertEqual(4, len(transport.buffers))
