#!/usr/bin/env python
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import asyncio
import json
from django.http import HttpResponse
from django.apps import apps
from botbuilder.schema import (Activity, ActivityTypes)

def home(request):
    return HttpResponse("Hello, Django!")

def messages(request):
    if request.headers['Content-Type'] == 'application/json':
        body = json.loads(request.body.decode("utf-8"))        
    else:
        return HttpResponse(status=415)

    activity = Activity().deserialize(body)
    auth_header = request.headers['Authorization'] if 'Authorization' in request.headers else ''
    loop = asyncio.get_event_loop()

    bot_app = apps.get_app_config('bots')
    bot = bot_app.bot
    ADAPTER = bot_app.ADAPTER

    async def aux_func(turn_context):
        asyncio.ensure_future(bot.on_turn(turn_context), loop=loop)
    try:
        task = asyncio.ensure_future(ADAPTER.process_activity(activity, auth_header, aux_func), loop=loop)
        loop.run_until_complete(task)
        return HttpResponse(status=201)
    except Exception as e:
        raise e
    return HttpResponse("This is message processing!")