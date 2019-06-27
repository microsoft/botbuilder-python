# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import Callable, Dict, List

from botbuilder.core import TurnContext
from botbuilder.dialogs.choices import Choice, ChoiceFactory, ChoiceFactoryOptions, FindChoicesOptions, ListStyle
from botbuilder.dialogs.prompts import Prompt, PromptOptions, PromptValidatorContext, PromptRecognizerResult
from botbuilder.schema import Activity, ActivityTypes

class ChoicePrompt(Prompt):
    """
    Prompts a user to select froma list of choices.

    By default the prompt will return to the calling dialog a `FoundChoice` object containing the choice that was selected.
    """
    # TODO in C#, Recognizers.Text.Culture (Spanish, Dutch, English, etc.) are used as keys instead of hard-coded strings 'es-es', 'nl-nl', 'en-us', etc.
    _default_choice_options: Dict[str, ChoiceFactoryOptions] = {
        'es-es': ChoiceFactoryOptions(inline_separator = ', ', inline_or = ' o ', include_numbers = True),
        'nl-nl': ChoiceFactoryOptions(inline_separator = ', ', inline_or = ' of ', include_numbers = True),
        'en-us': ChoiceFactoryOptions(inline_separator = ', ', inline_or = ' or ', include_numbers = True),
        'fr-fr': ChoiceFactoryOptions(inline_separator = ', ', inline_or = ' ou ', include_numbers = True),
        'de-de': ChoiceFactoryOptions(inline_separator = ', ', inline_or = ' oder ', include_numbers = True),
        'ja-jp': ChoiceFactoryOptions(inline_separator = '、 ', inline_or = ' または ', include_numbers = True),
        'pt-br': ChoiceFactoryOptions(inline_separator = ', ', inline_or = ' ou ', include_numbers = True),
        'zh-cn': ChoiceFactoryOptions(inline_separator = '， ', inline_or = ' 要么 ', include_numbers = True),
    }

    def __init__(
        self,
        dialog_id: str,
        validator: Callable[[PromptValidatorContext], bool] = None,
        default_locale: str = None
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
        is_retry: bool
    ):
        if not turn_context:
            raise TypeError('ChoicePrompt.on_prompt(): turn_context cannot be None.')
        
        if not options:
            raise TypeError('ChoicePrompt.on_prompt(): options cannot be None.')
        
        # Determine culture
        culture = turn_context.activity.locale if turn_context.activity.locale else self.default_locale
        
        if (not culture or culture not in ChoicePrompt._default_choice_options):
            # TODO replace with recognizers constant
            culture = 'en-us'
        
        # Format prompt to send
        choices: List[Choice] = self.choice_options.choices if self.choice_options.choices else []
        channel_id: str = turn_context.activity.channel_id
        choice_options: ChoiceFactoryOptions = self.choice_options if self.choice_options else ChoicePrompt._default_choice_options[culture]
        choice_style = options.style if options.style else self.style

        if is_retry and options.retry_prompt is not None:
            prompt = self.append_choices(
                options.retry_prompt,
                channel_id,
                choices,
                choice_style,
                choice_options
            )
        else:
            prompt = self.append_choices(
                options.prompt,
                channel_id,
                choices,
                choice_style,
                choice_options
            )
        
        # Send prompt
        await turn_context.send_activity(prompt)

    async def on_recognize(
        self,
        turn_context: TurnContext,
        state: Dict[str, object],
        options: PromptOptions
    ) -> PromptRecognizerResult:
        if not turn_context:
            raise TypeError('ChoicePrompt.on_recognize(): turn_context cannot be None.')
        
        choices: List[Choice] = options.choices if options.choices else []
        result: PromptRecognizerResult = PromptRecognizerResult()

        if turn_context.activity.type == ActivityTypes.message:
            activity = turn_context.activity
            utterance = activity.text
            opt = self.recognizer_options if self.recognizer_options else FindChoicesOptions()
            # TODO use recognizers constant for English
            opt.locale = activity.locale if activity.locale else (self.default_locale or 'en-us')
            # TODO complete when ChoiceRecognizers is complete -- pending publishing of new recognizers-numbers bits
            