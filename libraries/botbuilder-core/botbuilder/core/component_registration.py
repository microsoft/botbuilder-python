# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import Dict, Iterable, Type


class ComponentRegistration:
    @staticmethod
    def get_components() -> Iterable["ComponentRegistration"]:
        return _components.values()

    @staticmethod
    def add(component_registration: "ComponentRegistration"):
        _components[component_registration.__class__] = component_registration


_components: Dict[Type, ComponentRegistration] = {}
