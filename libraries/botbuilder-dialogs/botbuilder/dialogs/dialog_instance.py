# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import Dict
from botbuilder.core import BotState


class DialogInstance:
    """
    Tracking information for a dialog on the stack.
    """

    def __init__(self, id: str = None, state: Dict[str, object] = None):
        self.id: str = id  # pylint: disable=invalid-name
        self.state: Dict[str, object] = state

    def __str__(self):
        result = "\ndialog_instance_id: %s\n" % self.id
        if self.state is not None:
            for key, value in self.state.items():
                result += "   {} ({})\n".format(key, str(value))
        return result


def serializer(dialog_instance: DialogInstance) -> Dict[str, object]:
    return dict(id=dialog_instance.id, state=dialog_instance.state)


def deserializer(data: Dict[str, object]) -> DialogInstance:
    return DialogInstance(data["id"], data["state"])


BotState.register_serialization_functions(DialogInstance, serializer, deserializer)
