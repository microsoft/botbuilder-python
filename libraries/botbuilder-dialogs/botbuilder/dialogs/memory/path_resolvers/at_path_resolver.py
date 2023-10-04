# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from .alias_path_resolver import AliasPathResolver


class AtPathResolver(AliasPathResolver):
    _DELIMITERS = [".", "["]

    def __init__(self):
        super().__init__(alias="@", prefix="")

        self._PREFIX = "turn.recognized.entities."  # pylint: disable=invalid-name

    def transform_path(self, path: str):
        if not path:
            raise TypeError(f"Expecting: path, but received None")

        path = path.strip()
        if (
            path.startswith("@")
            and len(path) > 1
            and AtPathResolver._is_path_char(path[1])
        ):
            end = any(delimiter in path for delimiter in AtPathResolver._DELIMITERS)
            if end == -1:
                end = len(path)

            prop = path[1:end]
            suffix = path[end:]
            path = f"{self._PREFIX}{prop}.first(){suffix}"

        return path

    @staticmethod
    def _index_of_any(string: str, elements_to_search_for) -> int:
        for element in elements_to_search_for:
            index = string.find(element)
            if index != -1:
                return index

        return -1
