# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import json
import aiounittest
from typing import List, Tuple
from uuid import uuid4
from botbuilder.schema import Activity, ChannelAccount, ResourceResponse, ConversationAccount
from botbuilder.core import BotAdapter, BotTelemetryClient, NullTelemetryClient, TurnContext
from botbuilder.ai.qna import QnAMakerEndpoint, QnAMaker, QnAMakerOptions
# DELETE YO
ACTIVITY = Activity(id='1234',
                    type='message',
                    text='up',
                    from_property=ChannelAccount(id='user', name='User Name'),
                    recipient=ChannelAccount(id='bot', name='Bot Name'),
                    conversation=ConversationAccount(id='convo', name='Convo Name'),
                    channel_id='UnitTest',
                    service_url='https://example.org'
                    )

class SimpleAdapter(BotAdapter):
    async def send_activities(self, context, activities):
        responses = []
        for (idx, activity) in enumerate(activities):
            responses.append(ResourceResponse(id='5678'))
        return responses

    async def update_activity(self, context, activity):
        assert context is not None
        assert activity is not None

    async def delete_activity(self, context, reference):
        assert context is not None
        assert reference is not None
        assert reference.activity_id == '1234'

class QnaApplicationTest(aiounittest.AsyncTestCase):

    async def test_initial_test(self):
        pass