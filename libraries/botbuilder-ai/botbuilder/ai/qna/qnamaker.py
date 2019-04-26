# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.schema import Activity, ChannelAccount, ResourceResponse, ConversationAccount
from botbuilder.core import BotAdapter, BotTelemetryClient, NullTelemetryClient, TurnContext
# import http.client, urllib.parse, json, time, urllib.request
import json, requests
from copy import copy
from typing import Dict, List, Tuple
from enum import Enum

import asyncio
from abc import ABC, abstractmethod

# from . import(
#     QnATelemetryConstants
# )

QNAMAKER_TRACE_TYPE = 'https://www.qnamaker.ai/schemas/trace'
QNAMAKER_TRACE_NAME = 'QnAMaker'
QNAMAKER_TRACE_LABEL = 'QnAMaker Trace'

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

class QnATelemetryConstants(str, Enum):
    """
    The IBotTelemetryClient event and property names that logged by default.
    """

    qna_message_event = 'QnaMessage'
    """Event name"""
    knowledge_base_id_property = 'knowledgeBaseId'
    answer_property = 'answer'
    article_found_property = 'articleFound'
    channel_id_property = 'channelId'
    conversation_id_property = 'conversationId'
    question_property = 'question'
    matched_question_property = 'matchedQuestion'
    question_id_property = 'questionId'
    score_metric = 'score'
    username_property = 'username'

class QnAMakerTelemetryClient(ABC):
    def __init__(
        self, 
        log_personal_information: bool, 
        telemetry_client: BotTelemetryClient
    ):
        self.log_personal_information = log_personal_information,
        self.telemetry_client = telemetry_client
    
    @abstractmethod
    def get_answers(
        self, 
        context: TurnContext, 
        options: QnAMakerOptions = None, 
        telemetry_properties: Dict[str,str] = None, 
        telemetry_metrics: Dict[str, float] = None
    ):
        raise NotImplementedError('QnAMakerTelemetryClient.get_answers(): is not implemented.')

class QnAMakerTraceInfo:
    def __init__(
        self, 
        message: Activity, 
        query_results: [QueryResult], 
        knowledge_base_id, 
        score_threshold, 
        top, 
        strict_filters
    ):
        self.message = message,
        self.query_results = query_results,
        self.knowledge_base_id = knowledge_base_id,
        self.score_threshold = score_threshold,
        self.top = top,
        self.strict_filters = strict_filters

class QnAMaker(QnAMakerTelemetryClient):
    def __init__(
        self, 
        endpoint: QnAMakerEndpoint, 
        options: QnAMakerOptions = QnAMakerOptions(), 
        telemetry_client: BotTelemetryClient = None, 
        log_personal_information: bool = None
    ):
        self._endpoint = endpoint
        self._is_legacy_protocol: bool = self._endpoint.host.endswith('v3.0')
        self._options: QnAMakerOptions = options
        self._telemetry_client = telemetry_client or NullTelemetryClient()
        self._log_personal_information = log_personal_information or False

        self.validate_options(self._options)
    
    @property
    def log_personal_information(self) -> bool:
        """Gets a value indicating whether to log personal information that came from the user to telemetry.
        
        :return: If True, personal information is logged to Telemetry; otherwise the properties will be filtered.
        :rtype: bool
        """

        return self._log_personal_information

    @log_personal_information.setter
    def log_personal_information(self, value: bool) -> None:
        """Sets a value indicating whether to log personal information that came from the user to telemetry.
        
        :param value: If True, personal information is logged to Telemetry; otherwise the properties will be filtered.
        :type value: bool
        :return:
        :rtype: None
        """

        self._log_personal_information = value

    @property
    def telemetry_client(self) -> BotTelemetryClient:
        """Gets the currently configured BotTelemetryClient that logs the event.
        
        :return: The BotTelemetryClient being used to log events.
        :rtype: BotTelemetryClient
        """

        return self._telemetry_client

    @telemetry_client.setter
    def telemetry_client(self, value: BotTelemetryClient):
        """Sets the currently configured BotTelemetryClient that logs the event.
        
        :param value: The BotTelemetryClient being used to log events.
        :type value: BotTelemetryClient
        """

        self._telemetry_client = value

    async def on_qna_result(self):
        # event_data = await fill_qna_event()
        pass

    async def fill_qna_event(
        self,
        query_results: [QueryResult],
        turn_context: TurnContext,
        telemetry_properties: Dict[str,str] = None,
        telemetry_metrics: Dict[str,float] = None
    ) -> Tuple[ Dict[str, str], Dict[str,int] ]:
        
        properties: Dict[str,str] = dict()
        metrics: Dict[str, float] = dict()

        properties[QnATelemetryConstants.knowledge_base_id_property] = self._endpoint.knowledge_base_id

        pass

    async def get_answers(
        self, 
        context: TurnContext, 
        options: QnAMakerOptions = None, 
        telemetry_properties: Dict[str,str] = None,
        telemetry_metrics: Dict[str,int] = None
    ):
        # add timeout
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
    
    def hydrate_options(self, query_options: QnAMakerOptions) -> QnAMakerOptions:
        hydrated_options = copy(self._options)

        if query_options:
            if (query_options.score_threshold != hydrated_options.score_threshold and query_options.score_threshold):
                hydrated_options.score_threshold = query_options.score_threshold
            
            if (query_options.top != hydrated_options.top and query_options.top != 0):
                hydrated_options.top = query_options.top
            
            if (len(query_options.strict_filters) > 0):
                hydrated_options.strict_filters = query_options.strict_filters

        return hydrated_options
    
    def query_qna_service(self, message_activity: Activity, options: QnAMakerOptions) -> [QueryResult]:
        url = f'{ self._endpoint.host }/knowledgebases/{ self._endpoint.knowledge_base_id }/generateAnswer'

        question = {
            'question': message_activity.text,
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
    
    def format_qna_result(self, qna_result: requests.Response, options: QnAMakerOptions) -> [QueryResult]:
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
        