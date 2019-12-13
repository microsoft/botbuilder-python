# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from aiohttp import web
from aiohttp.web import Request, Response

from botframework.connector.auth import AuthenticationConfiguration, SimpleCredentialProvider
from botbuilder.core import BotFrameworkHttpClient
from botbuilder.core.integration import aiohttp_channel_service_routes
from botbuilder.schema import Activity

from config import DefaultConfig
from routing_id_factory import RoutingIdFactory
from routing_handler import RoutingHandler


CONFIG = DefaultConfig()
CREDENTIAL_PROVIDER = SimpleCredentialProvider(CONFIG.APP_ID, CONFIG.APP_PASSWORD)
CLIENT = BotFrameworkHttpClient(CREDENTIAL_PROVIDER)
AUTH_CONFIG = AuthenticationConfiguration()

TO_URI = CONFIG.NEXT
SERVICE_URL = CONFIG.SERVICE_URL

FACTORY = RoutingIdFactory()

ROUTING_HANDLER = RoutingHandler(FACTORY, CREDENTIAL_PROVIDER, AUTH_CONFIG)


async def messages(req: Request) -> Response:
    # Main bot message handler.
    if "application/json" in req.headers["Content-Type"]:
        body = await req.json()
    else:
        return Response(status=415)

    inbound_activity: Activity = Activity().deserialize(body)

    current_conversation_id = inbound_activity.conversation.id
    current_service_url = inbound_activity.service_url

    next_conversation_id = FACTORY.create_skill_conversation_id(current_conversation_id, current_service_url)

    await CLIENT.post_activity(CONFIG.APP_ID, CONFIG.SKILL_APP_ID, TO_URI, SERVICE_URL, next_conversation_id, inbound_activity)
    return Response(status=201)

APP = web.Application()

APP.router.add_post("/api/messages", messages)
APP.router.add_routes(aiohttp_channel_service_routes(ROUTING_HANDLER, "/api/connector"))

if __name__ == "__main__":
    try:
        web.run_app(APP, host="localhost", port=CONFIG.PORT)
    except Exception as error:
        raise error
