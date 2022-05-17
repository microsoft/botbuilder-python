# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import traceback

from aiohttp.web import (
    middleware,
    HTTPException,
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
    except HTTPException:
        raise
    except Exception:
        traceback.print_exc()
        raise HTTPInternalServerError()
