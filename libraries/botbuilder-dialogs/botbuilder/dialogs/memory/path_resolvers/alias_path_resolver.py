# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.dialogs.memory import PathResolverBase


class AliasPathResolver(PathResolverBase):
    def __init__(self, alias: str, prefix: str, postfix: str = None):
        """
        Initializes a new instance of the <see cref="AliasPathResolver"/> class.
        <param name="alias">Alias name.</param>
        <param name="prefix">Prefix name.</param>
        <param name="postfix">Postfix name.</param>
        """
        if alias is None:
            raise TypeError(f"Expecting: alias, but received None")
        if prefix is None:
            raise TypeError(f"Expecting: prefix, but received None")

        # Gets the alias name.
        self.alias = alias.strip()
        self._prefix = prefix.strip()
        self._postfix = postfix.strip() if postfix else ""

    def transform_path(self, path: str):
        """
        Transforms the path.
        <param name="path">Path to inspect.</param>
        <returns>Transformed path.</returns>
        """
        if not path:
            raise TypeError(f"Expecting: path, but received None")

        path = path.strip()
        if (
            path.startswith(self.alias)
            and len(path) > len(self.alias)
            and AliasPathResolver._is_path_char(path[len(self.alias)])
        ):
            # here we only deals with trailing alias, alias in middle be handled in further breakdown
            # $xxx -> path.xxx
            return f"{self._prefix}{path[len(self.alias):]}{self._postfix}".rstrip(".")

        return path

    @staticmethod
    def _is_path_char(char: str) -> bool:
        """
        Verifies if a character is valid for a path.
        <param name="ch">Character to verify.</param>
        <returns><c>true</c> if the character is valid for a path otherwise, <c>false</c>.</returns>
        """
        return len(char) == 1 and (char.isalpha() or char == "_")
