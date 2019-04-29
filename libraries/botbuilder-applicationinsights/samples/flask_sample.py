# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from flask import Flask
from flask import request
from botbuilder.applicationinsights import ApplicationInsightsTelemetryClient

# Instantiate the Flask application
app = Flask(__name__)

# Register App Insights to pull telemetry
instrumentation_key = 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'
app.config['APPINSIGHTS_INSTRUMENTATIONKEY'] = instrumentation_key

telemetry = ApplicationInsightsTelemetryClient(instrumentation_key)

# define a simple route
@app.route('/', methods=['POST'])
def hello_world():
    # Use Bot's Telemetry Client which replaces session_id, user_id and adds bot-specific ID's
    telemetry.track_event("Hello World")
    telemetry.flush()
    return 'Hello World!'

# run the application
if __name__ == '__main__':
    app.run()