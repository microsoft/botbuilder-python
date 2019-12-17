# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from inspect import getmembers
from typing import Type
from enum import Enum

from msrest.serialization import Model, Deserializer, Serializer

import botbuilder.schema as schema
import botbuilder.schema.teams as teams_schema

# Optimization: The dependencies dictionary could be cached here,
# and shared between the two methods.


def deserializer_helper(msrest_cls: Type[Model], dict_to_deserialize: dict) -> Model:
    dependencies = [
        schema_cls
        for key, schema_cls in getmembers(schema)
        if isinstance(schema_cls, type) and issubclass(schema_cls, (Model, Enum))
    ]
    dependencies += [
        schema_cls
        for key, schema_cls in getmembers(teams_schema)
        if isinstance(schema_cls, type) and issubclass(schema_cls, (Model, Enum))
    ]
    dependencies_dict = {dependency.__name__: dependency for dependency in dependencies}
    deserializer = Deserializer(dependencies_dict)
    return deserializer(msrest_cls.__name__, dict_to_deserialize)


def serializer_helper(object_to_serialize: Model) -> dict:
    if object_to_serialize is None:
        return None

    dependencies = [
        schema_cls
        for key, schema_cls in getmembers(schema)
        if isinstance(schema_cls, type) and issubclass(schema_cls, (Model, Enum))
    ]
    dependencies += [
        schema_cls
        for key, schema_cls in getmembers(teams_schema)
        if isinstance(schema_cls, type) and issubclass(schema_cls, (Model, Enum))
    ]
    dependencies_dict = {dependency.__name__: dependency for dependency in dependencies}
    serializer = Serializer(dependencies_dict)
    # pylint: disable=protected-access
    return serializer._serialize(object_to_serialize)
