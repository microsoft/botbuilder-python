# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
"""Flask Telemetry Bot Middleware."""

from io import BytesIO
from threading import current_thread

# Map of thread id => POST body text
_REQUEST_BODIES = {}


def retrieve_flask_body():
    """retrieve_flask_body
    Retrieve the POST body text from temporary cache.
    The POST body corresponds with the thread id and should resides in
    cache just for lifetime of request.
    """
    result = _REQUEST_BODIES.pop(current_thread().ident, None)
    return result


class BotTelemetryMiddleware:
    """Bot Telemetry Middleware
    Save off the POST body to later populate bot-specific properties to
    add to Application Insights.

    Example adding telemetry middleware to Flask:
       app = Flask(__name__)
       app.wsgi_app = BotTelemetryMiddleware(app.wsgi_app)
    """

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        self.process_request(environ)
        return self.app(environ, start_response)

    def process_request(self, environ) -> bool:
        """Process the incoming Flask request."""
        # Bot Service doesn't handle anything over 256k
        length = int(environ.get("CONTENT_LENGTH", "0"))
        if length > 256 * 1024:
            print(f"request too long - rejected")
        else:
            body_bytes = environ["wsgi.input"].read(length)
            environ["wsgi.input"] = BytesIO(body_bytes)
            body_unicode = body_bytes.decode("utf-8")

        # Sanity check JSON
        if body_unicode is not None:
            # Integration layer expecting just the json text.
            _REQUEST_BODIES[current_thread().ident] = body_unicode
        return True
