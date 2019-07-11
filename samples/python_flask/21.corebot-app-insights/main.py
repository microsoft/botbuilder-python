#!/usr/bin/env python
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

"""
This sample shows how to create a bot that demonstrates the following:
- Use [LUIS](https://www.luis.ai) to implement core AI capabilities.
- Implement a multi-turn conversation using Dialogs.
- Handle user interruptions for such things as `Help` or `Cancel`.
- Prompt for and validate requests for information from the user.

"""

import asyncio
from flask import Flask, request, Response
from botbuilder.core import (
    BotFrameworkAdapter,
    BotFrameworkAdapterSettings,
    ConversationState,
    MemoryStorage,
    UserState,
    TurnContext,
)
from botbuilder.schema import Activity
from botbuilder.applicationinsights import ApplicationInsightsTelemetryClient
from botbuilder.applicationinsights.flask import BotTelemetryMiddleware

from dialogs import MainDialog
from bots import DialogAndWelcomeBot


LOOP = asyncio.get_event_loop()
APP = Flask(__name__, instance_relative_config=True)
APP.config.from_object("config.DefaultConfig")
APP.wsgi_app = BotTelemetryMiddleware(APP.wsgi_app)

SETTINGS = BotFrameworkAdapterSettings(APP.config["APP_ID"], APP.config["APP_PASSWORD"])
ADAPTER = BotFrameworkAdapter(SETTINGS)

# pylint:disable=unused-argument
async def on_error(context: TurnContext, error: Exception):
    """ Catch-all for errors."""
    # Send a message to the user
    await context.send_activity("Oops. Something went wrong!")
    # Clear out state
    await CONVERSATION_STATE.delete(context)


ADAPTER.on_turn_error = on_error

# Create MemoryStorage, UserState and ConversationState
MEMORY = MemoryStorage()

USER_STATE = UserState(MEMORY)
CONVERSATION_STATE = ConversationState(MEMORY)
INSTRUMENTATION_KEY = APP.config["APPINSIGHTS_INSTRUMENTATION_KEY"]
TELEMETRY_CLIENT = ApplicationInsightsTelemetryClient(INSTRUMENTATION_KEY)
DIALOG = MainDialog(APP.config, telemetry_client=TELEMETRY_CLIENT)
BOT = DialogAndWelcomeBot(CONVERSATION_STATE, USER_STATE, DIALOG, TELEMETRY_CLIENT)


@APP.route("/api/messages", methods=["POST"])
def messages():
    """Main bot message handler."""
    if request.headers["Content-Type"] == "application/json":
        body = request.json
    else:
        return Response(status=415)

    activity = Activity().deserialize(body)
    auth_header = (
        request.headers["Authorization"] if "Authorization" in request.headers else ""
    )

    async def aux_func(turn_context):
        await BOT.on_turn(turn_context)

    try:
        future = asyncio.ensure_future(
            ADAPTER.process_activity(activity, auth_header, aux_func), loop=LOOP
        )
        LOOP.run_until_complete(future)
        return Response(status=201)
    except Exception as exception:
        raise exception


if __name__ == "__main__":
    try:
        APP.run(debug=True, port=APP.config["PORT"])

    except Exception as exception:
        raise exception
