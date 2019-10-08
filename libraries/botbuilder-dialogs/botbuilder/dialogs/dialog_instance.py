# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from msrest.serialization import Model
from botbuilder.core import BotState
from typing import Dict


class DialogInstance(Model):
    """
    Tracking information for a dialog on the stack.
    """

    _attribute_map = {
        "id": {"key": "id", "type": "str"},
        "state": {"key": "state", "type": "{object}"},
    }

    def __init__(self, id: str = None, state: Dict[str, object] = None, **kwargs):
        super(DialogInstance, self).__init__(**kwargs)
        self.id: str = id  # pylint: disable=invalid-name
        self.state: Dict[str, object] = state

    def __str__(self):
        result = "\ndialog_instance_id: %s\n" % self.id
        if self.state is not None:
            for key, value in self.state.items():
                result += "   {} ({})\n".format(key, str(value))
        return result


BotState.register_msrest_deserializer(DialogInstance)
