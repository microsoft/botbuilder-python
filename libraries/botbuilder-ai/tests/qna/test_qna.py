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
        adapter = SimpleAdapter()
        context = TurnContext(adapter, ACTIVITY)

        endpointy = QnAMakerEndpoint('a090f9f3-2f8e-41d1-a581-4f7a49269a0c', '4a439d5b-163b-47c3-b1d1-168cc0db5608', 'https://ashleyNlpBot1-qnahost.azurewebsites.net/qnamaker')
        qna = QnAMaker(endpointy)
        optionsies = QnAMakerOptions(top=3, strict_filters=[{'name': 'movie', 'value': 'disney'}])

        r = await qna.get_answers(context, optionsies)

        # loop = asyncio.get_event_loop()
        # r = loop.run_until_complete((qna.get_answers(context, optionsies)))
        # loop.close()

        # result = qna.get_answers(context)
        # print(type(result))
        print(r)

        print('donesies!')


        # context2 = TurnContext(adapter, ACTIVITY)
        # print(context2.__dict__.update({'test': '1'}))

        # qna_ressy = {
        #     'answers': [
        #         {
        #             'questions': ['hi', 'greetings', 'good morning', 'good evening'],
        #             'answer': 'Hello!',
        #             'score': 100.0,
        #             'id': 1,
        #             'source': 'QnAMaker.tsv',
        #             'metadata': []
        #         },
        #         {
        #             'questions': ['hi', 'greetings', 'good morning', 'good evening'],
        #             'answer': 'hi!',
        #             'score': 80.0,
        #             'id': 1,
        #             'source': 'QnAMaker.tsv',
        #             'metadata': []
        #         }
        #     ],
        #     'debugInfo': None
        # }

        # my_first_ans = qna_ressy['answers'][0]

        # my_query = QueryResult(**my_first_ans)

        # print(my_query)
