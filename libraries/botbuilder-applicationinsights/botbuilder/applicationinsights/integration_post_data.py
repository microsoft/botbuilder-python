# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
"""Retrieve the POST request body from underlying web framework."""

import sys
import json
from botbuilder.applicationinsights.django import retrieve_bot_body
from botbuilder.applicationinsights.flask import retrieve_flask_body


class IntegrationPostData:
    """
    Retrieve the POST body from the underlying framework:
    - Flask
    - Django
    - (soon Tornado?)

    This class:
    - Detects framework (currently flask or django)
    - Pulls the current request body as a string

    Usage:
      botdata = BotTelemetryData()
      body = botdata.activity_json  # Get current request body as json object
      activity_id = body[id] # Get the ID from the POST body
    """

    def __init__(self):
        pass

    @property
    def activity_json(self) -> json:
        """Retrieve the request body as json (Activity)."""
        body_text = self.get_request_body()
        body = json.loads(body_text) if body_text is not None else None
        return body

    def get_request_body(self) -> str:  # pylint: disable=inconsistent-return-statements
        """Retrieve the request body from flask/django middleware component."""
        if self.detect_flask():
            return retrieve_flask_body()

        if self.detect_django():
            # Retrieve from Middleware cache
            return retrieve_bot_body()

    def detect_flask(self) -> bool:
        """Detects if running in flask."""
        return "flask" in sys.modules

    def detect_django(self) -> bool:
        """Detects if running in django."""
        return "django" in sys.modules
