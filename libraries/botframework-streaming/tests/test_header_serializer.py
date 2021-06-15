from typing import List
from unittest import TestCase
from uuid import uuid4, UUID

import pytest
from botframework.streaming.payloads import HeaderSerializer
from botframework.streaming.payloads.models import Header, PayloadTypes
from botframework.streaming.transport import TransportConstants


class TestHeaderSerializer(TestCase):
    def test_can_round_trip(self):
        header = Header()
        header.type = PayloadTypes.REQUEST
        header.payload_length = 168
        header.id = uuid4()
        header.end = True

        buffer: List[int] = [None] * TransportConstants.MAX_PAYLOAD_LENGTH
        offset: int = 0

        length = HeaderSerializer.serialize(header, buffer, offset)
        result = HeaderSerializer.deserialize(buffer, 0, length)

        self.assertEqual(header.type, result.type)
        self.assertEqual(header.payload_length, result.payload_length)
        self.assertEqual(header.id, result.id)
        self.assertEqual(header.end, result.end)

    def test_serializes_to_ascii(self):
        header = Header()
        header.type = PayloadTypes.REQUEST
        header.payload_length = 168
        header.id = uuid4()
        header.end = True

        buffer: List[int] = [None] * TransportConstants.MAX_PAYLOAD_LENGTH
        offset: int = 0

        length = HeaderSerializer.serialize(header, buffer, offset)
        decoded = bytes(buffer[offset:length]).decode("ascii")

        self.assertEqual(f"A.000168.{str(header.id)}.1\n", decoded)

    def test_deserializes_from_ascii(self):
        header_id: UUID = uuid4()
        header: str = f"A.000168.{str(header_id)}.1\n"
        buffer: List[int] = list(bytes(header, "ascii"))

        result = HeaderSerializer.deserialize(buffer, 0, len(buffer))

        self.assertEqual("A", result.type)
        self.assertEqual(168, result.payload_length)
        self.assertEqual(header_id, result.id)
        self.assertTrue(result.end)

    def test_deserialize_unknown_type(self):
        header_id: UUID = uuid4()
        header: str = f"Z.000168.{str(header_id)}.1\n"
        buffer: List[int] = list(bytes(header, "ascii"))

        result = HeaderSerializer.deserialize(buffer, 0, len(buffer))

        self.assertEqual("Z", result.type)
        self.assertEqual(168, result.payload_length)

    def test_deserialize_length_too_short_throws(self):
        header_id: UUID = uuid4()
        header: str = f"A.000168.{str(header_id)}.1\n"
        buffer: List[int] = list(bytes(header, "ascii"))

        with pytest.raises(ValueError):
            HeaderSerializer.deserialize(buffer, 0, 5)

    def test_deserialize_length_too_long_throws(self):
        header_id: UUID = uuid4()
        header: str = f"A.000168.{str(header_id)}.1\n"
        buffer: List[int] = list(bytes(header, "ascii"))

        with pytest.raises(ValueError):
            HeaderSerializer.deserialize(buffer, 0, 55)

    def test_deserialize_bad_type_delimiter_throws(self):
        header_id: UUID = uuid4()
        header: str = f"Ax000168.{str(header_id)}.1\n"
        buffer: List[int] = list(bytes(header, "ascii"))

        with pytest.raises(ValueError):
            HeaderSerializer.deserialize(buffer, 0, len(buffer))

    def test_deserialize_bad_length_delimiter_throws(self):
        header_id: UUID = uuid4()
        header: str = f"A.000168x{str(header_id)}.1\n"
        buffer: List[int] = list(bytes(header, "ascii"))

        with pytest.raises(ValueError):
            HeaderSerializer.deserialize(buffer, 0, len(buffer))

    def test_deserialize_bad_id_delimiter_throws(self):
        header_id: UUID = uuid4()
        header: str = f"A.000168.{str(header_id)}x1\n"
        buffer: List[int] = list(bytes(header, "ascii"))

        with pytest.raises(ValueError):
            HeaderSerializer.deserialize(buffer, 0, len(buffer))

    def test_deserialize_bad_terminator_throws(self):
        header_id: UUID = uuid4()
        header: str = f"A.000168.{str(header_id)}.1c"
        buffer: List[int] = list(bytes(header, "ascii"))

        with pytest.raises(ValueError):
            HeaderSerializer.deserialize(buffer, 0, len(buffer))

    def test_deserialize_bad_length_throws(self):
        header_id: UUID = uuid4()
        header: str = f"A.00p168.{str(header_id)}.1\n"
        buffer: List[int] = list(bytes(header, "ascii"))

        with pytest.raises(ValueError):
            HeaderSerializer.deserialize(buffer, 0, len(buffer))

    def test_deserialize_bad_id_throws(self):
        header: str = "A.000168.68e9p9ca-a651-40f4-ad8f-3aaf781862b4.1\n"
        buffer: List[int] = list(bytes(header, "ascii"))

        with pytest.raises(ValueError):
            HeaderSerializer.deserialize(buffer, 0, len(buffer))

    def test_deserialize_bad_end_throws(self):
        header_id: UUID = uuid4()
        header: str = f"A.000168.{str(header_id)}.z\n"
        buffer: List[int] = list(bytes(header, "ascii"))

        with pytest.raises(ValueError):
            HeaderSerializer.deserialize(buffer, 0, len(buffer))
