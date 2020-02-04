# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import Dict


class DialogInstance:
    """
    Tracking information for a dialog on the stack.
    """

    def __init__(self):
        """
        Gets or sets the ID of the dialog and gets or sets the instance's
        persisted state.

        :var id: The ID of the dialog
        :vartype id: str
        :var state: The instance's persisted state.
        :vartype state: :class:`typing.Dict[str, object]`
        """
        self.id: str = None  # pylint: disable=invalid-name

        self.state: Dict[str, object] = {}

    def __str__(self):
        """
        Gets or sets a stack index.

        :return result: Returns stack index.
        :rtype result: str
        """
        result = "\ndialog_instance_id: %s\n" % self.id
        if self.state is not None:
            for key, value in self.state.items():
                result += "   {} ({})\n".format(key, str(value))
        return result
