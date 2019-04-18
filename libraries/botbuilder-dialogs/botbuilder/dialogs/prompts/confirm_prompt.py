# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core.turn_context import TurnContext
from botbuilder.schema.connector_client_enums import ActivityTypes

  

class ConfirmPrompt(Prompt):
    # TODO: Fix to reference recognizer to use proper constants
    choice_defaults : Dict[string, object] = { 
        { 'English', (Choice("Si"), Choice("No"), ChoiceFactoryOptions(", ", " o ", ", o ", True)) },
        { 'Dutch', (Choice("Ja"), Choice("Nee"), ChoiceFactoryOptions(", ", " of ", ", of ", True)) },
        { 'English', (Choice("Yes"), Choice("No"), ChoiceFactoryOptions(", ", " or ", ", or ", True)) },
        { 'French', (Choice("Oui"), Choice("Non"), ChoiceFactoryOptions(", ", " ou ", ", ou ", True)) },
        { 'German', (Choice("Ja"), Choice("Nein"), ChoiceFactoryOptions(", ", " oder ", ", oder ", True)) },
        { 'Japanese', (Choice("はい"), Choice("いいえ"), ChoiceFactoryOptions("、 ", " または ", "、 または ", True)) },
        { 'Portuguese', (Choice("Sim"), Choice("Não"), ChoiceFactoryOptions(", ", " ou ", ", ou ", True)) },
        { 'Chinese', (Choice("是的"), Choice("不"), ChoiceFactoryOptions("， ", " 要么 ",  "， 要么 ", True)) },
        }    
        
    # TODO: PromptValidator
    def __init__(self, dialog_id: str, validator: object, default_locale: str):
        super(ConfirmPrompt, self).__init__(dialog_id, validator)
        if dialogs is None:
            raise TypeError('ConfirmPrompt(): dialogs cannot be None.')
        self.style = ListStyle.auto
        self.default_locale = defaultLocale
        self.choice_options = None
        self.confirm_choices = None
        
    async def on_prompt(self, turn_context: TurnContext, state: Dict[str, object], options: PromptOptions, is_retry: bool):
        if not turn_context:
            raise TypeError('ConfirmPrompt.on_prompt(): turn_context cannot be None.')
        if not options:
            raise TypeError('ConfirmPrompt.on_prompt(): options cannot be None.')
        
        # Format prompt to send
        channel_id = turn_context.activity.channel_id
        culture  = determine_culture(turn_context.activity)
        defaults = choice_defaults[culture]
        choice_opts = choice_options if choice_options != None else defaults[2]
        confirms = confirm_choices if confirm_choices != None else (defaults[0], defaults[1])
        choices = { confirms[0], confirms[1] }
        if is_retry == True and options.retry_prompt != None:
            prompt = append_choices(options.retry_prompt)  
        else:
            prompt = append_choices(options.prompt, channel_id, choices, self.style, choice_opts)
        turn_context.send_activity(prompt)
        
    async def on_recognize(self, turn_context: TurnContext, state: Dict[str, object], options: PromptOptions) -> PromptRecognizerResult:
        if not turn_context:
            raise TypeError('ConfirmPrompt.on_prompt(): turn_context cannot be None.')
        
        result = PromptRecognizerResult();
        if turn_context.activity.type == ActivityTypes.message:
            # Recognize utterance
            message = turn_context.activity
            culture = determine_culture(turn_context.activity)
            results = ChoiceRecognizer.recognize_boolean(message.text, culture)
            if results.Count > 0:
                first = results[0];
                if "value" in first.Resolution:
                    result.Succeeded = true;
                    result.Value = first.Resolution["value"].str;
            else:
                # First check whether the prompt was sent to the user with numbers - if it was we should recognize numbers
                defaults = choice_defaults[culture];
                opts = choice_options if choice_options != None else defaults[2]

                # This logic reflects the fact that IncludeNumbers is nullable and True is the default set in Inline style
                if opts.include_numbers.has_value or opts.include_numbers.value:
                    # The text may be a number in which case we will interpret that as a choice.
                    confirmChoices = confirm_choices if confirm_choices != None else (defaults[0], defaults[1])
                    choices = { confirmChoices[0], confirmChoices[1] };
                    secondAttemptResults = ChoiceRecognizers.recognize_choices(message.text, choices);
                    if len(secondAttemptResults) > 0:
                        result.succeeded = True
                        result.value = secondAttemptResults[0].resolution.index == 0;

        return result;
        
    def determine_culture(self, activity: Activity) -> str:
        culture = activity.locale if activity.locale != None else default_locale
        if not culture or not culture in choice_defaults:
            culture = "English" # TODO: Fix to reference recognizer to use proper constants
        return culture