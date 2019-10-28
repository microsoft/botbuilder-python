# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

"""
This sample shows a simple Bot that echos messages back to the user.
"""
import asyncio

from flask import Flask, request, Response
from botbuilder.core import BotFrameworkAdapterSettings
from botbuilder.schema import Activity

from bots import SuggestActionsBot
from adapter_with_error_handler import AdapterWithErrorHandler

LOOP = asyncio.get_event_loop()
APP = Flask(__name__, instance_relative_config=True)
APP.config.from_object("config.DefaultConfig")

SETTINGS = BotFrameworkAdapterSettings(
    APP.config["APP_ID"], APP.config["APP_PASSWORD"]
)
ADAPTER = AdapterWithErrorHandler(SETTINGS)

BOT = SuggestActionsBot()


@APP.route("/api/messages", methods=["POST"])
def messages():
    """Main bot message handler."""
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
