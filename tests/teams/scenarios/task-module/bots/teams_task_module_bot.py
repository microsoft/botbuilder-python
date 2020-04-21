# Copyright (c) Microsoft Corp. All rights reserved.
# Licensed under the MIT License.

import json
from typing import List
import random
from botbuilder.core import CardFactory, MessageFactory, TurnContext
from botbuilder.schema import (
    ChannelAccount,
    HeroCard,
    CardAction,
    CardImage,
    Attachment,
)
from botbuilder.schema.teams import (
    MessagingExtensionAction,
    MessagingExtensionActionResponse,
    MessagingExtensionAttachment,
    MessagingExtensionResult,
    TaskModuleResponse,
    TaskModuleResponseBase,
    TaskModuleContinueResponse,
    TaskModuleMessageResponse,
    TaskModuleTaskInfo,
    TaskModuleRequest,
)
from botbuilder.core.teams import TeamsActivityHandler, TeamsInfo
from botbuilder.azure import CosmosDbPartitionedStorage
from botbuilder.core.teams.teams_helper import deserializer_helper

class TaskModuleBot(TeamsActivityHandler):
    async def on_message_activity(self, turn_context: TurnContext):
        reply = MessageFactory.attachment(self._get_task_module_hero_card())
        await turn_context.send_activity(reply)

    def _get_task_module_hero_card(self) -> Attachment:
        task_module_action = CardAction(
            type="invoke",
            title="Adaptive Card",
            value={"type": "task/fetch", "data": "adaptivecard"},
        )
        card = HeroCard(
            title="Task Module Invocation from Hero Card",
            subtitle="This is a hero card with a Task Module Action button.  Click the button to show an Adaptive Card within a Task Module.",
            buttons=[task_module_action],
        )
        return CardFactory.hero_card(card)

    async def on_teams_task_module_fetch(
        self, turn_context: TurnContext, task_module_request: TaskModuleRequest
    ) -> TaskModuleResponse:
        reply = MessageFactory.text(
            f"OnTeamsTaskModuleFetchAsync TaskModuleRequest: {json.dumps(task_module_request.data)}"
        )
        await turn_context.send_activity(reply)

        # base_response = TaskModuleResponseBase(type='continue')
        card = CardFactory.adaptive_card(
            {
                "version": "1.0.0",
                "type": "AdaptiveCard",
                "body": [
                    {"type": "TextBlock", "text": "Enter Text Here",},
                    {
                        "type": "Input.Text",
                        "id": "usertext",
                        "placeholder": "add some text and submit",
                        "IsMultiline": "true",
                    },
                ],
                "actions": [{"type": "Action.Submit", "title": "Submit",}],
            }
        )

        task_info = TaskModuleTaskInfo(
            card=card, title="Adaptive Card: Inputs", height=200, width=400
        )
        continue_response = TaskModuleContinueResponse(type="continue", value=task_info)
        return TaskModuleResponse(task=continue_response)

    async def on_teams_task_module_submit(
         self, turn_context: TurnContext, task_module_request: TaskModuleRequest
    ) -> TaskModuleResponse:
        reply = MessageFactory.text(
            f"on_teams_messaging_extension_submit_action_activity MessagingExtensionAction: {json.dumps(task_module_request.data)}"
        )
        await turn_context.send_activity(reply)

        message_response = TaskModuleMessageResponse(type="message", value="Thanks!")
        return TaskModuleResponse(task=message_response)
