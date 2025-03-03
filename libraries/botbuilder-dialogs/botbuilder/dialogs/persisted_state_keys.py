# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import Union

class PersistedStateKeys:
    def __init__(self):
        self.user_state: Union[str, None] = None
        self.conversation_state: Union[str, None] = None
