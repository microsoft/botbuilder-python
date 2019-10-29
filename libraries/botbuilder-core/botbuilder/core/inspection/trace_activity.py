# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from datetime import datetime
from typing import Dict, Union

from botbuilder.core import BotState
from botbuilder.schema import Activity, ActivityTypes, ConversationReference


def make_command_activity(command: str) -> Activity:
    return Activity(
        type=ActivityTypes.trace,
        timestamp=datetime.utcnow(),
        name="Command",
        label="Command",
        value=command,
        value_type="https://www.botframework.com/schemas/command",
    )


def from_activity(activity: Activity, name: str, label: str) -> Activity:
    return Activity(
        type=ActivityTypes.trace,
        timestamp=datetime.utcnow(),
        name=name,
        label=label,
        value=activity,
        value_type="https://www.botframework.com/schemas/activity",
    )


def from_state(bot_state: Union[BotState, Dict]) -> Activity:
    return Activity(
        type=ActivityTypes.trace,
        timestamp=datetime.utcnow(),
        name="Bot State",
        label="BotState",
        value=bot_state,
        value_type="https://www.botframework.com/schemas/botState",
    )


def from_conversation_reference(
    conversation_reference: ConversationReference,
) -> Activity:
    return Activity(
        type=ActivityTypes.trace,
        timestamp=datetime.utcnow(),
        name="Deleted Message",
        label="MessageDelete",
        value=conversation_reference,
        value_type="https://www.botframework.com/schemas/conversationReference",
    )


def from_error(error_message: str) -> Activity:
    return Activity(
        type=ActivityTypes.trace,
        timestamp=datetime.utcnow(),
        name="Turn Error",
        label="TurnError",
        value=error_message,
        value_type="https://www.botframework.com/schemas/error",
    )
