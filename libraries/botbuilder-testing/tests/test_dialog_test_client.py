# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import logging

from aiounittest import AsyncTestCase
from botbuilder.core import MessageFactory
from botbuilder.dialogs import (
    ComponentDialog,
    DialogContext,
    DialogTurnResult,
    DialogTurnStatus,
    PromptOptions,
    TextPrompt,
    WaterfallDialog,
    WaterfallStepContext,
)
from botbuilder.schema import Activity
from botbuilder.testing import DialogTestClient, DialogTestLogger


class DialogTestClientTest(AsyncTestCase):
    """Tests for dialog test client."""

    def __init__(self, *args, **kwargs):
        super(DialogTestClientTest, self).__init__(*args, **kwargs)
        logging.basicConfig(format="", level=logging.INFO)

    def test_init(self):
        client = DialogTestClient(channel_or_adapter="test", target_dialog=None)
        self.assertIsInstance(client, DialogTestClient)

    def test_init_with_custom_channel_id(self):
        client = DialogTestClient(channel_or_adapter="custom", target_dialog=None)
        self.assertEqual("custom", client.test_adapter.template.channel_id)

    async def test_single_turn_waterfall_dialog(self):
        async def step1(step: DialogContext) -> DialogTurnResult:
            await step.context.send_activity("hello")
            return await step.end_dialog()

        dialog = WaterfallDialog("waterfall", [step1])
        client = DialogTestClient("test", dialog)

        reply = await client.send_activity("hello")

        self.assertEqual("hello", reply.text)
        self.assertEqual("test", reply.channel_id)
        self.assertEqual(DialogTurnStatus.Complete, client.dialog_turn_result.status)

    async def test_single_turn_waterfall_dialog_with_logger(self):
        """
        Test for single turn waterfall dialog with logger with test client.
        To view the console output:
        * unittest
          ```bash
          python -m unittest -v -k logger
          ```
        * pytest
          ```bash
          pytest --log-cli-level=INFO --log-format="%(message)s" -k logger
          ```
        The results are similar to:
        ```
        User: Text = hello
        -> ts: 13:39:59

        Bot: Text      = hello
             Speak     = None
             InputHint = acceptingInput
        -> ts: 13:39:59 elapsed 8 ms
        ```

        :return: None
        :rtype: None
        """

        async def step1(step: DialogContext) -> DialogTurnResult:
            await step.context.send_activity("hello")
            return await step.end_dialog()

        dialog = WaterfallDialog("waterfall", [step1])
        client = DialogTestClient(
            "test",
            dialog,
            initial_dialog_options=None,
            middlewares=[DialogTestLogger()],
        )

        reply = await client.send_activity("hello")

        self.assertEqual("hello", reply.text)
        self.assertEqual("test", reply.channel_id)
        self.assertEqual(DialogTurnStatus.Complete, client.dialog_turn_result.status)

    async def test_two_turn_waterfall_dialog(self):
        async def step1(step: WaterfallStepContext) -> DialogTurnResult:
            await step.context.send_activity("hello")
            await step.context.send_activity(Activity(type="typing"))
            return await step.next(result=None)

        async def step2(step: WaterfallStepContext) -> DialogTurnResult:
            await step.context.send_activity("hello 2")
            return await step.end_dialog()

        dialog = WaterfallDialog("waterfall", [step1, step2])
        client = DialogTestClient(
            "test",
            dialog,
            initial_dialog_options=None,
            middlewares=[DialogTestLogger()],
        )

        reply = await client.send_activity("hello")
        self.assertEqual("hello", reply.text)

        reply = client.get_next_reply()
        self.assertEqual("typing", reply.type)

        reply = client.get_next_reply()
        self.assertEqual("hello 2", reply.text)
        self.assertEqual(DialogTurnStatus.Complete, client.dialog_turn_result.status)

    async def test_component_dialog(self):
        component = MainDialog("component")
        client = DialogTestClient(
            "test",
            component,
            initial_dialog_options=None,
            middlewares=[DialogTestLogger()],
        )

        reply = await client.send_activity("hello")

        self.assertEqual("Tell me something", reply.text)
        reply = await client.send_activity("foo")
        self.assertEqual("you said: foo", reply.text)
        self.assertEqual(DialogTurnStatus.Complete, client.dialog_turn_result.status)


class MainDialog(ComponentDialog):
    def __init__(self, dialog_id: str):
        super().__init__(dialog_id)

        dialog = WaterfallDialog("waterfall", [self.step1, self.step2])
        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(dialog)
        self.initial_dialog_id = dialog.id

    @staticmethod
    async def step1(step: WaterfallStepContext) -> DialogTurnResult:
        options = PromptOptions(prompt=MessageFactory.text("Tell me something"))
        return await step.prompt(TextPrompt.__name__, options)

    @staticmethod
    async def step2(step: WaterfallStepContext) -> DialogTurnResult:
        await step.context.send_activity(
            MessageFactory.text(f"you said: {step.result}")
        )
        return await step.end_dialog()
