# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import Dict


class DialogInstance:
    """
    Tracking information for a dialog on the stack.
    """

    def __init__(self):
        self.id: str = None
        self.state: Dict[str, object] = {}

    def __str__(self):
        result = "\ndialog_instance_id: %s\n" % self.id
        if not self.state is None:
            for key, value in self.state.items():
                result += "   {} ({})\n".format(key, str(value))
        return result
