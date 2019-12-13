# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import asyncio
import sys
from types import MethodType
from flask import Flask, Response, request

from botbuilder.core import (
    BotFrameworkAdapter,
    BotFrameworkAdapterSettings,
    MessageFactory,
    TurnContext,
)
from botbuilder.schema import Activity, InputHints

from .default_config import DefaultConfig
from .my_bot import MyBot


class BotApp:
    """A Flask echo bot."""

    def __init__(self):
        # Create the loop and Flask app
        self.loop = asyncio.get_event_loop()
        self.flask = Flask(__name__, instance_relative_config=True)
        self.flask.config.from_object(DefaultConfig)

        # Create adapter.
        # See https://aka.ms/about-bot-adapter to learn more about how bots work.
        self.settings = BotFrameworkAdapterSettings(
            self.flask.config["APP_ID"], self.flask.config["APP_PASSWORD"]
        )
        self.adapter = BotFrameworkAdapter(self.settings)

        # Catch-all for errors.
        async def on_error(adapter, context: TurnContext, error: Exception):
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

            # pylint: disable=protected-access
            if adapter._conversation_state:
                # If state was defined, clear it.
                await adapter._conversation_state.delete(context)

        self.adapter.on_turn_error = MethodType(on_error, self.adapter)

        # Create the main dialog
        self.bot = MyBot()

    def messages(self) -> Response:
        """Main bot message handler that listens for incoming requests."""

        if "application/json" in request.headers["Content-Type"]:
            body = request.json
        else:
            return Response(status=415)

        activity = Activity().deserialize(body)
        auth_header = (
            request.headers["Authorization"]
            if "Authorization" in request.headers
            else ""
        )

        async def aux_func(turn_context):
            await self.bot.on_turn(turn_context)

        try:
            task = self.loop.create_task(
                self.adapter.process_activity(activity, auth_header, aux_func)
            )
            self.loop.run_until_complete(task)
            return Response(status=201)
        except Exception as exception:
            raise exception

    @staticmethod
    def test() -> Response:
        """
        For test only - verify if the flask app works locally - e.g. with:
        ```bash
        curl http://127.0.0.1:3978/api/test
        ```
        You shall get:
        ```
        test
        ```
        """
        return Response(status=200, response="test\n")

    def run(self, host=None) -> None:
        try:
            self.flask.run(
                host=host, debug=False, port=self.flask.config["PORT"]
            )  # nosec debug
        except Exception as exception:
            raise exception
