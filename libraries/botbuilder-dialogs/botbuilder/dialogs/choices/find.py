# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import Union

from .choice import Choice
from .find_choices_options import FindChoicesOptions

class Find:
    """ Contains methods for matching user input against a list of choices """

    def __init__(self, utterance: str, choices: Union[str, Choice], options: FindChoicesOptions = None):
        if not choices:
            raise TypeError('Find: choices cannot be None.')
        
        self.options = options if options else FindChoicesOptions()