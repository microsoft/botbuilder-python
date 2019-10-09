# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from enum import Enum
from inspect import getmembers
from typing import List

from msrest.serialization import Model

import botbuilder.schema as schema
from botbuilder.schema import Activity
from botbuilder.dialogs.choices import Choice, ListStyle
from botbuilder.core import BotState


class PromptOptions(Model):
    _attribute_map = {
        "prompt": {"key": "prompt", "type": "Activity"},
        "retry_prompt": {"key": "retryPrompt", "type": "Activity"},
        "choices": {"key": "choices", "type": "[Choice]"},
        "style": {"key": "style", "type": "int"},
        "number_of_attempts": {"key": "numberOfAttempts", "type": "int"},
    }

    def __init__(
        self,
        prompt: Activity = None,
        retry_prompt: Activity = None,
        choices: List[Choice] = None,
        style: ListStyle = None,
        validations: object = None,
        number_of_attempts: int = 0,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.prompt = prompt
        self.retry_prompt = retry_prompt
        self.choices = choices
        self.style = style
        self.validations = validations
        self.number_of_attempts = number_of_attempts


BotState.register_msrest_deserializer(
    PromptOptions,
    dependencies=[
        schema_cls
        for key, schema_cls
        in getmembers(schema)
        if isinstance(schema_cls, type) and issubclass(schema_cls, (Model, Enum))
    ] + [Choice, ListStyle]
)
