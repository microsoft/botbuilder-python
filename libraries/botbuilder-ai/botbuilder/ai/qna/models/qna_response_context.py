# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from msrest.serialization import Model

from .prompt import Prompt
from typing import List


class QnAResponseContext(Model):
    """ The context associated with QnA.  Used to mark if the qna response has related prompts. """

    _attribute_map = {"prompts": {"key": "prompts", "type": "List of Prompt"}}

    def __init__(self, prompts: List[Prompt], **kwargs):
        """
        Parameters:
        -----------

        prompts: The prompts collection of related prompts.
        """

        super().__init__(**kwargs)

        self.prompts = prompts
