# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from abc import ABC

class StatePropertyAccessor(ABC):
    @property
    def name(self):
        raise NotImplementedError();