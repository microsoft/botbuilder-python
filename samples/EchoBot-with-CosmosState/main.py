# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

"""This sample shows how to create a simple EchoBot with state in CosmosDB."""


from aiohttp import web
from botbuilder.schema import (Activity, ActivityTypes)
from botbuilder.core import (BotFrameworkAdapter,
                             BotFrameworkAdapterSettings, TurnContext,
                             ConversationState)
from botbuilder.azure import (CosmosDbStorage, CosmosDbConfig)

APP_ID = ''
APP_PASSWORD = ''
PORT = 9000
SETTINGS = BotFrameworkAdapterSettings(APP_ID, APP_PASSWORD)
ADAPTER = BotFrameworkAdapter(SETTINGS)
CONFIG_FILE = 'sample_credentials_file.json'

# Create CosmosStorage and ConversationState
cosmos = CosmosDbStorage(CosmosDbConfig(filename=CONFIG_FILE))
# Commented out user_state because it's not being used.
# user_state = UserState(memory)
conversation_state = ConversationState(cosmos)

# Register both State middleware on the adapter.
# Commented out user_state because it's not being used.
# ADAPTER.use(user_state)
ADAPTER.use(conversation_state)


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
    # Access the state for the conversation between the user and the bot.
    state = await conversation_state.get(context)
    previous = None
    if hasattr(state, 'previous_text'):
        previous = state.previous_text
    if hasattr(state, 'counter'):
        state.counter += 1
    else:
        state.counter = 1
    state.previous_text = context.activity.text
    if previous:
        response_text = f'{state.counter}: You said {context.activity.text}. \
            Earlier you said {previous}'
    else:
        response_text = f'{state.counter}: You said {context.activity.text}.'
    response = await create_reply_activity(context.activity, response_text)
    await context.send_activity(response)
    return web.Response(status=202)


async def handle_conversation_update(context: TurnContext) -> web.Response:
    if context.activity.members_added[0].id != context.activity.recipient.id:
        response = await create_reply_activity(context.activity, 'Welcome to \
            the Echo Adapter Bot!')
        await context.send_activity(response)
    return web.Response(status=200)


async def unhandled_activity() -> web.Response:
    return web.Response(status=404)


async def request_handler(context: TurnContext) -> web.Response:
    if context.activity.type == 'message':
        return await handle_message(context)
    elif context.activity.type == 'conversationUpdate':
        return await handle_conversation_update(context)
    else:
        return await unhandled_activity()


async def messages(req: web.web_request) -> web.Response:
    body = await req.json()
    activity = Activity().deserialize(body)
    auth_header = (req.headers['Authorization']
                   if 'Authorization' in req.headers else '')
    try:
        return await ADAPTER.process_activity(activity,
                                              auth_header, request_handler)
    except Exception as e:
        raise e


app = web.Application()
app.router.add_post('/', messages)

try:
    web.run_app(app, host='localhost', port=PORT)
except Exception as e:
    raise e
