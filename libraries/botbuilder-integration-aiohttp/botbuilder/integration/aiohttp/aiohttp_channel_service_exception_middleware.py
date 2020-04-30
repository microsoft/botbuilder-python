# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from aiohttp.web import (
    middleware,
    HTTPError,
    HTTPNotImplemented,
    HTTPUnauthorized,
    HTTPNotFound,
    HTTPInternalServerError,
)

from botbuilder.core import BotActionNotImplementedError


@middleware
async def aiohttp_error_middleware(request, handler):
    try:
        response = await handler(request)
        return response
    except BotActionNotImplementedError:
        raise HTTPNotImplemented()
    except NotImplementedError:
        raise HTTPNotImplemented()
    except PermissionError:
        raise HTTPUnauthorized()
    except KeyError:
        raise HTTPNotFound()
    except HTTPError as error:
        # In the case the integration adapter raises a specific HTTPError
        raise error
    except Exception:
        raise HTTPInternalServerError()
