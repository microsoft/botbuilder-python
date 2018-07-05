# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from aiohttp import web
from botbuilder.schema import (Activity, ActivityTypes)
from botbuilder.core import (BotFrameworkAdapter, BotFrameworkAdapterSettings, TurnContext)

APP_ID = ''
APP_PASSWORD = ''
PORT = 9000
SETTINGS = BotFrameworkAdapterSettings(APP_ID, APP_PASSWORD)
ADAPTER = BotFrameworkAdapter(SETTINGS)


async def create_reply_activity(request_activity, text) -> Activity:
    return Activity(
        type=ActivityTypes.message,
        channel_id=request_activity.channel_id,
        conversation=request_activity.conversation,
        recipient=request_activity.from_property,
        from_property=request_activity.recipient,
        text=text,
        service_url=request_activity.service_url)


async def handle_message(context: TurnContext) -> web.Response:
    response = await create_reply_activity(context.request, 'You said %s.' % context.request.text)
    await context.send_activity(response)
    return web.Response(status=202)


async def handle_conversation_update(context: TurnContext) -> web.Response:
    if context.request.members_added[0].id != context.request.recipient.id:
        response = await create_reply_activity(context.request, 'Welcome to the Echo Adapter Bot!')
        await context.send_activity(response)
    return web.Response(status=200)


async def unhandled_activity() -> web.Response:
    return web.Response(status=404)


async def request_handler(context: TurnContext) -> web.Response:
    if context.request.type == 'message':
        return await handle_message(context)
    elif context.request.type == 'conversationUpdate':
        return await handle_conversation_update(context)
    else:
        return await unhandled_activity()


async def messages(req: web.web_request) -> web.Response:
    body = await req.json()
    activity = Activity().deserialize(body)
    auth_header = req.headers['Authorization'] if 'Authorization' in req.headers else ''
    try:
        return await ADAPTER.process_request(activity, auth_header, request_handler)
    except Exception as e:
        raise e


app = web.Application()
app.router.add_post('/', messages)

try:
    web.run_app(app, host='localhost', port=PORT)
except Exception as e:
    raise e
