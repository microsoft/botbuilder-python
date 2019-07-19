# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from .find_values_options import FindValuesOptions


class FindChoicesOptions(FindValuesOptions):
    """ Contains options to control how input is matched against a list of choices """

    def __init__(self, no_value: bool = None, no_action: bool = None, **kwargs):
        """
        Parameters:
        -----------

        no_value: (Optional) If `True`, the choices `value` field will NOT be search over. Defaults to `False`.

        no_action: (Optional) If `True`, the choices `action.title` field will NOT be searched over.
         Defaults to `False`.
        """

        super().__init__(**kwargs)
        self.no_value = no_value
        self.no_action = no_action
