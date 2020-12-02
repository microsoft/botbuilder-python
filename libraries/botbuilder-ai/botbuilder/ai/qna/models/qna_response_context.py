# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from msrest.serialization import Model


class QnAResponseContext(Model):
    """
    The context associated with QnA.
    Used to mark if the qna response has related prompts.
    """

    _attribute_map = {
        "is_context_only": {"key": "isContextOnly", "type": "bool"},
        "prompts": {"key": "prompts", "type": "[Prompt]"},
    }

    def __init__(self, **kwargs):
        """
        Parameters:
        -----------

        is_context_only: Whether this prompt is context only.

        prompts: The prompts collection of related prompts.

        """

        super().__init__(**kwargs)
        self.is_context_only = kwargs.get("is_context_only", None)
        self.prompts = kwargs.get("prompts", None)
