# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import Any, Dict, Union


class HttpRequest:
    def __init__(
        self,
        *,
        request_uri: Union[str, None] = None,
        content: Any = None,
        headers: Dict[str, str] = None
    ) -> None:
        self.request_uri = request_uri
        self.content = content
        self.headers = headers
