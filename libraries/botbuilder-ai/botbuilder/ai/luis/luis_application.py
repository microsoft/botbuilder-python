# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license.

from pathlib import PurePosixPath
from typing import Tuple
from urllib.parse import ParseResult, parse_qs, unquote, urlparse, urlunparse
from uuid import UUID, uuid4


class LuisApplication:
    """
    Data describing a LUIS application.
    """

    def __init__(self, application_id: str, endpoint_key: str, endpoint: str):
        """Initializes a new instance of the :class:`LuisApplication` class.

        :param application_id: LUIS application ID.
        :type application_id: str
        :param endpoint_key: LUIS subscription or endpoint key.
        :type endpoint_key: str
        :param endpoint: LUIS endpoint to use, like https://westus.api.cognitive.microsoft.com.
        :type endpoint: str
        :raises ValueError:
        :raises ValueError:
        :raises ValueError:
        """

        _, valid = LuisApplication._try_parse_uuid4(application_id)
        if not valid:
            raise ValueError(f'"{application_id}" is not a valid LUIS application id.')

        _, valid = LuisApplication._try_parse_uuid4(endpoint_key)
        if not valid:
            raise ValueError(f'"{endpoint_key}" is not a valid LUIS subscription key.')

        if not endpoint or endpoint.isspace():
            endpoint = "https://westus.api.cognitive.microsoft.com"

        _, valid = LuisApplication._try_parse_url(endpoint)
        if not valid:
            raise ValueError(f'"{endpoint}" is not a valid LUIS endpoint.')

        self.application_id = application_id
        self.endpoint_key = endpoint_key
        self.endpoint = endpoint

    @classmethod
    def from_application_endpoint(cls, application_endpoint: str):
        """Initializes a new instance of the :class:`LuisApplication` class.

        :param application_endpoint: LUIS application endpoint.
        :type application_endpoint: str
        :return:
        :rtype: LuisApplication
        """
        (application_id, endpoint_key, endpoint) = LuisApplication._parse(
            application_endpoint
        )
        return cls(application_id, endpoint_key, endpoint)

    @staticmethod
    def _parse(application_endpoint: str) -> Tuple[str, str, str]:
        url, valid = LuisApplication._try_parse_url(application_endpoint)
        if not valid:
            raise ValueError(
                f"{application_endpoint} is not a valid LUIS application endpoint."
            )

        segments = PurePosixPath(unquote(url.path)).parts
        application_id = segments[-1] if segments else None
        qs_parsed_result = parse_qs(url.query)
        endpoint_key = qs_parsed_result.get("subscription-key", [None])[0]

        parts_for_base_url = url.scheme, url.netloc, "", None, None, None
        endpoint = urlunparse(parts_for_base_url)
        return (application_id, endpoint_key, endpoint)

    @staticmethod
    def _try_parse_uuid4(uuid_string: str) -> Tuple[uuid4, bool]:
        try:
            uuid = UUID(uuid_string, version=4)
        except (TypeError, ValueError):
            return None, False

        return uuid, True

    @staticmethod
    def _try_parse_url(url: str) -> Tuple[ParseResult, bool]:
        try:
            result = urlparse(url)
            return result, True
        except ValueError:
            return None, False
