# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
from typing import Dict
from botbuilder.core.turn_context import TurnContext
from .prompt_options import PromptOptions
from .prompt_recognizer_result import PromptRecognizerResult


""" Contextual information passed to a custom `PromptValidator`.
"""
class PromptValidatorContext():
    def __init__(self, turn_context: TurnContext, recognized: PromptRecognizerResult, state: Dict[str, object], options: PromptOptions): 
        """Creates contextual information passed to a custom `PromptValidator`.
        Parameters
        ----------
        turn_context
            The context for the current turn of conversation with the user. 

        recognized
            Result returned from the prompts recognizer function.
            
        state
            A dictionary of values persisted for each conversational turn while the prompt is active.
            
        options
            Original set of options passed to the prompt by the calling dialog.
            
        """
        self._context = turn_context
        self._recognized = recognized
        self._state = state
        self._options = options

    @property
    def context(self) -> TurnContext:
        """ The context for the current turn of conversation with the user.
        
        Note
        ----
        The validator can use this to re-prompt the user.
        """
        return self._context

    @property
    def recognized(self) -> PromptRecognizerResult:
        """Result returned from the prompts recognizer function.
        
        Note
        ----
        The `prompt.recognized.succeeded` field can be checked to determine of the recognizer found
        anything and then the value can be retrieved from `prompt.recognized.value`.
        """
        return self._recognized

    @property
    def state(self) -> Dict:
        """A dictionary of values persisted for each conversational turn while the prompt is active.
        
        Note
        ----
        The validator can use this to persist things like turn counts or other state information.
        """
        return self._recognized

    @property
    def options(self) -> PromptOptions:
        """Original set of options passed to the prompt by the calling dialog.
        
        Note
        ----
        The validator can extend this interface to support additional prompt options.
        """
        return self._options
