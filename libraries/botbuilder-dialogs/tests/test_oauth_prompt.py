# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import aiounittest
from botbuilder.dialogs.prompts import OAuthPromptSettings
from botbuilder.schema import (
    Activity,
    ActivityTypes,
    ChannelAccount,
    ConversationAccount,
    InputHints,
    TokenResponse,
)

from botbuilder.core import CardFactory, ConversationState, MemoryStorage, TurnContext
from botbuilder.core.adapters import TestAdapter
from botbuilder.dialogs import DialogSet, DialogTurnStatus, PromptOptions
from botbuilder.dialogs.prompts import OAuthPrompt


def create_reply(activity):
    return Activity(
        type=ActivityTypes.message,
        from_property=ChannelAccount(
            id=activity.recipient.id, name=activity.recipient.name
        ),
        recipient=ChannelAccount(
            id=activity.from_property.id, name=activity.from_property.name
        ),
        reply_to_id=activity.id,
        service_url=activity.service_url,
        channel_id=activity.channel_id,
        conversation=ConversationAccount(
            is_group=activity.conversation.is_group,
            id=activity.conversation.id,
            name=activity.conversation.name,
        ),
    )


class OAuthPromptTests(aiounittest.AsyncTestCase):
    async def test_should_call_oauth_prompt(self):
        connection_name = "myConnection"
        token = "abc123"

        async def callback_handler(turn_context: TurnContext):
            dialog_context = await dialogs.create_context(turn_context)

            results = await dialog_context.continue_dialog()
            if results.status == DialogTurnStatus.Empty:
                await dialog_context.prompt("prompt", PromptOptions())
            elif results.status == DialogTurnStatus.Complete:
                if results.result.token:
                    await turn_context.send_activity("Logged in.")
                else:
                    await turn_context.send_activity("Failed")

            await convo_state.save_changes(turn_context)

        # Initialize TestAdapter.
        adapter = TestAdapter(callback_handler)

        # Create ConversationState with MemoryStorage and register the state as middleware.
        convo_state = ConversationState(MemoryStorage())

        # Create a DialogState property, DialogSet and AttachmentPrompt.
        dialog_state = convo_state.create_property("dialogState")
        dialogs = DialogSet(dialog_state)
        dialogs.add(
            OAuthPrompt(
                "prompt", OAuthPromptSettings(connection_name, "Login", None, 300000)
            )
        )

        async def inspector(
            activity: Activity, description: str = None
        ):  # pylint: disable=unused-argument

            self.assertTrue(len(activity.attachments) == 1)
            self.assertTrue(
                activity.attachments[0].content_type
                == CardFactory.content_types.oauth_card
            )

            # send a mock EventActivity back to the bot with the token
            adapter.add_user_token(
                connection_name, activity.channel_id, activity.recipient.id, token
            )

            event_activity = create_reply(activity)
            event_activity.type = ActivityTypes.event
            event_activity.from_property, event_activity.recipient = (
                event_activity.recipient,
                event_activity.from_property,
            )
            event_activity.name = "tokens/response"
            event_activity.value = TokenResponse(
                connection_name=connection_name, token=token
            )

            context = TurnContext(adapter, event_activity)
            await callback_handler(context)

        step1 = await adapter.send("Hello")
        step2 = await step1.assert_reply(inspector)
        await step2.assert_reply("Logged in.")

    async def test_should_call_oauth_prompt_with_code(self):
        connection_name = "myConnection"
        token = "abc123"
        magic_code = "888999"

        async def exec_test(turn_context: TurnContext):
            dialog_context = await dialogs.create_context(turn_context)

            results = await dialog_context.continue_dialog()
            if results.status == DialogTurnStatus.Empty:
                await dialog_context.prompt("prompt", PromptOptions())
            elif results.status == DialogTurnStatus.Complete:
                if results.result.token:
                    await turn_context.send_activity("Logged in.")

                else:
                    await turn_context.send_activity("Failed")

            await convo_state.save_changes(turn_context)

        # Initialize TestAdapter.
        adapter = TestAdapter(exec_test)

        # Create ConversationState with MemoryStorage and register the state as middleware.
        convo_state = ConversationState(MemoryStorage())

        # Create a DialogState property, DialogSet and AttachmentPrompt.
        dialog_state = convo_state.create_property("dialog_state")
        dialogs = DialogSet(dialog_state)
        dialogs.add(
            OAuthPrompt(
                "prompt", OAuthPromptSettings(connection_name, "Login", None, 300000)
            )
        )

        def inspector(
            activity: Activity, description: str = None
        ):  # pylint: disable=unused-argument
            assert len(activity.attachments) == 1
            assert (
                activity.attachments[0].content_type
                == CardFactory.content_types.oauth_card
            )

            # send a mock EventActivity back to the bot with the token
            adapter.add_user_token(
                connection_name,
                activity.channel_id,
                activity.recipient.id,
                token,
                magic_code,
            )

        step1 = await adapter.send("Hello")
        step2 = await step1.assert_reply(inspector)
        step3 = await step2.send(magic_code)
        await step3.assert_reply("Logged in.")

    async def test_oauth_prompt_doesnt_detect_code_in_begin_dialog(self):
        connection_name = "myConnection"
        token = "abc123"
        magic_code = "888999"

        async def exec_test(turn_context: TurnContext):
            # Add a magic code to the adapter preemptively so that we can test if the message that triggers
            # BeginDialogAsync uses magic code detection
            adapter.add_user_token(
                connection_name,
                turn_context.activity.channel_id,
                turn_context.activity.from_property.id,
                token,
                magic_code,
            )

            dialog_context = await dialogs.create_context(turn_context)

            results = await dialog_context.continue_dialog()
            if results.status == DialogTurnStatus.Empty:

                # If magicCode is detected when prompting, this will end the dialog and return the token in tokenResult
                token_result = await dialog_context.prompt("prompt", PromptOptions())
                if isinstance(token_result.result, TokenResponse):
                    self.assertTrue(False)  # pylint: disable=redundant-unittest-assert

            await convo_state.save_changes(turn_context)

        # Initialize TestAdapter.
        adapter = TestAdapter(exec_test)

        # Create ConversationState with MemoryStorage and register the state as middleware.
        convo_state = ConversationState(MemoryStorage())

        # Create a DialogState property, DialogSet and AttachmentPrompt.
        dialog_state = convo_state.create_property("dialog_state")
        dialogs = DialogSet(dialog_state)
        dialogs.add(
            OAuthPrompt(
                "prompt", OAuthPromptSettings(connection_name, "Login", None, 300000)
            )
        )

        def inspector(
            activity: Activity, description: str = None
        ):  # pylint: disable=unused-argument
            assert len(activity.attachments) == 1
            assert (
                activity.attachments[0].content_type
                == CardFactory.content_types.oauth_card
            )

        step1 = await adapter.send(magic_code)
        await step1.assert_reply(inspector)

    async def test_should_add_accepting_input_hint_oauth_prompt(self):
        connection_name = "myConnection"
        called = False

        async def callback_handler(turn_context: TurnContext):
            nonlocal called
            dialog_context = await dialogs.create_context(turn_context)

            await dialog_context.continue_dialog()
            await dialog_context.prompt(
                "prompt", PromptOptions(prompt=Activity(), retry_prompt=Activity())
            )

            self.assertTrue(
                dialog_context.active_dialog.state["options"].prompt.input_hint
                == InputHints.accepting_input
            )
            self.assertTrue(
                dialog_context.active_dialog.state["options"].retry_prompt.input_hint
                == InputHints.accepting_input
            )

            await convo_state.save_changes(turn_context)
            called = True

        # Initialize TestAdapter.
        adapter = TestAdapter(callback_handler)

        # Create ConversationState with MemoryStorage and register the state as middleware.
        convo_state = ConversationState(MemoryStorage())

        # Create a DialogState property, DialogSet and AttachmentPrompt.
        dialog_state = convo_state.create_property("dialogState")
        dialogs = DialogSet(dialog_state)
        dialogs.add(
            OAuthPrompt(
                "prompt", OAuthPromptSettings(connection_name, "Login", None, 300000)
            )
        )

        await adapter.send("Hello")
        self.assertTrue(called)
