# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
from botbuilder.core.state_property_accessor import StatePropertyAccessor


class PropertyManager:
    def create_property(self, name: str) -> StatePropertyAccessor:
        raise NotImplementedError()
