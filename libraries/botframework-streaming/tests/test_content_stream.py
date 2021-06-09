# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from uuid import uuid4

import aiounittest

from botframework.streaming.payloads import ContentStream
from botframework.streaming.payloads.assemblers import PayloadStreamAssembler


class TestResponses(aiounittest.AsyncTestCase):
    async def test_content_stream_ctor_none_assembler_throws(self):
        with self.assertRaises(TypeError):
            ContentStream(uuid4(), None)

    async def test_content_stream_id(self):
        test_id = uuid4()
        test_assembler = PayloadStreamAssembler(None, test_id)
        sut = ContentStream(test_id, test_assembler)

        self.assertEqual(test_id, sut.identifier)

    async def test_content_stream_type(self):
        test_id = uuid4()
        test_assembler = PayloadStreamAssembler(None, test_id)
        sut = ContentStream(test_id, test_assembler)
        test_type = "foo/bar"

        sut.content_type = test_type

        self.assertEqual(test_type, sut.content_type)

        sut.cancel()
