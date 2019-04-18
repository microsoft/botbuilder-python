# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

""" Result returned by a prompts recognizer function.
"""
class PromptRecognizerResult():
    def __init__(self):
        """Creates result returned by a prompts recognizer function.
        """
        self._succeeded : bool = False
        self._value : object = None
        
    @property
    def succeeded(self) -> bool:
        """Gets a bool indicating whether the users utterance was successfully recognized 
        """
        return self._succeeded

    @succeeded.setter
    def succeeded(self, value: bool) -> None:
        """Sets the whether the users utterance was successfully recognized
        Parameters
        ----------
        value
            A bool indicating whether the users utterance was successfully recognized
        """
        self._succeeded = value

    @property
    def value(self) -> object:
        """Gets the value that was recognized if succeeded is `True` 
        """
        return self._value

    @value.setter
    def value(self, value: object) -> None:
        """Sets the value that was recognized (if succeeded is `True`)
        Parameters
        ----------
        value
            The value that was recognized
        """
        self._value = value
    
    

