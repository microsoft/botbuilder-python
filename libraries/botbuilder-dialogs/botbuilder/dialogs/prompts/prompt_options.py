# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import List

from botbuilder.schema import Activity
from botbuilder.dialogs.choices import Choice, ListStyle


class PromptOptions:
    """
    Contains settings to pass to a :class:`Prompt` object when the prompt is started.
    """

    def __init__(
        self,
        prompt: Activity = None,
        retry_prompt: Activity = None,
        choices: List[Choice] = None,
        style: ListStyle = None,
        validations: object = None,
        number_of_attempts: int = 0,
    ):
        """
        Sets the initial prompt to send to the user as an :class:`botbuilder.schema.Activity`.

        :param prompt: The initial prompt to send to the user
        :type prompt: :class:`botbuilder.schema.Activity`
        :param retry_prompt: The retry prompt to send to the user
        :type retry_prompt: :class:`botbuilder.schema.Activity`
        :param choices: The choices to send to the user
        :type choices: :class:`List`
        :param style: The style of the list of choices to send to the user
        :type style: :class:`ListStyle`
        :param validations: The prompt validations
        :type validations: :class:`Object`
        :param number_of_attempts: The number of attempts allowed
        :type number_of_attempts: :class:`int`

        """
        self.prompt = prompt
        self.retry_prompt = retry_prompt
        self.choices = choices
        self.style = style
        self.validations = validations
        self.number_of_attempts = number_of_attempts
