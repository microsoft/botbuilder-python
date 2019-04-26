# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.schema import Activity, ChannelAccount, ResourceResponse, ConversationAccount
from botbuilder.core import BotAdapter, BotTelemetryClient, NullTelemetryClient, TurnContext
# import http.client, urllib.parse, json, time, urllib.request
import json, requests
from copy import copy
from typing import Dict
import asyncio
from abc import ABC, abstractmethod

QNAMAKER_TRACE_TYPE = 'https://www.qnamaker.ai/schemas/trace'
QNAMAKER_TRACE_NAME = 'QnAMaker'
QNAMAKER_TRACE_LABEL = 'QnAMaker Trace'

# DELETE YO
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

ACTIVITY = Activity(id='1234',
                    type='message',
                    text='up',
                    from_property=ChannelAccount(id='user', name='User Name'),
                    recipient=ChannelAccount(id='bot', name='Bot Name'),
                    conversation=ConversationAccount(id='convo', name='Convo Name'),
                    channel_id='UnitTest',
                    service_url='https://example.org'
                    )

class Metadata:
    def __init__(self, name, value):
        self.name = name
        self.value = value

class QueryResult:
    def __init__(self, questions: str, answer: str, score: float, metadata: [Metadata], source: str, id: int):
        self.questions = questions,
        self.answer = answer,
        self.score = score,
        self.metadata = Metadata,
        self.source = source
        self.id = id

class QnAMakerEndpoint:
    def __init__(self, knowledge_base_id: str, endpoint_key: str, host: str):
        self.knowledge_base_id = knowledge_base_id
        self.endpoint_key = endpoint_key
        self.host = host

# figure out if 300 milliseconds is ok for python requests library...or 100000
class QnAMakerOptions:
    def __init__(self, score_threshold: float = 0.0, timeout: int = 0, top: int = 0, strict_filters: [Metadata] = []):
        self.score_threshold = score_threshold
        self.timeout = timeout
        self.top = top
        self.strict_filters = strict_filters

class QnAMakerTelemetryClient(ABC):
    def __init__(self, log_personal_information: bool, telemetry_client: BotTelemetryClient):
        self.log_personal_information = log_personal_information,
        self.telemetry_client = telemetry_client
    
    @abstractmethod
    def get_answers(self, context: TurnContext, options: QnAMakerOptions = None, telemetry_properties: Dict[str,str] = None, telemetry_metrics: Dict[str, int] = None):
        raise NotImplementedError('QnAMakerTelemetryClient.get_answers(): is not implemented.')

class QnAMakerTraceInfo:
    def __init__(self, message, query_results, knowledge_base_id, score_threshold, top, strict_filters):
        self.message = message,
        self.query_results = query_results,
        self.knowledge_base_id = knowledge_base_id,
        self.score_threshold = score_threshold,
        self.top = top,
        self.strict_filters = strict_filters

class QnAMaker():
    def __init__(self, endpoint: QnAMakerEndpoint, options: QnAMakerOptions = QnAMakerOptions()):
        self._endpoint = endpoint
        self._is_legacy_protocol: bool = self._endpoint.host.endswith('v3.0')
        self._options: QnAMakerOptions = options
        self.validate_options(self._options)

    
    async def get_answers(self, context: TurnContext, options: QnAMakerOptions = None):
        # don't forget to add timeout
        # maybe omit metadata boost?
        hydrated_options = self.hydrate_options(options)
        self.validate_options(hydrated_options)
        
        result = self.query_qna_service(context.activity, hydrated_options)
        
        await self.emit_trace_info(context, result, hydrated_options)

        return result

    def validate_options(self, options: QnAMakerOptions):
        if not options.score_threshold:
            options.score_threshold = 0.3
        
        if not options.top:
            options.top = 1
        
        # write range error for if scorethreshold < 0 or > 1

        if not options.timeout:
            options.timeout = 100000 # check timeout units in requests module
        
        # write range error for if top < 1
        
        if not options.strict_filters:
            options.strict_filters = [Metadata]
    
    def hydrate_options(self, query_options: QnAMakerOptions):
        hydrated_options = copy(self._options)

        if query_options:
            if (query_options.score_threshold != hydrated_options.score_threshold and query_options.score_threshold):
                hydrated_options.score_threshold = query_options.score_threshold
            
            if (query_options.top != hydrated_options.top and query_options.top != 0):
                hydrated_options.top = query_options.top
            
            if (len(query_options.strict_filters) > 0):
                hydrated_options.strict_filters = query_options.strict_filters

        return hydrated_options
    
    def query_qna_service(self, message_activity: Activity, options: QnAMakerOptions):
        url = f'{ self._endpoint.host }/knowledgebases/{ self._endpoint.knowledge_base_id }/generateAnswer'

        question = {
            'question': context.activity.text,
            'top': options.top,
            'scoreThreshold': options.score_threshold,
            'strictFilters': options.strict_filters
        }
        
        serialized_content = json.dumps(question)

        headers = self.get_headers()

        response = requests.post(url, data=serialized_content, headers=headers)
        
        result = self.format_qna_result(response, options)
        
        return result
    
    async def emit_trace_info(self, turn_context: TurnContext, result: [QueryResult], options: QnAMakerOptions):
        trace_info = QnAMakerTraceInfo(
            message = turn_context.activity,
            query_results = result,
            knowledge_base_id = self._endpoint.knowledge_base_id,
            score_threshold = options.score_threshold,
            top = options.top,
            strict_filters = options.strict_filters
        )
        
        trace_activity = Activity(
            label = QNAMAKER_TRACE_LABEL,
            name = QNAMAKER_TRACE_NAME,
            type = 'trace',
            value = trace_info,
            value_type = QNAMAKER_TRACE_TYPE
        )

        await turn_context.send_activity(trace_activity)
    
    def format_qna_result(self, qna_result: requests.Response, options: QnAMakerOptions):
        result = qna_result.json()

        answers_within_threshold = [
            { **answer,'score': answer['score']/100 } for answer in result['answers'] 
            if answer['score']/100 > options.score_threshold
        ]
        sorted_answers = sorted(answers_within_threshold, key = lambda ans: ans['score'], reverse = True)

        if self._is_legacy_protocol:
            for answer in answers_within_threshold:
                answer['id'] = answer.pop('qnaId', None)
    
        answers_as_query_results = list(map(lambda answer: QueryResult(**answer), sorted_answers))

        return answers_as_query_results

    def get_headers(self):
        headers = { 'Content-Type': 'application/json' }

        if self._is_legacy_protocol:
            headers['Ocp-Apim-Subscription-Key'] = self._endpoint.endpoint_key
        else:
            headers['Authorization'] = f'EndpointKey {self._endpoint.endpoint_key}'
        # need user-agent header
        return headers
        

        

  
    
adapter = SimpleAdapter()
context = TurnContext(adapter, ACTIVITY)

endpointy = QnAMakerEndpoint('a090f9f3-2f8e-41d1-a581-4f7a49269a0c', '4a439d5b-163b-47c3-b1d1-168cc0db5608', 'https://ashleyNlpBot1-qnahost.azurewebsites.net/qnamaker')
qna = QnAMaker(endpointy)
optionsies = QnAMakerOptions(top=3, strict_filters=[{'name': 'movie', 'value': 'disney'}])

loop = asyncio.get_event_loop()
r = loop.run_until_complete((qna.get_answers(context, optionsies)))
loop.close()

# result = qna.get_answers(context)
# print(type(result))
# print(r)

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