# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import Dict
from recognizers_choice import recognize_boolean
from botbuilder.core.turn_context import TurnContext
from botbuilder.schema import ActivityTypes, Activity
from botbuilder.dialogs.choices import (
    Choice,
    ChoiceFactoryOptions,
    ChoiceRecognizers,
    ListStyle,
)
from .prompt import Prompt
from .prompt_culture_models import PromptCultureModels
from .prompt_options import PromptOptions
from .prompt_recognizer_result import PromptRecognizerResult


class ConfirmPrompt(Prompt):
    _default_choice_options: Dict[str, object] = {
        c.locale: (
            Choice(c.yes_in_language),
            Choice(c.no_in_language),
            ChoiceFactoryOptions(c.separator, c.inline_or, c.inline_or_more, True),
        )
        for c in PromptCultureModels.get_supported_cultures()
    }

    # TODO: PromptValidator
    def __init__(
        self,
        dialog_id: str,
        validator: object = None,
        default_locale: str = None,
        choice_defaults: Dict[str, object] = None,
    ):
        super().__init__(dialog_id, validator)
        if dialog_id is None:
            raise TypeError("ConfirmPrompt(): dialog_id cannot be None.")
        # TODO: Port ListStyle
        self.style = ListStyle.auto
        # TODO: Import defaultLocale
        self.default_locale = default_locale
        self.choice_options = None
        self.confirm_choices = None

        if choice_defaults is not None:
            self._default_choice_options = choice_defaults

    async def on_prompt(
        self,
        turn_context: TurnContext,
        state: Dict[str, object],
        options: PromptOptions,
        is_retry: bool,
    ):
        if not turn_context:
            raise TypeError("ConfirmPrompt.on_prompt(): turn_context cannot be None.")
        if not options:
            raise TypeError("ConfirmPrompt.on_prompt(): options cannot be None.")

        # Format prompt to send
        channel_id = turn_context.activity.channel_id
        culture = self._determine_culture(turn_context.activity)
        defaults = self._default_choice_options[culture]
        choice_opts = (
            self.choice_options if self.choice_options is not None else defaults[2]
        )
        confirms = (
            self.confirm_choices
            if self.confirm_choices is not None
            else (defaults[0], defaults[1])
        )
        choices = [confirms[0], confirms[1]]
        if is_retry and options.retry_prompt is not None:
            prompt = self.append_choices(
                options.retry_prompt, channel_id, choices, self.style, choice_opts
            )
        else:
            prompt = self.append_choices(
                options.prompt, channel_id, choices, self.style, choice_opts
            )
        await turn_context.send_activity(prompt)

    async def on_recognize(
        self,
        turn_context: TurnContext,
        state: Dict[str, object],
        options: PromptOptions,
    ) -> PromptRecognizerResult:
        if not turn_context:
            raise TypeError("ConfirmPrompt.on_prompt(): turn_context cannot be None.")

        result = PromptRecognizerResult()
        if turn_context.activity.type == ActivityTypes.message:
            # Recognize utterance
            utterance = turn_context.activity.text
            if not utterance:
                return result
            culture = self._determine_culture(turn_context.activity)
            results = recognize_boolean(utterance, culture)
            if results:
                first = results[0]
                if "value" in first.resolution:
                    result.succeeded = True
                    result.value = first.resolution["value"]
            else:
                # First check whether the prompt was sent to the user with numbers
                # if it was we should recognize numbers
                defaults = self._default_choice_options[culture]
                opts = (
                    self.choice_options
                    if self.choice_options is not None
                    else defaults[2]
                )

                # This logic reflects the fact that IncludeNumbers is nullable and True is the default set in
                # Inline style
                if opts.include_numbers is None or opts.include_numbers:
                    # The text may be a number in which case we will interpret that as a choice.
                    confirm_choices = (
                        self.confirm_choices
                        if self.confirm_choices is not None
                        else (defaults[0], defaults[1])
                    )
                    choices = {confirm_choices[0], confirm_choices[1]}
                    second_attempt_results = ChoiceRecognizers.recognize_choices(
                        utterance, choices
                    )
                    if second_attempt_results:
                        result.succeeded = True
                        result.value = second_attempt_results[0].resolution.index == 0

        return result

    def _determine_culture(self, activity: Activity) -> str:
        culture = (
            PromptCultureModels.map_to_nearest_language(activity.locale)
            or self.default_locale
            or PromptCultureModels.English.locale
        )
        if not culture or not self._default_choice_options.get(culture):
            culture = PromptCultureModels.English.locale

        return culture
