# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

""" Result returned by a prompts recognizer function.
"""


class PromptRecognizerResult:
    def __init__(self, succeeded: bool = False, value: object = None):
        """Creates result returned by a prompts recognizer function."""
        self.succeeded = succeeded
        self.value = value
