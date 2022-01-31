# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
from copy import copy
from inspect import getmembers
from typing import Type
from enum import Enum

from msrest.serialization import Model, Deserializer, Serializer

import botbuilder.schema as schema
import botbuilder.schema.teams as teams_schema

DEPENDICIES = [
    schema_cls
    for key, schema_cls in getmembers(schema)
    if isinstance(schema_cls, type) and issubclass(schema_cls, (Model, Enum))
]
DEPENDICIES += [
    schema_cls
    for key, schema_cls in getmembers(teams_schema)
    if isinstance(schema_cls, type) and issubclass(schema_cls, (Model, Enum))
]
DEPENDICIES_DICT = {dependency.__name__: dependency for dependency in DEPENDICIES}


def deserializer_helper(msrest_cls: Type[Model], dict_to_deserialize: dict) -> Model:
    deserializer = Deserializer(DEPENDICIES_DICT)
    _clean_data_for_serialization(
        deserializer.dependencies[msrest_cls.__name__], dict_to_deserialize
    )
    return deserializer(msrest_cls.__name__, dict_to_deserialize)


def serializer_helper(object_to_serialize: Model) -> dict:
    if object_to_serialize is None:
        return None

    serializer = Serializer(DEPENDICIES_DICT)
    # pylint: disable=protected-access
    return serializer._serialize(object_to_serialize)


def _clean_data_for_serialization(msrest_cls: Type[Model], dict_to_deserialize: dict):
    # pylint: disable=protected-access
    # Clean channel response of empty strings for expected objects.
    if not isinstance(dict_to_deserialize, dict):
        return
    serialization_model = copy(msrest_cls._attribute_map)
    for key, value in msrest_cls._attribute_map.items():
        if key != value["key"]:
            serialization_model[value["key"]] = value
    for prop, prop_value in dict_to_deserialize.items():
        if (
            prop in serialization_model
            and serialization_model[prop]["type"] in DEPENDICIES_DICT
            and not prop_value
        ):
            dict_to_deserialize[prop] = None
