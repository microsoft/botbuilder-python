from typing import List
from uuid import UUID, uuid4

import aiounittest
from botframework.streaming import ReceiveRequest
from botframework.streaming.payloads import StreamManager
from botframework.streaming.payloads.assemblers import (
    ReceiveRequestAssembler,
    PayloadStreamAssembler,
)
from botframework.streaming.payloads.models import (
    Header,
    RequestPayload,
    StreamDescription,
)


class MockStreamManager(StreamManager):
    def get_payload_assembler(self, identifier: UUID) -> PayloadStreamAssembler:
        return PayloadStreamAssembler(self, identifier)


class TestPayloadProcessor(aiounittest.AsyncTestCase):
    async def test_process_request(self):
        # Arrange
        header_id: UUID = uuid4()
        header = Header(type="A", id=header_id, end=True)
        header.payload_length = 3
        stream_manager = MockStreamManager()

        on_completed_called = False

        async def mock_on_completed(identifier: UUID, request: ReceiveRequest):
            nonlocal on_completed_called
            assert identifier == header_id
            assert request.verb == "POST"
            assert request.path == "/api/messages"
            assert len(request.streams) == 1
            on_completed_called = True

        sut = ReceiveRequestAssembler(
            header, stream_manager, on_completed=mock_on_completed
        )

        # Act
        stream_id: UUID = uuid4()
        streams: List[StreamDescription] = [
            StreamDescription(id=str(stream_id), content_type="json", length=100)
        ]
        payload = RequestPayload(
            verb="POST", path="/api/messages", streams=streams
        ).to_json()
        payload_stream: List[int] = list(bytes(payload, "utf-8"))
        await sut.process_request(payload_stream)

        # Assert
        assert on_completed_called
