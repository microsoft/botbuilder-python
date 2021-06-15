from unittest import TestCase
from uuid import UUID, uuid4

from botframework.streaming.payloads import StreamManager
from botframework.streaming.payloads.assemblers import PayloadStreamAssembler
from botframework.streaming.payloads.models import Header


class TestStreamManager(TestCase):
    def test_ctor_null_cancel_ok(self):
        manager = StreamManager(None)
        self.assertIsNotNone(manager)

    def test_get_payload_assembler_not_exists_ok(self):
        manager = StreamManager(None)
        identifier: UUID = uuid4()

        assembler = manager.get_payload_assembler(identifier)

        self.assertIsNotNone(assembler)
        self.assertEqual(identifier, assembler.identifier)

    def test_get_payload_assembler_exists_ok(self):
        manager = StreamManager(None)
        identifier: UUID = uuid4()

        assembler1 = manager.get_payload_assembler(identifier)
        assembler2 = manager.get_payload_assembler(identifier)

        self.assertEqual(assembler1, assembler2)

    def test_get_payload_stream_not_exists_ok(self):
        manager = StreamManager(None)
        identifier: UUID = uuid4()

        stream = manager.get_payload_stream(Header(id=identifier))

        self.assertIsNotNone(stream)

    def test_get_payload_stream_exists_ok(self):
        manager = StreamManager(None)
        identifier: UUID = uuid4()

        stream1 = manager.get_payload_stream(Header(id=identifier))
        stream2 = manager.get_payload_stream(Header(id=identifier))

        self.assertEqual(stream1, stream2)

    def test_get_payload_stream_streams_match(self):
        manager = StreamManager(None)
        identifier: UUID = uuid4()

        assembler = manager.get_payload_assembler(identifier)
        stream = manager.get_payload_stream(Header(id=identifier))

        self.assertEqual(assembler.get_payload_as_stream(), stream)

    def test_on_receive_not_exists_no_op(self):
        manager = StreamManager(None)
        identifier: UUID = uuid4()

        manager.on_receive(Header(id=identifier), [], 100)

    def test_on_receive_exists(self):
        manager = StreamManager(None)
        identifier: UUID = uuid4()

        assembler = manager.get_payload_assembler(identifier)
        assembler.get_payload_as_stream()

        manager.on_receive(Header(id=identifier, end=True), [], 100)

        self.assertTrue(assembler.end)

    def test_close_stream_not_exists_no_op(self):
        manager = StreamManager(None)
        identifier: UUID = uuid4()

        manager.close_stream(identifier)

    def test_close_stream_not_end_closed(self):
        closed = False

        def mock_cancel_stream(_: PayloadStreamAssembler):
            nonlocal closed
            closed = True

        manager = StreamManager(on_cancel_stream=mock_cancel_stream)
        identifier: UUID = uuid4()
        assembler = manager.get_payload_assembler(identifier)
        assembler.get_payload_as_stream()

        manager.close_stream(identifier)

        self.assertTrue(closed)

    def test_close_stream_end_no_op(self):
        closed = False

        def mock_cancel_stream(_: PayloadStreamAssembler):
            nonlocal closed
            closed = True

        manager = StreamManager(on_cancel_stream=mock_cancel_stream)
        identifier: UUID = uuid4()
        assembler = manager.get_payload_assembler(identifier)
        assembler.get_payload_as_stream()
        assembler.on_receive(Header(end=True), [], 1)  # Set it as ended

        manager.close_stream(identifier)

        self.assertFalse(closed)
