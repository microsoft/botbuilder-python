# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import Dict


class DialogInstance:
    """
    Tracking information for a dialog on the stack.
    """

    def __init__(self):
        """    
        Gets or sets the ID of the dialog and gets or sets the instance's persisted state.

        :var self.id: The ID of the dialog
        :vartype self.id: str
        :var self.state: The instance's persisted state.
        :vartype self.state: Dict
        """
        self.id: str = None  # pylint: disable=invalid-name

        self.state: Dict[str, object] = {}

    def __str__(self):
        """
        Gets or sets a stack index. 
        
        .. remarks::
            Positive values are indexes within the current DC and negative values are indexes in the parent DC.

        :return: result
        :rtype: str
        """
        result = "\ndialog_instance_id: %s\n" % self.id
        if self.state is not None:
            for key, value in self.state.items():
                result += "   {} ({})\n".format(key, str(value))
        return result
