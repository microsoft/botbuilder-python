# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import sys
import traceback

from aiohttp import web
from aiohttp.web import Request, Response
from aiohttp.web_response import json_response
from botbuilder.core import (
    BotFrameworkAdapterSettings,
    MemoryStorage,
    TurnContext,
    BotFrameworkAdapter,
)
from botbuilder.core.integration import (
    aiohttp_channel_service_routes,
    aiohttp_error_middleware,
    BotFrameworkHttpClient
)
from botbuilder.core.skills import SkillHandler
from botbuilder.schema import Activity
from botframework.connector.auth import (
    AuthenticationConfiguration,
    SimpleCredentialProvider,
)

from bots.parent_bot import ParentBot
from skill_conversation_id_factory import SkillConversationIdFactory
from config import DefaultConfig

CONFIG = DefaultConfig()

# Create adapter.
# See https://aka.ms/about-bot-adapter to learn more about how bots work.
SETTINGS = BotFrameworkAdapterSettings(
    app_id=CONFIG.APP_ID, app_password=CONFIG.APP_PASSWORD,
)
ADAPTER = BotFrameworkAdapter(SETTINGS)

CREDENTIAL_PROVIDER = SimpleCredentialProvider(CONFIG.APP_ID, CONFIG.APP_PASSWORD)
CLIENT = BotFrameworkHttpClient(CREDENTIAL_PROVIDER)


# Catch-all for errors.
async def on_error(context: TurnContext, error: Exception):
    # This check writes out errors to console log .vs. app insights.
    # NOTE: In production environment, you should consider logging this to Azure
    #       application insights.
    print(f"\n [on_turn_error] unhandled error: {error}", file=sys.stderr)
    traceback.print_exc()

    # Send a message to the user
    await context.send_activity("The bot encountered an error or bug.")
    await context.send_activity(
        "To continue to run this bot, please fix the bot source code."
    )


ADAPTER.on_turn_error = on_error

# Create the Bot
BOT = ParentBot(CLIENT)

STORAGE = MemoryStorage()
ID_FACTORY = SkillConversationIdFactory(STORAGE)
SKILL_HANDLER = SkillHandler(
    ADAPTER, BOT, ID_FACTORY, CREDENTIAL_PROVIDER, AuthenticationConfiguration()
)


# Listen for incoming requests on /api/messages
async def messages(req: Request) -> Response:
    # Main bot message handler.
    if "application/json" in req.headers["Content-Type"]:
        body = await req.json()
    else:
        return Response(status=415)

    activity = Activity().deserialize(body)
    auth_header = req.headers["Authorization"] if "Authorization" in req.headers else ""

    try:
        response = await ADAPTER.process_activity(activity, auth_header, BOT.on_turn)
        if response:
            return json_response(data=response.body, status=response.status)
        return Response(status=201)
    except Exception as exception:
        raise exception


APP = web.Application(middlewares=[aiohttp_error_middleware])
APP.router.add_post("/api/messages", messages)
APP.router.add_routes(aiohttp_channel_service_routes(SKILL_HANDLER, "/api/skills"))

if __name__ == "__main__":
    try:
        web.run_app(APP, host="localhost", port=CONFIG.PORT)
    except Exception as error:
        raise error
