# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from abc import ABC


class StatePropertyInfo(ABC):
    @property
    def name(self):
        raise NotImplementedError()
