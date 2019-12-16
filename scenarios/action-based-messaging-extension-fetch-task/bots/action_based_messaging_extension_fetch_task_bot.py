# Copyright (c) Microsoft Corp. All rights reserved.
# Licensed under the MIT License.

from typing import List
import random
from botbuilder.core import (
    CardFactory,
    MessageFactory,
    TurnContext,
)
from botbuilder.schema import Attachment
from botbuilder.schema.teams import (
    MessagingExtensionAction,
    MessagingExtensionActionResponse,
    TaskModuleContinueResponse,
    MessagingExtensionResult,
    TaskModuleTaskInfo,
)
from botbuilder.core.teams import TeamsActivityHandler
from example_data import ExampleData


class ActionBasedMessagingExtensionFetchTaskBot(TeamsActivityHandler):
    async def on_message_activity(self, turn_context: TurnContext):
        value = turn_context.activity.value
        if value is not None:
            # This was a message from the card.
            answer = value["Answer"]
            choices = value["Choices"]
            reply = MessageFactory.text(
                f"{turn_context.activity.from_property.name} answered '{answer}' and chose '{choices}'."
            )
            await turn_context.send_activity(reply)
        else:
            # This is a regular text message.
            reply = MessageFactory.text(
                "Hello from ActionBasedMessagingExtensionFetchTaskBot."
            )
            await turn_context.send_activity(reply)

    async def on_teams_messaging_extension_fetch_task(
        self, turn_context: TurnContext, action: MessagingExtensionAction
    ) -> MessagingExtensionActionResponse:
        card = self._create_adaptive_card_editor()
        task_info = TaskModuleTaskInfo(
            card=card, height=450, title="Task Module Fetch Example", width=500
        )
        continue_response = TaskModuleContinueResponse(type="continue", value=task_info)
        return MessagingExtensionActionResponse(task=continue_response)

    async def on_teams_messaging_extension_submit_action(  # pylint: disable=unused-argument
        self, turn_context: TurnContext, action: MessagingExtensionAction
    ) -> MessagingExtensionActionResponse:
        question = action.data["Question"]
        multi_select = action.data["MultiSelect"]
        option1 = action.data["Option1"]
        option2 = action.data["Option2"]
        option3 = action.data["Option3"]
        preview_card = self._create_adaptive_card_preview(
            user_text=question,
            is_multi_select=multi_select,
            option1=option1,
            option2=option2,
            option3=option3,
        )

        extension_result = MessagingExtensionResult(
            type="botMessagePreview",
            activity_preview=MessageFactory.attachment(preview_card),
        )
        return MessagingExtensionActionResponse(compose_extension=extension_result)

    async def on_teams_messaging_extension_bot_message_preview_edit(  # pylint: disable=unused-argument
        self, turn_context: TurnContext, action: MessagingExtensionAction
    ) -> MessagingExtensionActionResponse:
        activity_preview = action.bot_activity_preview[0]
        content = activity_preview.attachments[0].content
        data = self._get_example_data(content)
        card = self._create_adaptive_card_editor(
            data.question,
            data.is_multi_select,
            data.option1,
            data.option2,
            data.option3,
        )
        task_info = TaskModuleTaskInfo(
            card=card, height=450, title="Task Module Fetch Example", width=500
        )
        continue_response = TaskModuleContinueResponse(type="continue", value=task_info)
        return MessagingExtensionActionResponse(task=continue_response)

    async def on_teams_messaging_extension_bot_message_preview_send(  # pylint: disable=unused-argument
        self, turn_context: TurnContext, action: MessagingExtensionAction
    ) -> MessagingExtensionActionResponse:
        activity_preview = action.bot_activity_preview[0]
        content = activity_preview.attachments[0].content
        data = self._get_example_data(content)
        card = self._create_adaptive_card_preview(
            data.question,
            data.is_multi_select,
            data.option1,
            data.option2,
            data.option3,
        )
        message = MessageFactory.attachment(card)
        await turn_context.send_activity(message)

    def _get_example_data(self, content: dict) -> ExampleData:
        body = content["body"]
        question = body[1]["text"]
        choice_set = body[3]
        multi_select = "isMultiSelect" in choice_set
        option1 = choice_set["choices"][0]["value"]
        option2 = choice_set["choices"][1]["value"]
        option3 = choice_set["choices"][2]["value"]
        return ExampleData(question, multi_select, option1, option2, option3)

    def _create_adaptive_card_editor(
        self,
        user_text: str = None,
        is_multi_select: bool = False,
        option1: str = None,
        option2: str = None,
        option3: str = None,
    ) -> Attachment:
        return CardFactory.adaptive_card(
            {
                "actions": [
                    {
                        "data": {"submitLocation": "messagingExtensionFetchTask"},
                        "title": "Submit",
                        "type": "Action.Submit",
                    }
                ],
                "body": [
                    {
                        "text": "This is an Adaptive Card within a Task Module",
                        "type": "TextBlock",
                        "weight": "bolder",
                    },
                    {"type": "TextBlock", "text": "Enter text for Question:"},
                    {
                        "id": "Question",
                        "placeholder": "Question text here",
                        "type": "Input.Text",
                        "value": user_text,
                    },
                    {"type": "TextBlock", "text": "Options for Question:"},
                    {"type": "TextBlock", "text": "Is Multi-Select:"},
                    {
                        "choices": [
                            {"title": "True", "value": "true"},
                            {"title": "False", "value": "false"},
                        ],
                        "id": "MultiSelect",
                        "isMultiSelect": "false",
                        "style": "expanded",
                        "type": "Input.ChoiceSet",
                        "value": "true" if is_multi_select else "false",
                    },
                    {
                        "id": "Option1",
                        "placeholder": "Option 1 here",
                        "type": "Input.Text",
                        "value": option1,
                    },
                    {
                        "id": "Option2",
                        "placeholder": "Option 2 here",
                        "type": "Input.Text",
                        "value": option2,
                    },
                    {
                        "id": "Option3",
                        "placeholder": "Option 3 here",
                        "type": "Input.Text",
                        "value": option3,
                    },
                ],
                "type": "AdaptiveCard",
                "version": "1.0",
            }
        )

    def _create_adaptive_card_preview(
        self,
        user_text: str = None,
        is_multi_select: bool = False,
        option1: str = None,
        option2: str = None,
        option3: str = None,
    ) -> Attachment:
        return CardFactory.adaptive_card(
            {
                "actions": [
                    {
                        "type": "Action.Submit",
                        "title": "Submit",
                        "data": {"submitLocation": "messagingExtensionSubmit"},
                    }
                ],
                "body": [
                    {
                        "text": "Adaptive Card from Task Module",
                        "type": "TextBlock",
                        "weight": "bolder",
                    },
                    {"text": user_text, "type": "TextBlock", "id": "Question"},
                    {
                        "id": "Answer",
                        "placeholder": "Answer here...",
                        "type": "Input.Text",
                    },
                    {
                        "choices": [
                            {"title": option1, "value": option1},
                            {"title": option2, "value": option2},
                            {"title": option3, "value": option3},
                        ],
                        "id": "Choices",
                        "isMultiSelect": is_multi_select,
                        "style": "expanded",
                        "type": "Input.ChoiceSet",
                    },
                ],
                "type": "AdaptiveCard",
                "version": "1.0",
            }
        )
