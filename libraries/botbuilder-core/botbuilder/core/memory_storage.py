# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from copy import deepcopy
from typing import Dict, List
from .storage import Storage, StoreItem


class MemoryStorage(Storage):
    def __init__(self, dictionary=None):
        super(MemoryStorage, self).__init__()
        self.memory = dictionary if dictionary is not None else {}
        self._e_tag = 0

    async def delete(self, keys: List[str]):
        try:
            for key in keys:
                if key in self.memory:
                    del self.memory[key]
        except TypeError as error:
            raise error

    async def read(self, keys: List[str]):
        data = {}
        if not keys:
            return data
        try:
            for key in keys:
                if key in self.memory:
                    data[key] = self.memory[key]
        except TypeError as error:
            raise error

        return data

    async def write(self, changes: Dict[str, StoreItem]):
        if changes is None:
            raise Exception("Changes are required when writing")
        if not changes:
            return
        try:
            # iterate over the changes
            for (key, change) in changes.items():
                new_value = deepcopy(change)
                old_state_etag = None

                # Check if the a matching key already exists in self.memory
                # If it exists then we want to cache its original value from memory
                if key in self.memory:
                    old_state = self.memory[key]
                    if isinstance(old_state, dict):
                        old_state_etag = old_state.get("e_tag", None)
                    elif hasattr(old_state, "e_tag"):
                        old_state_etag = old_state.e_tag

                new_state = new_value

                # Set ETag if applicable
                new_value_etag = None
                if isinstance(new_value, dict):
                    new_value_etag = new_value.get("e_tag", None)
                elif hasattr(new_value, "e_tag"):
                    new_value_etag = new_value.e_tag
                if new_value_etag == "":
                    raise Exception("memory_storage.write(): etag missing")
                if (
                    old_state_etag is not None
                    and new_value_etag is not None
                    and new_value_etag != "*"
                    and new_value_etag < old_state_etag
                ):
                    raise KeyError(
                        "Etag conflict.\nOriginal: %s\r\nCurrent: %s"
                        % (new_value_etag, old_state_etag)
                    )
                if isinstance(new_state, dict):
                    new_state["e_tag"] = str(self._e_tag)
                else:
                    new_state.e_tag = str(self._e_tag)
                self._e_tag += 1
                self.memory[key] = deepcopy(new_state)

        except Exception as error:
            raise error

    # TODO: Check if needed, if not remove
    def __should_write_changes(
        self, old_value: StoreItem, new_value: StoreItem
    ) -> bool:
        """
        Helper method that compares two StoreItems and their e_tags and returns True if the new_value should overwrite
        the old_value. Otherwise returns False.
        :param old_value:
        :param new_value:
        :return:
        """

        # If old_value is none or if the new_value's e_tag is '*', then we return True
        if old_value is None or (
            hasattr(new_value, "e_tag") and new_value.e_tag == "*"
        ):
            return True
        # If none of the above cases, we verify that e_tags exist on both arguments
        if hasattr(new_value, "e_tag") and hasattr(old_value, "e_tag"):
            if new_value.e_tag is not None and old_value.e_tag is None:
                return True
            # And then we do a comparing between the old and new e_tag values to decide if the new data will be written
            if old_value.e_tag == new_value.e_tag or int(old_value.e_tag) <= int(
                new_value.e_tag
            ):
                return True
            return False
        return False
