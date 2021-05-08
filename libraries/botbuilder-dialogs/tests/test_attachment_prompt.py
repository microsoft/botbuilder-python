# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import copy
import aiounittest
from botbuilder.dialogs.prompts import (
    AttachmentPrompt,
    PromptOptions,
    PromptValidatorContext,
)
from botbuilder.schema import Activity, ActivityTypes, Attachment, InputHints

from botbuilder.core import (
    TurnContext,
    ConversationState,
    MemoryStorage,
    MessageFactory,
)
from botbuilder.core.adapters import TestAdapter
from botbuilder.dialogs import DialogSet, DialogTurnStatus


class AttachmentPromptTests(aiounittest.AsyncTestCase):
    def test_attachment_prompt_with_empty_id_should_fail(self):
        empty_id = ""

        with self.assertRaises(TypeError):
            AttachmentPrompt(empty_id)

    def test_attachment_prompt_with_none_id_should_fail(self):
        with self.assertRaises(TypeError):
            AttachmentPrompt(None)

    async def test_basic_attachment_prompt(self):
        async def exec_test(turn_context: TurnContext):
            dialog_context = await dialogs.create_context(turn_context)

            results = await dialog_context.continue_dialog()
            if results.status == DialogTurnStatus.Empty:
                options = PromptOptions(
                    prompt=Activity(
                        type=ActivityTypes.message, text="please add an attachment."
                    )
                )
                await dialog_context.prompt("AttachmentPrompt", options)
            elif results.status == DialogTurnStatus.Complete:
                attachment = results.result[0]
                content = MessageFactory.text(attachment.content)
                await turn_context.send_activity(content)

            await convo_state.save_changes(turn_context)

        # Initialize TestAdapter.
        adapter = TestAdapter(exec_test)

        # Create ConversationState with MemoryStorage and register the state as middleware.
        convo_state = ConversationState(MemoryStorage())

        # Create a DialogState property, DialogSet and AttachmentPrompt.
        dialog_state = convo_state.create_property("dialog_state")
        dialogs = DialogSet(dialog_state)
        dialogs.add(AttachmentPrompt("AttachmentPrompt"))

        # Create incoming activity with attachment.
        attachment = Attachment(content="some content", content_type="text/plain")
        attachment_activity = Activity(
            type=ActivityTypes.message, attachments=[attachment]
        )

        step1 = await adapter.send("hello")
        step2 = await step1.assert_reply("please add an attachment.")
        step3 = await step2.send(attachment_activity)
        await step3.assert_reply("some content")

    async def test_attachment_prompt_with_input_hint(self):
        prompt_activity = Activity(
            type=ActivityTypes.message,
            text="please add an attachment.",
            input_hint=InputHints.accepting_input,
        )

        async def exec_test(turn_context: TurnContext):
            dialog_context = await dialogs.create_context(turn_context)

            results = await dialog_context.continue_dialog()

            if results.status == DialogTurnStatus.Empty:
                options = PromptOptions(prompt=copy.copy(prompt_activity))
                await dialog_context.prompt("AttachmentPrompt", options)
            elif results.status == DialogTurnStatus.Complete:
                attachment = results.result[0]
                content = MessageFactory.text(attachment.content)
                await turn_context.send_activity(content)

            await convo_state.save_changes(turn_context)

        # Initialize TestAdapter.
        adapter = TestAdapter(exec_test)

        # Create ConversationState with MemoryStorage and register the state as middleware.
        convo_state = ConversationState(MemoryStorage())

        # Create a DialogState property, DialogSet and AttachmentPrompt.
        dialog_state = convo_state.create_property("dialog_state")
        dialogs = DialogSet(dialog_state)
        dialogs.add(AttachmentPrompt("AttachmentPrompt"))

        step1 = await adapter.send("hello")
        await step1.assert_reply(prompt_activity)

    async def test_attachment_prompt_with_validator(self):
        async def exec_test(turn_context: TurnContext):
            dialog_context = await dialogs.create_context(turn_context)

            results = await dialog_context.continue_dialog()
            if results.status == DialogTurnStatus.Empty:
                options = PromptOptions(
                    prompt=Activity(
                        type=ActivityTypes.message, text="please add an attachment."
                    )
                )
                await dialog_context.prompt("AttachmentPrompt", options)
            elif results.status == DialogTurnStatus.Complete:
                attachment = results.result[0]
                content = MessageFactory.text(attachment.content)
                await turn_context.send_activity(content)

            await convo_state.save_changes(turn_context)

        # Initialize TestAdapter.
        adapter = TestAdapter(exec_test)

        # Create ConversationState with MemoryStorage and register the state as middleware.
        convo_state = ConversationState(MemoryStorage())

        # Create a DialogState property, DialogSet and AttachmentPrompt.
        dialog_state = convo_state.create_property("dialog_state")
        dialogs = DialogSet(dialog_state)

        async def aux_validator(prompt_context: PromptValidatorContext):
            assert prompt_context, "Validator missing prompt_context"
            return prompt_context.recognized.succeeded

        dialogs.add(AttachmentPrompt("AttachmentPrompt", aux_validator))

        # Create incoming activity with attachment.
        attachment = Attachment(content="some content", content_type="text/plain")
        attachment_activity = Activity(
            type=ActivityTypes.message, attachments=[attachment]
        )

        step1 = await adapter.send("hello")
        step2 = await step1.assert_reply("please add an attachment.")
        step3 = await step2.send(attachment_activity)
        await step3.assert_reply("some content")

    async def test_retry_attachment_prompt(self):
        async def exec_test(turn_context: TurnContext):
            dialog_context = await dialogs.create_context(turn_context)

            results = await dialog_context.continue_dialog()
            if results.status == DialogTurnStatus.Empty:
                options = PromptOptions(
                    prompt=Activity(
                        type=ActivityTypes.message, text="please add an attachment."
                    )
                )
                await dialog_context.prompt("AttachmentPrompt", options)
            elif results.status == DialogTurnStatus.Complete:
                attachment = results.result[0]
                content = MessageFactory.text(attachment.content)
                await turn_context.send_activity(content)

            await convo_state.save_changes(turn_context)

        # Initialize TestAdapter.
        adapter = TestAdapter(exec_test)

        # Create ConversationState with MemoryStorage and register the state as middleware.
        convo_state = ConversationState(MemoryStorage())

        # Create a DialogState property, DialogSet and AttachmentPrompt.
        dialog_state = convo_state.create_property("dialog_state")
        dialogs = DialogSet(dialog_state)
        dialogs.add(AttachmentPrompt("AttachmentPrompt"))

        # Create incoming activity with attachment.
        attachment = Attachment(content="some content", content_type="text/plain")
        attachment_activity = Activity(
            type=ActivityTypes.message, attachments=[attachment]
        )

        step1 = await adapter.send("hello")
        step2 = await step1.assert_reply("please add an attachment.")
        step3 = await step2.send("hello again")
        step4 = await step3.assert_reply("please add an attachment.")
        step5 = await step4.send(attachment_activity)
        await step5.assert_reply("some content")

    async def test_attachment_prompt_with_custom_retry(self):
        async def exec_test(turn_context: TurnContext):
            dialog_context = await dialogs.create_context(turn_context)

            results = await dialog_context.continue_dialog()
            if results.status == DialogTurnStatus.Empty:
                options = PromptOptions(
                    prompt=Activity(
                        type=ActivityTypes.message, text="please add an attachment."
                    ),
                    retry_prompt=Activity(
                        type=ActivityTypes.message, text="please try again."
                    ),
                )
                await dialog_context.prompt("AttachmentPrompt", options)
            elif results.status == DialogTurnStatus.Complete:
                attachment = results.result[0]
                content = MessageFactory.text(attachment.content)
                await turn_context.send_activity(content)

            await convo_state.save_changes(turn_context)

        # Initialize TestAdapter.
        adapter = TestAdapter(exec_test)

        # Create ConversationState with MemoryStorage and register the state as middleware.
        convo_state = ConversationState(MemoryStorage())

        # Create a DialogState property, DialogSet and AttachmentPrompt.
        dialog_state = convo_state.create_property("dialog_state")
        dialogs = DialogSet(dialog_state)

        async def aux_validator(prompt_context: PromptValidatorContext):
            assert prompt_context, "Validator missing prompt_context"
            return prompt_context.recognized.succeeded

        dialogs.add(AttachmentPrompt("AttachmentPrompt", aux_validator))

        # Create incoming activity with attachment.
        attachment = Attachment(content="some content", content_type="text/plain")
        attachment_activity = Activity(
            type=ActivityTypes.message, attachments=[attachment]
        )
        invalid_activty = Activity(type=ActivityTypes.message, text="invalid")

        step1 = await adapter.send("hello")
        step2 = await step1.assert_reply("please add an attachment.")
        step3 = await step2.send(invalid_activty)
        step4 = await step3.assert_reply("please try again.")
        step5 = await step4.send(attachment_activity)
        await step5.assert_reply("some content")

    async def test_should_send_ignore_retry_rompt_if_validator_replies(self):
        async def exec_test(turn_context: TurnContext):
            dialog_context = await dialogs.create_context(turn_context)

            results = await dialog_context.continue_dialog()
            if results.status == DialogTurnStatus.Empty:
                options = PromptOptions(
                    prompt=Activity(
                        type=ActivityTypes.message, text="please add an attachment."
                    ),
                    retry_prompt=Activity(
                        type=ActivityTypes.message, text="please try again."
                    ),
                )
                await dialog_context.prompt("AttachmentPrompt", options)
            elif results.status == DialogTurnStatus.Complete:
                attachment = results.result[0]
                content = MessageFactory.text(attachment.content)
                await turn_context.send_activity(content)

            await convo_state.save_changes(turn_context)

        # Initialize TestAdapter.
        adapter = TestAdapter(exec_test)

        # Create ConversationState with MemoryStorage and register the state as middleware.
        convo_state = ConversationState(MemoryStorage())

        # Create a DialogState property, DialogSet and AttachmentPrompt.
        dialog_state = convo_state.create_property("dialog_state")
        dialogs = DialogSet(dialog_state)

        async def aux_validator(prompt_context: PromptValidatorContext):
            assert prompt_context, "Validator missing prompt_context"

            if not prompt_context.recognized.succeeded:
                await prompt_context.context.send_activity("Bad input.")

            return prompt_context.recognized.succeeded

        dialogs.add(AttachmentPrompt("AttachmentPrompt", aux_validator))

        # Create incoming activity with attachment.
        attachment = Attachment(content="some content", content_type="text/plain")
        attachment_activity = Activity(
            type=ActivityTypes.message, attachments=[attachment]
        )
        invalid_activty = Activity(type=ActivityTypes.message, text="invalid")

        step1 = await adapter.send("hello")
        step2 = await step1.assert_reply("please add an attachment.")
        step3 = await step2.send(invalid_activty)
        step4 = await step3.assert_reply("Bad input.")
        step5 = await step4.send(attachment_activity)
        await step5.assert_reply("some content")

    async def test_should_not_send_retry_if_not_specified(self):
        async def exec_test(turn_context: TurnContext):
            dialog_context = await dialogs.create_context(turn_context)

            results = await dialog_context.continue_dialog()
            if results.status == DialogTurnStatus.Empty:
                await dialog_context.begin_dialog("AttachmentPrompt", PromptOptions())
            elif results.status == DialogTurnStatus.Complete:
                attachment = results.result[0]
                content = MessageFactory.text(attachment.content)
                await turn_context.send_activity(content)

            await convo_state.save_changes(turn_context)

        # Initialize TestAdapter.
        adapter = TestAdapter(exec_test)

        # Create ConversationState with MemoryStorage and register the state as middleware.
        convo_state = ConversationState(MemoryStorage())

        # Create a DialogState property, DialogSet and AttachmentPrompt.
        dialog_state = convo_state.create_property("dialog_state")
        dialogs = DialogSet(dialog_state)
        dialogs.add(AttachmentPrompt("AttachmentPrompt"))

        # Create incoming activity with attachment.
        attachment = Attachment(content="some content", content_type="text/plain")
        attachment_activity = Activity(
            type=ActivityTypes.message, attachments=[attachment]
        )

        step1 = await adapter.send("hello")
        step2 = await step1.send("what?")
        step3 = await step2.send(attachment_activity)
        await step3.assert_reply("some content")
