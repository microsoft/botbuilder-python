# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

"""
This sample shows how to create a simple EchoBot with state.
"""

import yaml
import os
from aiohttp import web
from botbuilder.schema import (Activity, ActivityTypes)
from botbuilder.core import (BotFrameworkAdapter, BotFrameworkAdapterSettings, TurnContext,
                             ConversationState, MemoryStorage, UserState)

from dialogs import MainDialog
from bots import DialogAndWelcomeBot
from helpers.dialog_helper import DialogHelper

APP_ID = ''
APP_PASSWORD = ''
PORT = 9000
SETTINGS = BotFrameworkAdapterSettings(APP_ID, APP_PASSWORD)
ADAPTER = BotFrameworkAdapter(SETTINGS)

# Create MemoryStorage, UserState and ConversationState
memory = MemoryStorage()

user_state = UserState(memory)
conversation_state = ConversationState(memory)

relative_path = os.path.abspath(os.path.dirname(__file__))
path = os.path.join(relative_path, "config.yaml")
with open(path, 'r') as ymlfile:
    cfg = yaml.load(ymlfile)
dialog = MainDialog(cfg['settings'])
bot = DialogAndWelcomeBot(conversation_state, user_state, dialog)

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
