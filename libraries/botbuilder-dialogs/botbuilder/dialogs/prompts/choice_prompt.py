# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import Callable, Dict, List

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
from .prompt_culture_models import PromptCultureModels
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
        c.locale: ChoiceFactoryOptions(
            inline_separator=c.separator,
            inline_or=c.inline_or_more,
            inline_or_more=c.inline_or_more,
            include_numbers=True,
        )
        for c in PromptCultureModels.get_supported_cultures()
    }

    def __init__(
        self,
        dialog_id: str,
        validator: Callable[[PromptValidatorContext], bool] = None,
        default_locale: str = None,
        choice_defaults: Dict[str, ChoiceFactoryOptions] = None,
    ):
        """
        :param dialog_id: Unique ID of the dialog within its parent `DialogSet`.
        :param validator: (Optional) validator that will be called each time the user responds to the prompt.
            If the validator replies with a message no additional retry prompt will be sent.
        :param default_locale: (Optional) locale to use if `dc.context.activity.locale` not specified.
            Defaults to a value of `en-us`.
        :param choice_defaults: (Optional) Overrides the dictionary of
            Bot Framework SDK-supported _default_choice_options.
            As type Dict[str, ChoiceFactoryOptions], the key is a string of the locale, such as "en-us".
            *  Must be passed in to each ConfirmPrompt that needs the custom choice defaults.
        """
        super().__init__(dialog_id, validator)

        self.style = ListStyle.auto
        self.default_locale = default_locale
        self.choice_options: ChoiceFactoryOptions = None
        self.recognizer_options: FindChoicesOptions = None

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
            raise TypeError("ChoicePrompt.on_prompt(): turn_context cannot be None.")

        if not options:
            raise TypeError("ChoicePrompt.on_prompt(): options cannot be None.")

        # Determine culture
        culture = self._determine_culture(turn_context.activity)

        # Format prompt to send
        choices: List[Choice] = options.choices if options.choices else []
        channel_id: str = turn_context.activity.channel_id
        choice_options: ChoiceFactoryOptions = (
            self.choice_options
            if self.choice_options
            else self._default_choice_options[culture]
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
            opt: FindChoicesOptions = (
                self.recognizer_options
                if self.recognizer_options
                else FindChoicesOptions()
            )
            opt.locale = self._determine_culture(turn_context.activity, opt)
            results = ChoiceRecognizers.recognize_choices(utterance, choices, opt)

            if results is not None and results:
                result.succeeded = True
                result.value = results[0].resolution

        return result

    def _determine_culture(
        self, activity: Activity, opt: FindChoicesOptions = FindChoicesOptions()
    ) -> str:
        culture = (
            PromptCultureModels.map_to_nearest_language(activity.locale)
            or opt.locale
            or self.default_locale
            or PromptCultureModels.English.locale
        )
        if not culture or not self._default_choice_options.get(culture):
            culture = PromptCultureModels.English.locale

        return culture
