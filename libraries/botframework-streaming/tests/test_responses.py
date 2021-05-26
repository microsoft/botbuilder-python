import json
from http import HTTPStatus

import aiounittest

from botbuilder.schema import Activity
from botframework.streaming import ReceiveResponse, StreamingResponse
from botframework.streaming.payloads import ResponseMessageStream


class TestResponses(aiounittest.AsyncTestCase):
    async def test_receive_response_empty_streams(self):
        sut = ReceiveResponse()

        self.assertIsNotNone(sut.streams)
        self.assertEqual(0, len(sut.streams))

    async def test_receive_response_none_properties(self):
        sut = ReceiveResponse()

        self.assertEqual(0, sut.status_code)

    async def test_streaming_response_null_properties(self):
        sut = StreamingResponse()

        self.assertEqual(0, sut.status_code)
        self.assertIsNone(sut.streams)

    async def test_streaming_response_add_stream_none_throws(self):
        sut = StreamingResponse()

        with self.assertRaises(TypeError):
            sut.add_stream(None)

    async def test_streaming_response_add_stream_success(self):
        sut = StreamingResponse()
        content = "hi"

        sut.add_stream(content)

        self.assertIsNotNone(sut.streams)
        self.assertEqual(1, len(sut.streams))
        self.assertEqual(content, sut.streams[0].content)

    async def test_streaming_response_add_stream_existing_list_success(self):
        sut = StreamingResponse()
        content = "hi"
        content_2 = "hello"

        sut.streams = [ResponseMessageStream(content=content_2)]

        sut.add_stream(content)

        self.assertIsNotNone(sut.streams)
        self.assertEqual(2, len(sut.streams))
        self.assertEqual(content_2, sut.streams[0].content)
        self.assertEqual(content, sut.streams[1].content)

    async def test_streaming_response_not_found_success(self):
        sut = StreamingResponse.not_found()

        self.assertEqual(HTTPStatus.NOT_FOUND, sut.status_code)
        self.assertIsNone(sut.streams)

    async def test_streaming_response_forbidden_success(self):
        sut = StreamingResponse.forbidden()

        self.assertEqual(HTTPStatus.FORBIDDEN, sut.status_code)
        self.assertIsNone(sut.streams)

    async def test_streaming_response_ok_success(self):
        sut = StreamingResponse.ok()

        self.assertEqual(HTTPStatus.OK, sut.status_code)
        self.assertIsNone(sut.streams)

    async def test_streaming_response_internal_server_error_success(self):
        sut = StreamingResponse.internal_server_error()

        self.assertEqual(HTTPStatus.INTERNAL_SERVER_ERROR, sut.status_code)
        self.assertIsNone(sut.streams)

    async def test_streaming_response_create_with_body_success(self):
        content = "hi"
        sut = StreamingResponse.create_response(HTTPStatus.OK, content)

        self.assertEqual(HTTPStatus.OK, sut.status_code)
        self.assertIsNotNone(sut.streams)
        self.assertEqual(1, len(sut.streams))
        self.assertEqual(content, sut.streams[0].content)

    async def test_streaming_response_set_body_string_success(self):
        sut = StreamingResponse()

        sut.set_body("123")

        self.assertIsNotNone(sut.streams)
        self.assertEqual(1, len(sut.streams))
        self.assertIsInstance(sut.streams[0].content, list)
        self.assertIsInstance(sut.streams[0].content[0], int)
        self.assertEqual("123", bytes(sut.streams[0].content).decode("utf-8-sig"))

    async def test_streaming_response_set_body_none_does_not_throw(self):
        sut = StreamingResponse()

        sut.set_body(None)

    async def test_streaming_response_set_body_success(self):
        sut = StreamingResponse()
        activity = Activity(text="hi", type="message")

        sut.set_body(activity)

        self.assertIsNotNone(sut.streams)
        self.assertEqual(1, len(sut.streams))
        self.assertIsInstance(sut.streams[0].content, list)
        self.assertIsInstance(sut.streams[0].content[0], int)

        assert_activity = Activity.deserialize(
            json.loads(bytes(sut.streams[0].content).decode("utf-8-sig"))
        )

        self.assertEqual(activity.text, assert_activity.text)
        self.assertEqual(activity.type, assert_activity.type)

    async def test_receive_base_read_body_as_string_no_content_empty_string(self):
        sut = ReceiveResponse()
        sut.streams = []

        result = sut.read_body_as_str()

        self.assertEqual("", result)
