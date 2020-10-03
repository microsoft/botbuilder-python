# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
"""Bot Telemetry Middleware."""

from threading import current_thread


# Map of thread id => POST body text
_REQUEST_BODIES = {}


def retrieve_bot_body():
    """
    Retrieve the POST body text from temporary cache.

    The POST body corresponds to the thread ID and must reside in the cache just for the lifetime of the request.
    """

    result = _REQUEST_BODIES.get(current_thread().ident, None)
    return result


class BotTelemetryMiddleware:
    """
    Save off the POST body to later populate bot-specific properties to add to Application Insights.

    Example activating MIDDLEWARE in Django settings:

    .. code-block:: python

        MIDDLEWARE = [
            # Ideally add somewhere near top
            'botbuilder.applicationinsights.django.BotTelemetryMiddleware',
            ...
            ]
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self.process_request(request)
        response = self.get_response(request)
        _REQUEST_BODIES.pop(current_thread().ident, None)
        return response

    def process_request(self, request) -> bool:
        """Process the incoming Django request."""
        # Bot Service doesn't handle anything over 256k
        # TODO: Add length check
        body_unicode = (
            request.body.decode("utf-8") if request.method == "POST" else None
        )
        # Sanity check JSON
        if body_unicode is not None:
            # Integration layer expecting just the json text.
            _REQUEST_BODIES[current_thread().ident] = body_unicode
        return True
