# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from enum import Enum


class ListStyle(str, Enum):
    none = 0
    auto = 1
    in_line = 2
    list_style = 3
    suggested_action = 4
    hero_card = 5
