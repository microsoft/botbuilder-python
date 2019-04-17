# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.schema.activity import Activity

class PromptOptions:
    def __init__(self):
        self._prompt: Activity = None 
        self._retry_prompt: Activity = None
        # TODO: Replace with Choice Object once ported
        self._choices: [] = None
        # TODO: Replace with ListStyle Object once ported
        self._style: Object = None
        self._validations: Object = None
        self._number_of_attempts: int = 0
        
    @property
    def prompt(self) -> Activity:
        """Gets the initial prompt to send the user as Activity.
        """
        return self._prompt

    @id.setter
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

    @id.setter
    def retry_prompt(self, value: Activity) -> None:
        """Sets the retry prompt to send the user as Activity.
        Parameters
        ----------
        value
            The new value of the retry prompt.
        """
        self._retry_prompt = value
        
    @property
    def choices(self) -> Object:
        """Gets the list of choices associated with the prompt.
        """
        return self._choices

    @id.setter
    def choices(self, value: Object) -> None:
        """Sets the list of choices associated with the prompt.
        Parameters
        ----------
        value
            The new list of choices associated with the prompt.
        """
        self._choices = value
        
    @property
    def style(self) -> Object:
        """Gets the ListStyle for a ChoicePrompt.
        """
        return self._style

    @id.setter
    def style(self, value: Object) -> None:
        """Sets the ListStyle for a ChoicePrompt.
        Parameters
        ----------
        value
            The new ListStyle for a ChoicePrompt.
        """
        self._style = value

    @property
    def validations(self) -> Object:
        """Gets additional validation rules to pass the prompts validator routine.
        """
        return self._validations

    @id.setter
    def validations(self, value: Object) -> None:
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

    @id.setter
    def number_of_attempts(self, value: int) -> None:
        """Sets the count of the number of times the prompt has retried.
        Parameters
        ----------
        value
            Count of the number of times the prompt has retried.
        """
        self._number_of_attempts = value

        
