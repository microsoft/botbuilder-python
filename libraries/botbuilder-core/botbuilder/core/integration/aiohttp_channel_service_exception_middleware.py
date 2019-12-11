from aiohttp.web import (
    middleware,
    HTTPNotImplemented,
    HTTPUnauthorized,
    HTTPNotFound,
    HTTPInternalServerError,
)

from .channel_service_handler import BotActionNotImplementedError


@middleware
async def error_middleware(request, handler):
    try:
        response = await handler(request)
        return response
    except BotActionNotImplementedError:
        raise HTTPNotImplemented()
    except PermissionError:
        raise HTTPUnauthorized()
    except KeyError:
        raise HTTPNotFound()
    except Exception:
        raise HTTPInternalServerError()
