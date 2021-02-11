# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
import asyncio
from uuid import uuid4
import aiounittest

from botbuilder.core import ShowTypingMiddleware, TurnContext
from botbuilder.core.adapters import TestAdapter
from botbuilder.schema import Activity, ActivityTypes
from botframework.connector.auth import AuthenticationConstants, ClaimsIdentity


class SkillTestAdapter(TestAdapter):
    def create_turn_context(self, activity: Activity) -> TurnContext:
        turn_context = super().create_turn_context(activity)

        claims_identity = ClaimsIdentity(
            claims={
                AuthenticationConstants.VERSION_CLAIM: "2.0",
                AuthenticationConstants.AUDIENCE_CLAIM: str(uuid4()),
                AuthenticationConstants.AUTHORIZED_PARTY: str(uuid4()),
            },
            is_authenticated=True,
        )

        turn_context.turn_state[self.BOT_IDENTITY_KEY] = claims_identity

        return turn_context


class TestShowTypingMiddleware(aiounittest.AsyncTestCase):
    async def test_should_automatically_send_a_typing_indicator(self):
        async def aux(context):
            await asyncio.sleep(0.600)
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
            await asyncio.sleep(0.600)
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

    async def test_not_send_not_send_typing_indicator_when_bot_running_as_skill(self):
        async def aux(context):
            await asyncio.sleep(1)
            await context.send_activity(f"echo:{context.activity.text}")

        skill_adapter = SkillTestAdapter(aux)
        skill_adapter.use(ShowTypingMiddleware(0.001, 1))

        step1 = await skill_adapter.send("foo")
        await step1.assert_reply("echo:foo")
