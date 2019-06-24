# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from .find_values_options import FindValuesOptions

class FindChoicesOptions(FindValuesOptions):
    def __init__(self, no_value: bool = None, no_action: bool = None, **kwargs):
        super().__init__(**kwargs)
        self.no_value = no_value
        self.no_action = no_action