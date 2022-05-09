# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import Dict

from .persisted_state_keys import PersistedStateKeys


class PersistedState:
    def __init__(self, keys: PersistedStateKeys = None, data: Dict[str, object] = None):
        if keys and data:
            self.user_state: Dict[str, object] = (
                data[keys.user_state] if keys.user_state in data else {}
            )
            self.conversation_state: Dict[str, object] = (
                data[keys.conversation_state] if keys.conversation_state in data else {}
            )
        else:
            self.user_state: Dict[str, object] = {}
            self.conversation_state: Dict[str, object] = {}
