import json

import aiounittest

from botbuilder.schema import Activity
from botframework.streaming import ReceiveRequest, StreamingRequest
from botframework.streaming.payloads import ResponseMessageStream


class TestRequests(aiounittest.AsyncTestCase):
    async def test_receive_request_empty_streams(self):
        sut = ReceiveRequest()

        self.assertIsNotNone(sut.streams)
        self.assertEqual(0, len(sut.streams))

    async def test_receive_request_null_properties(self):
        sut = ReceiveRequest()

        self.assertIsNone(sut.verb)
        self.assertIsNone(sut.path)

    async def test_streaming_request_null_properties(self):
        sut = StreamingRequest()

        self.assertIsNone(sut.verb)
        self.assertIsNone(sut.path)

    async def test_streaming_request_add_stream_null_throws(self):
        sut = StreamingRequest()

        with self.assertRaises(TypeError):
            sut.add_stream(None)

    async def test_streaming_request_add_stream_success(self):
        sut = StreamingRequest()
        content = "hi"

        sut.add_stream(content)

        self.assertIsNotNone(sut.streams)
        self.assertEqual(1, len(sut.streams))
        self.assertEqual(content, sut.streams[0].content)

    async def test_streaming_request_add_stream_existing_list_success(self):
        sut = StreamingRequest()
        content = "hi"
        content_2 = "hello"

        sut.streams = [ResponseMessageStream(content=content_2)]

        sut.add_stream(content)

        self.assertIsNotNone(sut.streams)
        self.assertEqual(2, len(sut.streams))
        self.assertEqual(content_2, sut.streams[0].content)
        self.assertEqual(content, sut.streams[1].content)

    async def test_streaming_request_create_get_success(self):
        sut = StreamingRequest.create_get()

        self.assertEqual(StreamingRequest.GET, sut.verb)
        self.assertIsNone(sut.path)
        self.assertIsNone(sut.streams)

    async def test_streaming_request_create_post_success(self):
        sut = StreamingRequest.create_post()

        self.assertEqual(StreamingRequest.POST, sut.verb)
        self.assertIsNone(sut.path)
        self.assertIsNone(sut.streams)

    async def test_streaming_request_create_delete_success(self):
        sut = StreamingRequest.create_delete()

        self.assertEqual(StreamingRequest.DELETE, sut.verb)
        self.assertIsNone(sut.path)
        self.assertIsNone(sut.streams)

    async def test_streaming_request_create_put_success(self):
        sut = StreamingRequest.create_put()

        self.assertEqual(StreamingRequest.PUT, sut.verb)
        self.assertIsNone(sut.path)
        self.assertIsNone(sut.streams)

    async def test_streaming_request_create_with_body_success(self):
        content = "hi"
        sut = StreamingRequest.create_request(StreamingRequest.POST, "123", content)

        self.assertEqual(StreamingRequest.POST, sut.verb)
        self.assertEqual("123", sut.path)
        self.assertIsNotNone(sut.streams)
        self.assertEqual(1, len(sut.streams))
        self.assertEqual(content, sut.streams[0].content)

    async def test_streaming_request_set_body_string_success(self):
        sut = StreamingRequest()

        sut.set_body("123")

        self.assertIsNotNone(sut.streams)
        self.assertEqual(1, len(sut.streams))
        self.assertIsInstance(sut.streams[0].content, list)
        self.assertIsInstance(sut.streams[0].content[0], int)
        self.assertEqual("123", bytes(sut.streams[0].content).decode("utf-8-sig"))

    async def test_streaming_request_set_body_none_does_not_throw(self):
        sut = StreamingRequest()

        sut.set_body(None)

    async def test_streaming_request_set_body_success(self):
        sut = StreamingRequest()
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
