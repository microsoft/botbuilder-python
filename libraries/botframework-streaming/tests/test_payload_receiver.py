from typing import List

import aiounittest

from botframework.streaming import PayloadStream
from botframework.streaming.payload_transport import PayloadReceiver
from botframework.streaming.transport import TransportReceiverBase


class MockTransportReceiver(TransportReceiverBase):
    # pylint: disable=unused-argument
    def __init__(self, mock_header: bytes, mock_payload: bytes):
        self._is_connected = True
        self._mock_gen = self._mock_receive(mock_header, mock_payload)

    def _mock_receive(self, mock_header: bytes, mock_payload: bytes):
        yield mock_header
        yield mock_payload

    @property
    def is_connected(self):
        if self._is_connected:
            self._is_connected = False
            return True
        return False

    async def close(self):
        return

    async def receive(self, buffer: object, offset: int, count: int) -> int:
        resp_buffer = list(next(self._mock_gen))
        for index, val in enumerate(resp_buffer):
            buffer[index] = val
        return len(resp_buffer)


class MockStream(PayloadStream):
    # pylint: disable=super-init-not-called
    def __init__(self):
        self.buffer = None
        self._producer_length = 0  # total length

    def give_buffer(self, buffer: List[int]):
        self.buffer = buffer


class TestBotFrameworkHttpClient(aiounittest.AsyncTestCase):
    async def test_connect(self):
        mock_header = b"S.000004.e35ed534-0808-4acf-af1e-24aa81d2b31d.1\n"
        mock_payload = b"test"

        mock_receiver = MockTransportReceiver(mock_header, mock_payload)
        mock_stream = MockStream()

        receive_action_called = False

        def mock_get_stream(header):  # pylint: disable=unused-argument
            return mock_stream

        def mock_receive_action(header, stream, offset):
            nonlocal receive_action_called
            assert header.type == "S"
            assert len(stream.buffer) == offset
            receive_action_called = True

        sut = PayloadReceiver()
        sut.subscribe(mock_get_stream, mock_receive_action)
        await sut.connect(mock_receiver)

        assert bytes(mock_stream.buffer) == mock_payload
        assert receive_action_called
