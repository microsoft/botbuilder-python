from asyncio import Semaphore
from typing import List
from uuid import UUID, uuid4

import aiounittest
from botbuilder.streaming.payload_transport import PayloadSender
from botbuilder.streaming.payloads import HeaderSerializer
from botbuilder.streaming.payloads.models import Header
from botbuilder.streaming.transport import TransportSenderBase


class MockTransportSender(TransportSenderBase):
    def __init__(self):
        super().__init__()
        self.send_called = Semaphore(0)

    async def send(self, buffer: List[int], offset: int, count: int) -> int:
        # Assert
        if count == 48:  # Header
            print("Validating Header...")
            header = HeaderSerializer.deserialize(buffer, offset, count)
            assert header.type == "A"
            assert header.payload_length == 3
            assert header.end
        else:  # Payload
            print("Validating Payload...")
            assert count == 3
            self.send_called.release()

        return count

    def close(self):
        pass


class TestPayloadSender(aiounittest.AsyncTestCase):
    async def test_send(self):
        # Arrange
        sut = PayloadSender()
        sender = MockTransportSender()
        sut.connect(sender)

        headerId: UUID = uuid4()
        header = Header(type="A", id=headerId, end=True)
        header.payload_length = 3
        payload = [1, 2, 3]

        async def mock_sent_callback(h: Header):
            print(f"{h.type}.{h.payload_length}.{h.id}.{h.end}")

        # Act
        sut.send_payload(
            header, payload, is_length_known=True, sent_callback=mock_sent_callback
        )

        # Assert
        await sender.send_called.acquire()
        await sut.disconnect()
