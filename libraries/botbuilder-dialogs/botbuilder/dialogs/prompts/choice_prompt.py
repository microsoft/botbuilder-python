# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import Callable, Dict, List, Union

from recognizers_text import Culture
from botbuilder.core import TurnContext
from botbuilder.dialogs.choices import (
    Choice,
    ChoiceFactoryOptions,
    ChoiceRecognizers,
    FindChoicesOptions,
    ListStyle,
)
from botbuilder.schema import Activity, ActivityTypes

from .prompt import Prompt
from .prompt_options import PromptOptions
from .prompt_validator_context import PromptValidatorContext
from .prompt_recognizer_result import PromptRecognizerResult


class ChoicePrompt(Prompt):
    """
    Prompts a user to select from a list of choices.

    By default the prompt will return to the calling dialog a `FoundChoice` object containing the choice that
     was selected.
    """

    _default_choice_options: Dict[str, ChoiceFactoryOptions] = {
        Culture.Spanish: ChoiceFactoryOptions(
            inline_separator=", ",
            inline_or=" o ",
            inline_or_more=", o ",
            include_numbers=True,
        ),
        Culture.Dutch: ChoiceFactoryOptions(
            inline_separator=", ",
            inline_or=" of ",
            inline_or_more=", of ",
            include_numbers=True,
        ),
        Culture.English: ChoiceFactoryOptions(
            inline_separator=", ",
            inline_or=" or ",
            inline_or_more=", or ",
            include_numbers=True,
        ),
        Culture.French: ChoiceFactoryOptions(
            inline_separator=", ",
            inline_or=" ou ",
            inline_or_more=", ou ",
            include_numbers=True,
        ),
        "de-de": ChoiceFactoryOptions(
            inline_separator=", ",
            inline_or=" oder ",
            inline_or_more=", oder ",
            include_numbers=True,
        ),
        Culture.Japanese: ChoiceFactoryOptions(
            inline_separator="、 ",
            inline_or=" または ",
            inline_or_more="、 または ",
            include_numbers=True,
        ),
        Culture.Portuguese: ChoiceFactoryOptions(
            inline_separator=", ",
            inline_or=" ou ",
            inline_or_more=", ou ",
            include_numbers=True,
        ),
        Culture.Chinese: ChoiceFactoryOptions(
            inline_separator="， ",
            inline_or=" 要么 ",
            inline_or_more="， 要么 ",
            include_numbers=True,
        ),
    }

    def __init__(
        self,
        dialog_id: str,
        validator: Callable[[PromptValidatorContext], bool] = None,
        default_locale: str = None,
    ):
        super().__init__(dialog_id, validator)

        self.style = ListStyle.auto
        self.default_locale = default_locale
        self.choice_options: ChoiceFactoryOptions = None
        self.recognizer_options: FindChoicesOptions = None

    async def on_prompt(
        self,
        turn_context: TurnContext,
        state: Dict[str, object],
        options: PromptOptions,
        is_retry: bool,
    ):
        if not turn_context:
            raise TypeError("ChoicePrompt.on_prompt(): turn_context cannot be None.")

        if not options:
            raise TypeError("ChoicePrompt.on_prompt(): options cannot be None.")

        # Determine culture
        culture: Union[
            str, None
        ] = turn_context.activity.locale if turn_context.activity.locale else self.default_locale

        if not culture or culture not in ChoicePrompt._default_choice_options:
            culture = Culture.English

        # Format prompt to send
        choices: List[Choice] = options.choices if options.choices else []
        channel_id: str = turn_context.activity.channel_id
        choice_options: ChoiceFactoryOptions = (
            self.choice_options
            if self.choice_options
            else ChoicePrompt._default_choice_options[culture]
        )
        choice_style = (
            0 if options.style == 0 else options.style if options.style else self.style
        )

        if is_retry and options.retry_prompt is not None:
            prompt = self.append_choices(
                options.retry_prompt, channel_id, choices, choice_style, choice_options
            )
        else:
            prompt = self.append_choices(
                options.prompt, channel_id, choices, choice_style, choice_options
            )

        # Send prompt
        await turn_context.send_activity(prompt)

    async def on_recognize(
        self,
        turn_context: TurnContext,
        state: Dict[str, object],
        options: PromptOptions,
    ) -> PromptRecognizerResult:
        if not turn_context:
            raise TypeError("ChoicePrompt.on_recognize(): turn_context cannot be None.")

        choices: List[Choice] = options.choices if (options and options.choices) else []
        result: PromptRecognizerResult = PromptRecognizerResult()

        if turn_context.activity.type == ActivityTypes.message:
            activity: Activity = turn_context.activity
            utterance: str = activity.text
            if not utterance:
                return result
            opt: FindChoicesOptions = self.recognizer_options if self.recognizer_options else FindChoicesOptions()
            opt.locale = (
                activity.locale
                if activity.locale
                else (self.default_locale or Culture.English)
            )
            results = ChoiceRecognizers.recognize_choices(utterance, choices, opt)

            if results is not None and results:
                result.succeeded = True
                result.value = results[0].resolution

        return result
