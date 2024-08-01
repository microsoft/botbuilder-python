# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from enum import Enum
from typing import Type
import json
from botbuilder.schema.teams.surface_type import SurfaceType


class Surface:

    def __init__(self, type: SurfaceType):
        """
        Initializes a new instance of the Surface class.

        :param type: Type of Surface.
        """
        self.type = type

    @property
    def type(self) -> SurfaceType:
        return self._type

    @type.setter
    def type(self, value: SurfaceType):
        self._type = value

    def to_json(self) -> str:
        """
        Converts the Surface object to JSON.

        :return: JSON representation of the Surface object.
        """
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
