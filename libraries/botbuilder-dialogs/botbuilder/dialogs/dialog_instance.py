# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import Dict


class DialogInstance:
    """
    Tracking information for a dialog on the stack.
    """

    def __init__(self):
        self._id: str = None
        self._state: Dict[str, object] = {}

    @property
    def id(self) -> str:
        """Gets the ID of the dialog this instance is for.

        :param:
        :return str:
        """
        return self._id

    @id.setter
    def id(self, value: str) -> None:
        """Sets the ID of the dialog this instance is for.

        :param:
        :param value: ID of the dialog this instance is for.
        :return:
        """
        self._id = value

    @property
    def state(self) -> Dict[str, object]:
        """Gets the instance's persisted state.

        :param:
        :return Dict[str, object]:
        """
        return self._state

    @state.setter
    def state(self, value: Dict[str, object]) -> None:
        """Sets the instance's persisted state.

        :param:
        :param value: The instance's persisted state.
        :return:
        """
        
        self._state = value

    def __str__(self):
        result = "\ndialog_instance_id: %s\n" % self.id
        if not self._state is None:
            for key, value in self._state.items():
                result += "   {} ({})\n".format(key, str(value))
        return result