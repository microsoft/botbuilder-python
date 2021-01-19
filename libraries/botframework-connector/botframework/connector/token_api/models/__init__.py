# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

try:
    from ._models_py3 import AadResourceUrls
    from ._models_py3 import Error
    from ._models_py3 import ErrorResponse, ErrorResponseException
    from ._models_py3 import InnerHttpError
    from ._models_py3 import SignInUrlResponse
    from ._models_py3 import TokenExchangeRequest
    from ._models_py3 import TokenExchangeResource
    from ._models_py3 import TokenResponse
    from ._models_py3 import TokenStatus
except (SyntaxError, ImportError):
    from ._models import AadResourceUrls
    from ._models import Error
    from ._models import ErrorResponse, ErrorResponseException
    from ._models import InnerHttpError
    from ._models import SignInUrlResponse
    from ._models import TokenExchangeRequest
    from ._models import TokenExchangeResource
    from ._models import TokenResponse
    from ._models import TokenStatus

__all__ = [
    "AadResourceUrls",
    "Error",
    "ErrorResponse",
    "ErrorResponseException",
    "InnerHttpError",
    "SignInUrlResponse",
    "TokenExchangeRequest",
    "TokenExchangeResource",
    "TokenResponse",
    "TokenStatus",
]
