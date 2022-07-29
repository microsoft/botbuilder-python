# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

# pylint: disable=ungrouped-imports
import enum
from typing import List
import uuid

import aiounittest

from botframework.connector.auth import ClaimsIdentity, AuthenticationConstants
from botbuilder.core import (
    TurnContext,
    MessageFactory,
    MemoryStorage,
    ConversationState,
    UserState,
    AdapterExtensions,
    BotAdapter,
)
from botbuilder.core.adapters import (
    TestFlow,
    TestAdapter,
)
from botbuilder.core.skills import (
    SkillHandler,
    SkillConversationReference,
)
from botbuilder.core.transcript_logger import (
    TranscriptLoggerMiddleware,
    ConsoleTranscriptLogger,
)
from botbuilder.schema import ActivityTypes, Activity, EndOfConversationCodes
from botbuilder.dialogs import (
    ComponentDialog,
    TextPrompt,
    WaterfallDialog,
    DialogInstance,
    DialogReason,
    WaterfallStepContext,
    PromptOptions,
    Dialog,
    DialogExtensions,
    DialogEvents,
)


class SimpleComponentDialog(ComponentDialog):
    def __init__(self):
        super().__init__("SimpleComponentDialog")

        self.add_dialog(TextPrompt("TextPrompt"))
        self.add_dialog(
            WaterfallDialog("WaterfallDialog", [self.prompt_for_name, self.final_step])
        )

        self.initial_dialog_id = "WaterfallDialog"
        self.end_reason = DialogReason.BeginCalled

    async def end_dialog(
        self, context: TurnContext, instance: DialogInstance, reason: DialogReason
    ) -> None:
        self.end_reason = reason
        return await super().end_dialog(context, instance, reason)

    async def prompt_for_name(self, step_context: WaterfallStepContext):
        return await step_context.prompt(
            "TextPrompt",
            PromptOptions(
                prompt=MessageFactory.text("Hello, what is your name?"),
                retry_prompt=MessageFactory.text("Hello, what is your name again?"),
            ),
        )

    async def final_step(self, step_context: WaterfallStepContext):
        await step_context.context.send_activity(
            f"Hello {step_context.result}, nice to meet you!"
        )
        return await step_context.end_dialog(step_context.result)


class FlowTestCase(enum.Enum):
    root_bot_only = 1
    root_bot_consuming_skill = 2
    middle_skill = 3
    leaf_skill = 4


class DialogExtensionsTests(aiounittest.AsyncTestCase):
    def __init__(self, methodName):
        super().__init__(methodName)
        self.eoc_sent: Activity = None
        self.skill_bot_id = str(uuid.uuid4())
        self.parent_bot_id = str(uuid.uuid4())

    async def handles_bot_and_skills_test_cases(
        self, test_case: FlowTestCase, send_eoc: bool
    ):
        dialog = SimpleComponentDialog()

        test_flow = self.create_test_flow(dialog, test_case)

        await test_flow.send("Hi")
        await test_flow.assert_reply("Hello, what is your name?")
        await test_flow.send("SomeName")
        await test_flow.assert_reply("Hello SomeName, nice to meet you!")

        assert dialog.end_reason == DialogReason.EndCalled

        if send_eoc:
            self.assertIsNotNone(
                self.eoc_sent, "Skills should send EndConversation to channel"
            )
            assert ActivityTypes.end_of_conversation == self.eoc_sent.type
            assert EndOfConversationCodes.completed_successfully == self.eoc_sent.code
            assert self.eoc_sent.value == "SomeName"
        else:
            self.assertIsNone(
                self.eoc_sent, "Root bot should not send EndConversation to channel"
            )

    async def test_handles_root_bot_only(self):
        return await self.handles_bot_and_skills_test_cases(
            FlowTestCase.root_bot_only, False
        )

    async def test_handles_root_bot_consuming_skill(self):
        return await self.handles_bot_and_skills_test_cases(
            FlowTestCase.root_bot_consuming_skill, False
        )

    async def test_handles_middle_skill(self):
        return await self.handles_bot_and_skills_test_cases(
            FlowTestCase.middle_skill, True
        )

    async def test_handles_leaf_skill(self):
        return await self.handles_bot_and_skills_test_cases(
            FlowTestCase.leaf_skill, True
        )

    async def test_skill_handles_eoc_from_parent(self):
        dialog = SimpleComponentDialog()
        test_flow = self.create_test_flow(dialog, FlowTestCase.leaf_skill)

        await test_flow.send("Hi")
        await test_flow.assert_reply("Hello, what is your name?")
        await test_flow.send(
            Activity(
                type=ActivityTypes.end_of_conversation,
                caller_id=self.parent_bot_id,
            )
        )

        self.assertIsNone(
            self.eoc_sent,
            "Skill should not send back EoC when an EoC is sent from a parent",
        )
        assert dialog.end_reason == DialogReason.CancelCalled

    async def test_skill_handles_reprompt_from_parent(self):
        dialog = SimpleComponentDialog()
        test_flow = self.create_test_flow(dialog, FlowTestCase.leaf_skill)

        await test_flow.send("Hi")
        await test_flow.assert_reply("Hello, what is your name?")
        await test_flow.send(
            Activity(
                type=ActivityTypes.event,
                caller_id=self.parent_bot_id,
                name=DialogEvents.reprompt_dialog,
            )
        )
        await test_flow.assert_reply("Hello, what is your name?")

        assert dialog.end_reason == DialogReason.BeginCalled

    def create_test_flow(self, dialog: Dialog, test_case: FlowTestCase) -> TestFlow:
        conversation_id = str(uuid.uuid4())
        storage = MemoryStorage()
        convo_state = ConversationState(storage)
        user_state = UserState(storage)

        async def logic(context: TurnContext):
            if test_case != FlowTestCase.root_bot_only:
                claims_identity = ClaimsIdentity(
                    {
                        AuthenticationConstants.VERSION_CLAIM: "2.0",
                        AuthenticationConstants.AUDIENCE_CLAIM: self.skill_bot_id,
                        AuthenticationConstants.AUTHORIZED_PARTY: self.parent_bot_id,
                    },
                    True,
                )
                context.turn_state[BotAdapter.BOT_IDENTITY_KEY] = claims_identity

                if test_case == FlowTestCase.root_bot_consuming_skill:
                    context.turn_state[
                        SkillHandler.SKILL_CONVERSATION_REFERENCE_KEY
                    ] = SkillConversationReference(
                        None, AuthenticationConstants.TO_CHANNEL_FROM_BOT_OAUTH_SCOPE
                    )

                if test_case == FlowTestCase.middle_skill:
                    context.turn_state[
                        SkillHandler.SKILL_CONVERSATION_REFERENCE_KEY
                    ] = SkillConversationReference(None, self.parent_bot_id)

            async def capture_eoc(
                inner_context: TurnContext, activities: List[Activity], next
            ):  # pylint: disable=unused-argument
                for activity in activities:
                    if activity.type == ActivityTypes.end_of_conversation:
                        self.eoc_sent = activity
                        break
                return await next()

            context.on_send_activities(capture_eoc)

            await DialogExtensions.run_dialog(
                dialog, context, convo_state.create_property("DialogState")
            )

        adapter = TestAdapter(
            logic, TestAdapter.create_conversation_reference(conversation_id)
        )
        AdapterExtensions.use_storage(adapter, storage)
        AdapterExtensions.use_bot_state(adapter, user_state, convo_state)
        adapter.use(TranscriptLoggerMiddleware(ConsoleTranscriptLogger()))

        return TestFlow(None, adapter)
