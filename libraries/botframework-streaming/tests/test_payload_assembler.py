from unittest import TestCase
from uuid import UUID, uuid4

from botframework.streaming.payloads import StreamManager
from botframework.streaming.payloads.assemblers import PayloadStreamAssembler
from botframework.streaming.payloads.models import Header


class TestPayloadAssembler(TestCase):
    def test_ctor_id(self):
        identifier: UUID = uuid4()
        stream_manager = StreamManager()
        assembler = PayloadStreamAssembler(stream_manager, identifier)
        self.assertEqual(identifier, assembler.identifier)

    def test_ctor_end_false(self):
        identifier: UUID = uuid4()
        stream_manager = StreamManager()
        assembler = PayloadStreamAssembler(stream_manager, identifier)
        self.assertFalse(assembler.end)

    def test_get_stream(self):
        identifier: UUID = uuid4()
        stream_manager = StreamManager()
        assembler = PayloadStreamAssembler(stream_manager, identifier)
        stream = assembler.get_payload_as_stream()
        self.assertIsNotNone(stream)

    def test_get_stream_does_not_make_new_each_time(self):
        identifier: UUID = uuid4()
        stream_manager = StreamManager()
        assembler = PayloadStreamAssembler(stream_manager, identifier)
        stream1 = assembler.get_payload_as_stream()
        stream2 = assembler.get_payload_as_stream()
        self.assertEqual(stream1, stream2)

    def test_on_receive_sets_end(self):
        identifier: UUID = uuid4()
        stream_manager = StreamManager()
        assembler = PayloadStreamAssembler(stream_manager, identifier)

        header = Header()
        header.end = True

        assembler.get_payload_as_stream()
        assembler.on_receive(header, [], 100)

        self.assertTrue(assembler.end)

    def test_close_does_not_set_end(self):
        identifier: UUID = uuid4()
        stream_manager = StreamManager()
        assembler = PayloadStreamAssembler(stream_manager, identifier)

        assembler.close()

        self.assertFalse(assembler.end)
