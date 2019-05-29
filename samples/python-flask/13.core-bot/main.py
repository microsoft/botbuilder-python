#!/usr/bin/env python3ex
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

"""
This sample shows how to create a bot that demonstrates the following:
- Use [LUIS](https://www.luis.ai) to implement core AI capabilities.
- Implement a multi-turn conversation using Dialogs.
- Handle user interruptions for such things as `Help` or `Cancel`.
- Prompt for and validate requests for information from the user.
gi
"""
from functools import wraps
import json
import asyncio
import sys
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
        asyncio.ensure_future(bot.on_turn(turn_context))
    try:
        task = loop.create_task(ADAPTER.process_activity(activity, auth_header, aux_func))
        loop.run_until_complete(task)
        return Response(status=201)
    except Exception as e:
        raise e

if __name__ == "__main__" :
    try:
        app.run(debug=True, port=app.config["PORT"])
    except Exception as e:
        raise e

