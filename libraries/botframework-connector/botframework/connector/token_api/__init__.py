# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

from ._configuration import TokenApiClientConfiguration
from ._token_api_client import TokenApiClient

__all__ = ["TokenApiClient", "TokenApiClientConfiguration"]

from .version import VERSION

__version__ = VERSION
