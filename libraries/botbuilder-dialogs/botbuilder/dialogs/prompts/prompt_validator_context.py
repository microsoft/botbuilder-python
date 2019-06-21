# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
from typing import Dict
from botbuilder.core.turn_context import TurnContext
from .prompt_options import PromptOptions
from .prompt_recognizer_result import PromptRecognizerResult


""" Contextual information passed to a custom `PromptValidator`.
"""
class PromptValidatorContext():
    def __init__(self, turn_context: TurnContext, recognized: PromptRecognizerResult, state: Dict[str, object], options: PromptOptions, attempt_count: int= None): 
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
        self.context = turn_context
        self.recognized = recognized
        self.state = state
        self.options = options
        self.attempt_count = attempt_count
