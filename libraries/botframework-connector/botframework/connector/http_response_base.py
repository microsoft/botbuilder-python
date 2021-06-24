# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from abc import ABC, abstractmethod
from http import HTTPStatus
from typing import Union


class HttpResponseBase(ABC):
    @property
    @abstractmethod
    def status_code(self) -> Union[HTTPStatus, int]:
        raise NotImplementedError()

    @abstractmethod
    async def is_succesful(self) -> bool:
        raise NotImplementedError()

    @abstractmethod
    async def read_content_str(self) -> str:
        raise NotImplementedError()
