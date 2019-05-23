# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

"""
This sample shows how to use different types of rich cards.
"""
import os
import yaml
import sys

from aiohttp import web
from botbuilder.schema import Activity, ActivityTypes
from botbuilder.core import (BotFrameworkAdapter, BotFrameworkAdapterSettings, TurnContext,
                             ConversationState, MemoryStorage, UserState, CardFactory)

from dialogs import MainDialog
from bots import RichCardsBot

relative_path = os.path.abspath(os.path.dirname(__file__))
path = os.path.join(relative_path, "config.yaml")
with open(path, 'r') as ymlfile:
    cfg = yaml.safe_load(ymlfile)

PORT = cfg['Settings']['Port']
SETTINGS = BotFrameworkAdapterSettings(cfg['Settings']['AppId'], cfg['Settings']['AppPassword'])
ADAPTER = BotFrameworkAdapter(SETTINGS)

# Catch-all for errors.
async def on_error(context: TurnContext, error: Exception):
    # This check writes out errors to console log
    # NOTE: In production environment, you should consider logging this to Azure
    #       application insights.
    print(f'\n [on_turn_error]: { error }', file=sys.stderr)
    # Send a message to the user
    await context.send_activity('Oops. Something went wrong!')
    # Clear out state
    await conversation_state.delete(context)

ADAPTER.on_turn_error = on_error

# Create MemoryStorage, UserState and ConversationState
memory = MemoryStorage()

# Commented out user_state because it's not being used.
user_state = UserState(memory)
conversation_state = ConversationState(memory)


dialog = MainDialog()
bot = RichCardsBot(conversation_state, user_state, dialog)

async def messages(req: web.Request) -> web.Response:
    body = await req.json()
    activity = Activity().deserialize(body)
    auth_header = req.headers['Authorization'] if 'Authorization' in req.headers else ''
    async def aux_func(turn_context):
        await bot.on_turn(turn_context)

    try:
        await ADAPTER.process_activity(activity, auth_header, aux_func)
        return web.Response(status=200)
    except Exception as e:
        raise e


app = web.Application()
app.router.add_post('/api/messages', messages)

try:
    web.run_app(app, host='localhost', port=PORT)
except Exception as e:
    raise e
