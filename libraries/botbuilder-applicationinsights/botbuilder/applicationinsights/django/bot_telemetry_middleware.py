# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
import sys
import json
from threading import current_thread

# Map of thread id => POST body text
_request_bodies = {}

def retrieve_bot_body():
    """ retrieve_bot_body
    Retrieve the POST body text from temporary cache.
    The POST body corresponds with the thread id and should resides in 
    cache just for lifetime of request.

    TODO: Add cleanup job to kill orphans
    """
    result = _request_bodies.pop(current_thread().ident, None)
    return result

class BotTelemetryMiddleware():
    """
    Save off the POST body to later populate bot properties
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self.process_request(request)
        return self.get_response(request)

    def process_request(self, request):
        body_unicode = request.body.decode('utf-8') if request.method == "POST" else None
        # Sanity check JSON
        if body_unicode != None:
            try:
                body = json.loads(body_unicode)
            except:
                return
            # Integration layer expecting just the json text.
            _request_bodies[current_thread().ident] = body_unicode

    
