# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from .alias_path_resolver import AliasPathResolver


class DollarPathResolver(AliasPathResolver):
    def __init__(self):
        super().__init__(alias="$", prefix="dialog.")
