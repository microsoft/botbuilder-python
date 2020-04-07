# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.


from abc import ABC


# TODO: debate if this class is pertinent or should use msrest infrastructure
class Serializable(ABC):
    def to_json(self) -> str:
        raise NotImplementedError()

    def from_json(self, json_str: str):
        raise NotImplementedError()
