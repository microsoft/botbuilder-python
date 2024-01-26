from threading import current_thread
from aiohttp.web import middleware

# Map of thread id => POST body text
_REQUEST_BODIES = {}


def retrieve_aiohttp_body():
    """
    Retrieve the POST body text from temporary cache.

    The POST body corresponds with the thread id and should resides in
    cache just for lifetime of request.
    """
    result = _REQUEST_BODIES.pop(current_thread().ident, None)
    return result


@middleware
async def bot_telemetry_middleware(request, handler):
    """Process the incoming Flask request."""
    if (
        "Content-Type" in request.headers
        and request.headers["Content-Type"] == "application/json"
    ):
        body = await request.json()
        _REQUEST_BODIES[current_thread().ident] = body

    response = await handler(request)
    return response
