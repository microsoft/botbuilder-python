# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

"""
This sample shows how to create a simple EchoBot with state.
"""
from functools import wraps
import json
import asyncio
from flask import Flask, jsonify, request, Response
from botbuilder.schema import (Activity, ActivityTypes)
from botbuilder.core import (BotFrameworkAdapter, BotFrameworkAdapterSettings, TurnContext,
                             ConversationState, MemoryStorage, UserState)

from dialogs import MainDialog
from bots import DialogAndWelcomeBot
from helpers.dialog_helper import DialogHelper

loop = asyncio.get_event_loop()
app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config.DefaultConfig')

SETTINGS = BotFrameworkAdapterSettings(app.config['APP_ID'], app.config['APP_PASSWORD'])
ADAPTER = BotFrameworkAdapter(SETTINGS)

# Create MemoryStorage, UserState and ConversationState
memory = MemoryStorage()

user_state = UserState(memory)
conversation_state = ConversationState(memory)

dialog = MainDialog(app.config)
bot = DialogAndWelcomeBot(conversation_state, user_state, dialog)

@app.route('/api/messages', methods = ['POST'])
def messages():
    
    if request.headers['Content-Type'] == 'application/json':
        body = request.json
    else:
        return Response(status=415)

    activity = Activity().deserialize(body)
    auth_header = request.headers['Authorization'] if 'Authorization' in request.headers else ''
    
    async def aux_func(turn_context):
        loop.create_task(asyncio.wait([bot.on_turn(turn_context)]))
    try:
        task = loop.create_task(ADAPTER.process_activity(activity, auth_header, aux_func))
        loop.run_until_complete(task)
        return Response(status=201)
    except Exception as e:
        raise e

try:
    app.run(debug=True, port=app.config["PORT"])
except Exception as e:
    raise e

