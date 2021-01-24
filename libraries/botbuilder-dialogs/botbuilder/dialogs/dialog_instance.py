# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import Dict


class DialogInstance:
    """
    Tracking information for a dialog on the stack.
    """

    def __init__(
        self, id: str = None, state: Dict[str, object] = None
    ):  # pylint: disable=invalid-name
        """
        Gets or sets the ID of the dialog and gets or sets the instance's persisted state.

        :var self.id: The ID of the dialog
        :vartype self.id: str
        :var self.state: The instance's persisted state.
        :vartype self.state: :class:`typing.Dict[str, object]`
        """
        self.id = id  # pylint: disable=invalid-name

        self.state = state or {}

    def __str__(self):
        """
        Gets or sets a stack index.

        :return: Returns stack index.
        :rtype: str
        """
        result = "\ndialog_instance_id: %s\n" % self.id
        if self.state is not None:
            for key, value in self.state.items():
                result += "   {} ({})\n".format(key, str(value))
        return result
