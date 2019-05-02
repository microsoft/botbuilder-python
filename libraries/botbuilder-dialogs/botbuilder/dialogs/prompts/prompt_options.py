# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.schema import Activity
from botbuilder.dialogs.choices import Choice, ListStyle


class PromptOptions:

    def __init__(self, prompt: Activity = None, retry_prompt: Activity = None, choices: [Choice] = None, style: ListStyle = None, validations: object = None, number_of_attempts: int = 0):
        self._prompt= prompt 
        self._retry_prompt= retry_prompt
        self._choices= choices
        self._style = style
        self._validations = validations
        self._number_of_attempts = number_of_attempts
        
    @property
    def prompt(self) -> Activity:
        """Gets the initial prompt to send the user as Activity.
        """
        return self._prompt

    @prompt.setter
    def prompt(self, value: Activity) -> None:
        """Sets the initial prompt to send the user as Activity.
        Parameters
        ----------
        value
            The new value of the initial prompt.
        """
        self._prompt = value
        
    @property
    def retry_prompt(self) -> Activity:
        """Gets the retry prompt to send the user as Activity.
        """
        return self._retry_prompt

    @retry_prompt.setter
    def retry_prompt(self, value: Activity) -> None:
        """Sets the retry prompt to send the user as Activity.
        Parameters
        ----------
        value
            The new value of the retry prompt.
        """
        self._retry_prompt = value
        
    @property
    def choices(self) -> Choice:
        """Gets the list of choices associated with the prompt.
        """
        return self._choices

    @choices.setter
    def choices(self, value: Choice) -> None:
        """Sets the list of choices associated with the prompt.
        Parameters
        ----------
        value
            The new list of choices associated with the prompt.
        """
        self._choices = value
        
    @property
    def style(self) -> ListStyle:
        """Gets the ListStyle for a ChoicePrompt.
        """
        return self._style

    @style.setter
    def style(self, value: ListStyle) -> None:
        """Sets the ListStyle for a ChoicePrompt.
        Parameters
        ----------
        value
            The new ListStyle for a ChoicePrompt.
        """
        self._style = value

    @property
    def validations(self) -> object:
        """Gets additional validation rules to pass the prompts validator routine.
        """
        return self._validations

    @validations.setter
    def validations(self, value: object) -> None:
        """Sets additional validation rules to pass the prompts validator routine.
        Parameters
        ----------
        value
            Additional validation rules to pass the prompts validator routine.
        """
        self._validations = value
        
    @property
    def number_of_attempts(self) -> int:
        """Gets the count of the number of times the prompt has retried.
        """
        return self._number_of_attempts

    @number_of_attempts.setter
    def number_of_attempts(self, value: int) -> None:
        """Sets the count of the number of times the prompt has retried.
        Parameters
        ----------
        value
            Count of the number of times the prompt has retried.
        """
        self._number_of_attempts = value
        
