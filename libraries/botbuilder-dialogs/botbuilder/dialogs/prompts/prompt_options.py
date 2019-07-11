# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import List

from botbuilder.schema import Activity
from botbuilder.dialogs.choices import Choice, ListStyle


class PromptOptions:
    def __init__(
        self,
        prompt: Activity = None,
        retry_prompt: Activity = None,
        choices: List[Choice] = None,
        style: ListStyle = None,
        validations: object = None,
        number_of_attempts: int = 0,
    ):
        self.prompt = prompt
        self.retry_prompt = retry_prompt
        self.choices = choices
        self.style = style
        self.validations = validations
        self.number_of_attempts = number_of_attempts
