# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import asyncio
import sys
from types import MethodType

from flask import Flask, request, Response
from botbuilder.core import (
    BotFrameworkAdapter,
    BotFrameworkAdapterSettings,
    MessageFactory,
    TurnContext,
)
from botbuilder.schema import Activity, InputHints
from bot import MyBot

# Create the loop and Flask app
LOOP = asyncio.get_event_loop()
APP = Flask(__name__, instance_relative_config=True)
APP.config.from_object("config.DefaultConfig")

# Create adapter.
# See https://aka.ms/about-bot-adapter to learn more about how bots work.
SETTINGS = BotFrameworkAdapterSettings(APP.config["APP_ID"], APP.config["APP_PASSWORD"])
ADAPTER = BotFrameworkAdapter(SETTINGS)

# Catch-all for errors.
# pylint: disable=unused-argument
async def on_error(self, context: TurnContext, error: Exception):
    # This check writes out errors to console log .vs. app insights.
    # NOTE: In production environment, you should consider logging this to Azure
    #       application insights.
    print(f"\n [on_turn_error]: {error}", file=sys.stderr)

    # Send a message to the user
    error_message_text = "Sorry, it looks like something went wrong."
    error_message = MessageFactory.text(
        error_message_text, error_message_text, InputHints.expecting_input
    )
    await context.send_activity(error_message)


ADAPTER.on_turn_error = MethodType(on_error, ADAPTER)

# Create the main dialog
BOT = MyBot()

# Listen for incoming requests on GET / for Azure monitoring
@APP.route("/", methods=["GET"])
def ping():
    return Response(status=200)


# Listen for incoming requests on /api/messages.
@APP.route("/api/messages", methods=["POST"])
def messages():
    # Main bot message handler.
    if "application/json" in request.headers["Content-Type"]:
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
        task = LOOP.create_task(
            ADAPTER.process_activity(activity, auth_header, aux_func)
        )
        LOOP.run_until_complete(task)
        return Response(status=201)
    except Exception as exception:
        raise exception


if __name__ == "__main__":
    try:
        APP.run(debug=False, port=APP.config["PORT"])  # nosec debug
    except Exception as exception:
        raise exception
