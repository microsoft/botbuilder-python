# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from uuid import UUID
from typing import List

from botframework.streaming.transport import TransportConstants

from .models import Header

_CHAR_TO_BINARY_INT = {val.decode(): list(val)[0] for val in [b".", b"\n", b"1", b"0"]}


# TODO: consider abstracting the binary int list logic into a class for easier handling
class HeaderSerializer:
    DELIMITER = _CHAR_TO_BINARY_INT["."]
    TERMINATOR = _CHAR_TO_BINARY_INT["\n"]
    END = _CHAR_TO_BINARY_INT["1"]
    NOT_END = _CHAR_TO_BINARY_INT["0"]
    TYPE_OFFSET = 0
    TYPE_DELIMITER_OFFSET = 1
    LENGTH_OFFSET = 2
    LENGTH_LENGTH = 6
    LENGTH_DELIMETER_OFFSET = 8
    ID_OFFSET = 9
    ID_LENGTH = 36
    ID_DELIMETER_OFFSET = 45
    END_OFFSET = 46
    TERMINATOR_OFFSET = 47

    @staticmethod
    def serialize(
        header: Header,
        buffer: List[int],
        offset: int,  # pylint: disable=unused-argument
    ) -> int:
        # write type
        buffer[HeaderSerializer.TYPE_OFFSET] = HeaderSerializer._char_to_binary_int(
            header.type
        )
        buffer[HeaderSerializer.TYPE_DELIMITER_OFFSET] = HeaderSerializer.DELIMITER

        # write length
        length_binary_array: List[int] = list(
            HeaderSerializer._int_to_formatted_encoded_str(
                header.payload_length, "{:06d}"
            )
        )
        HeaderSerializer._write_in_buffer(
            length_binary_array, buffer, HeaderSerializer.LENGTH_OFFSET
        )
        buffer[HeaderSerializer.LENGTH_DELIMETER_OFFSET] = HeaderSerializer.DELIMITER

        # write id
        id_binary_array: List[int] = list(
            HeaderSerializer._uuid_to_numeric_encoded_str(header.id)
        )
        HeaderSerializer._write_in_buffer(
            id_binary_array, buffer, HeaderSerializer.ID_OFFSET
        )
        buffer[HeaderSerializer.ID_DELIMETER_OFFSET] = HeaderSerializer.DELIMITER

        # write terminator
        buffer[HeaderSerializer.END_OFFSET] = (
            HeaderSerializer.END if header.end else HeaderSerializer.NOT_END
        )
        buffer[HeaderSerializer.TERMINATOR_OFFSET] = HeaderSerializer.TERMINATOR

        return TransportConstants.MAX_HEADER_LENGTH

    @staticmethod
    def deserialize(
        buffer: List[int], offset: int, count: int  # pylint: disable=unused-argument
    ) -> Header:
        if count != TransportConstants.MAX_HEADER_LENGTH:
            raise ValueError("Cannot deserialize header, incorrect length")

        header = Header(
            type=HeaderSerializer._binary_int_to_char(
                buffer[HeaderSerializer.TYPE_OFFSET]
            )
        )

        if buffer[HeaderSerializer.TYPE_DELIMITER_OFFSET] != HeaderSerializer.DELIMITER:
            raise ValueError("Header type delimeter is malformed")

        length_str = HeaderSerializer._binary_array_to_str(
            buffer[
                HeaderSerializer.LENGTH_OFFSET : HeaderSerializer.LENGTH_OFFSET
                + HeaderSerializer.LENGTH_LENGTH
            ]
        )

        try:
            length = int(length_str)
        except Exception:
            raise ValueError("Header length is malformed")

        header.payload_length = length

        if (
            buffer[HeaderSerializer.LENGTH_DELIMETER_OFFSET]
            != HeaderSerializer.DELIMITER
        ):
            raise ValueError("Header length delimeter is malformed")

        identifier_str = HeaderSerializer._binary_array_to_str(
            buffer[
                HeaderSerializer.ID_OFFSET : HeaderSerializer.ID_OFFSET
                + HeaderSerializer.ID_LENGTH
            ]
        )

        try:
            identifier = UUID(identifier_str)
        except Exception:
            raise ValueError("Header id is malformed")

        header.id = identifier

        if buffer[HeaderSerializer.ID_DELIMETER_OFFSET] != HeaderSerializer.DELIMITER:
            raise ValueError("Header id delimeter is malformed")

        if buffer[HeaderSerializer.END_OFFSET] not in [
            HeaderSerializer.END,
            HeaderSerializer.NOT_END,
        ]:
            raise ValueError("Header end is malformed")

        header.end = buffer[HeaderSerializer.END_OFFSET] == HeaderSerializer.END

        if buffer[HeaderSerializer.TERMINATOR_OFFSET] != HeaderSerializer.TERMINATOR:
            raise ValueError("Header terminator is malformed")

        return header

    @staticmethod
    def _char_to_binary_int(char: str) -> int:
        if len(char) != 1:
            raise ValueError("Char to cast should be a str of exactly length 1")

        unicode_list = list(char.encode())

        if len(unicode_list) != 1:
            raise ValueError("Char to cast should be in the ASCII domain")

        return unicode_list[0]

    @staticmethod
    def _int_to_formatted_encoded_str(value: int, str_format: str) -> bytes:
        return str_format.format(value).encode("ascii")

    @staticmethod
    def _uuid_to_numeric_encoded_str(value: UUID) -> bytes:
        return str(value).encode("ascii")

    @staticmethod
    def _binary_int_to_char(binary_int: int) -> str:
        return bytes([binary_int]).decode("ascii")

    @staticmethod
    def _binary_array_to_str(binary_array: List[int]) -> str:
        return bytes(binary_array).decode("ascii")

    @staticmethod
    def _write_in_buffer(data: List[int], buffer: List[int], insert_index: int):
        for byte_int in data:
            buffer[insert_index] = byte_int
            insert_index += 1
