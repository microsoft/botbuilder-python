# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import List
from msrest.serialization import Model
from .prompt import Prompt


class QnAResponseContext(Model):
    """
    The context associated with QnA.
    Used to mark if the qna response has related prompts.
    """

    _attribute_map = {
        "is_context_only": {"key": "isContextOnly", "type": "bool"},
        "prompts": {"key": "prompts", "type": "[Prompt]"},
    }

    def __init__(
        self, *, is_context_only: bool = False, prompts: List[Prompt] = None, **kwargs
    ):
        """
        Parameters:
        -----------

        is_context_only: Whether this prompt is context only.

        prompts: The prompts collection of related prompts.

        """

        super(QnAResponseContext, self).__init__(**kwargs)
        self.is_context_only = is_context_only
        self.prompts = prompts
