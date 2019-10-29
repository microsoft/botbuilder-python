# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import time
import aiounittest

from botbuilder.core import ShowTypingMiddleware
from botbuilder.core.adapters import TestAdapter
from botbuilder.schema import ActivityTypes


class TestShowTypingMiddleware(aiounittest.AsyncTestCase):
    async def test_should_automatically_send_a_typing_indicator(self):
        async def aux(context):
            time.sleep(0.600)
            await context.send_activity(f"echo:{context.activity.text}")

        def assert_is_typing(activity, description):  # pylint: disable=unused-argument
            assert activity.type == ActivityTypes.typing

        adapter = TestAdapter(aux)
        adapter.use(ShowTypingMiddleware())

        step1 = await adapter.send("foo")
        step2 = await step1.assert_reply(assert_is_typing)
        step3 = await step2.assert_reply("echo:foo")
        step4 = await step3.send("bar")
        step5 = await step4.assert_reply(assert_is_typing)
        await step5.assert_reply("echo:bar")

    async def test_should_not_automatically_send_a_typing_indicator_if_no_middleware(
        self,
    ):
        async def aux(context):
            await context.send_activity(f"echo:{context.activity.text}")

        adapter = TestAdapter(aux)

        step1 = await adapter.send("foo")
        await step1.assert_reply("echo:foo")

    async def test_should_not_immediately_respond_with_message(self):
        async def aux(context):
            time.sleep(0.600)
            await context.send_activity(f"echo:{context.activity.text}")

        def assert_is_not_message(
            activity, description
        ):  # pylint: disable=unused-argument
            assert activity.type != ActivityTypes.message

        adapter = TestAdapter(aux)
        adapter.use(ShowTypingMiddleware())

        step1 = await adapter.send("foo")
        await step1.assert_reply(assert_is_not_message)

    async def test_should_immediately_respond_with_message_if_no_middleware(self):
        async def aux(context):
            await context.send_activity(f"echo:{context.activity.text}")

        def assert_is_message(activity, description):  # pylint: disable=unused-argument
            assert activity.type == ActivityTypes.message

        adapter = TestAdapter(aux)

        step1 = await adapter.send("foo")
        await step1.assert_reply(assert_is_message)
