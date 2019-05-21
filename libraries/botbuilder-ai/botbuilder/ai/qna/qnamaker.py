# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from aiohttp import ClientSession, ClientTimeout, ClientResponse

from botbuilder.schema import Activity
from botbuilder.core import BotTelemetryClient, NullTelemetryClient, TurnContext
from copy import copy
import json, platform, requests
from typing import Dict, List, NamedTuple, Union

from .metadata import Metadata
from .query_result import QueryResult
from .qnamaker_endpoint import QnAMakerEndpoint
from .qnamaker_options import QnAMakerOptions
from .qnamaker_telemetry_client import QnAMakerTelemetryClient
from .qna_telemetry_constants import QnATelemetryConstants
from .qnamaker_trace_info import QnAMakerTraceInfo

from .. import __title__, __version__

QNAMAKER_TRACE_NAME = 'QnAMaker'
QNAMAKER_TRACE_LABEL = 'QnAMaker Trace'
QNAMAKER_TRACE_TYPE = 'https://www.qnamaker.ai/schemas/trace'

class EventData(NamedTuple):
    properties: Dict[str, str]
    metrics: Dict[str, float]

class QnAMaker(QnAMakerTelemetryClient):
    """ 
    Class used to query a QnA Maker knowledge base for answers. 
    """

    def __init__(
        self, 
        endpoint: QnAMakerEndpoint, 
        options: QnAMakerOptions = None,
        http_client: ClientSession = None,
        telemetry_client: BotTelemetryClient = None, 
        log_personal_information: bool = None
    ):
        if not isinstance(endpoint, QnAMakerEndpoint):
            raise TypeError('QnAMaker.__init__(): endpoint is not an instance of QnAMakerEndpoint')

        if endpoint.host.endswith('v2.0'):
            raise ValueError('v2.0 of QnA Maker service is no longer supported in the Bot Framework. Please upgrade your QnA Maker service at www.qnamaker.ai.')

        self._endpoint: str = endpoint
        self._is_legacy_protocol: bool = self._endpoint.host.endswith('v3.0')

        self._options = options or QnAMakerOptions()
        self._validate_options(self._options)

        instance_timeout = ClientTimeout(total=self._options.timeout/1000)
        self._req_client = http_client or ClientSession(timeout=instance_timeout)

        self._telemetry_client: Union[BotTelemetryClient, NullTelemetryClient] = telemetry_client or NullTelemetryClient()
        self._log_personal_information = log_personal_information or False

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

    async def on_qna_result(
        self,
        query_results: [QueryResult],
        turn_context: TurnContext,
        telemetry_properties: Dict[str, str] = None,
        telemetry_metrics: Dict[str, float] = None
    ):
        event_data = await self.fill_qna_event(query_results, turn_context, telemetry_properties, telemetry_metrics)

        self.telemetry_client.track_event(
            name = QnATelemetryConstants.qna_message_event,
            properties = event_data.properties,
            measurements = event_data.metrics
        )

    async def fill_qna_event(
        self,
        query_results: [QueryResult],
        turn_context: TurnContext,
        telemetry_properties: Dict[str,str] = None,
        telemetry_metrics: Dict[str,float] = None
    ) -> EventData:
        """
        Fills the event properties and metrics for the QnaMessage event for telemetry.

        :return: A tuple of event data properties and metrics that will be sent to the BotTelemetryClient.track_event() method for the QnAMessage event. The properties and metrics returned the standard properties logged with any properties passed from the get_answers() method.

        :rtype: EventData
        """

        properties: Dict[str,str] = dict()
        metrics: Dict[str, float] = dict()

        properties[QnATelemetryConstants.knowledge_base_id_property] = self._endpoint.knowledge_base_id

        text: str = turn_context.activity.text
        userName: str = turn_context.activity.from_property.name

        # Use the LogPersonalInformation flag to toggle logging PII data; text and username are common examples.
        if self.log_personal_information:
            if text:
                properties[QnATelemetryConstants.question_property] = text
            
            if userName:
                properties[QnATelemetryConstants.username_property] = userName

        # Fill in Qna Results (found or not).
        if len(query_results) > 0:
            query_result = query_results[0]

            result_properties = {
                QnATelemetryConstants.matched_question_property: json.dumps(query_result.questions),
                QnATelemetryConstants.question_id_property: str(query_result.id),
                QnATelemetryConstants.answer_property: query_result.answer,
                QnATelemetryConstants.article_found_property: 'true'
            }
            properties.update(result_properties)

            metrics[QnATelemetryConstants.score_metric] = query_result.score
        else:
            no_match_properties = {
                QnATelemetryConstants.matched_question_property : 'No Qna Question matched',
                QnATelemetryConstants.question_id_property : 'No Qna Question Id matched',
                QnATelemetryConstants.answer_property : 'No Qna Answer matched',
                QnATelemetryConstants.article_found_property : 'false'
            }
            
            properties.update(no_match_properties)

        # Additional Properties can override "stock" properties.
        if telemetry_properties:
            properties.update(telemetry_properties)

        # Additional Metrics can override "stock" metrics.
        if telemetry_metrics:
            metrics.update(telemetry_metrics)
        
        return EventData(properties=properties, metrics=metrics)

    async def get_answers(
        self, 
        context: TurnContext, 
        options: QnAMakerOptions = None, 
        telemetry_properties: Dict[str,str] = None,
        telemetry_metrics: Dict[str,int] = None
    ) -> [QueryResult]:
        """
        Generates answers from the knowledge base.
        
        :return: A list of answers for the user's query, sorted in decreasing order of ranking score.
        
        :rtype: [QueryResult]
        """

        hydrated_options = self._hydrate_options(options)
        self._validate_options(hydrated_options)
        
        result = await self._query_qna_service(context, hydrated_options)

        await self.on_qna_result(result, context, telemetry_properties, telemetry_metrics)
        
        await self._emit_trace_info(context, result, hydrated_options)

        return result

    def _validate_options(self, options: QnAMakerOptions):
        if not options.score_threshold:
            options.score_threshold = 0.3
        
        if not options.top:
            options.top = 1
        
        if options.score_threshold < 0 or options.score_threshold > 1:
            raise ValueError('Score threshold should be a value between 0 and 1')

        if options.top < 1:
            raise ValueError('QnAMakerOptions.top should be an integer greater than 0')
        
        if not options.strict_filters:
            options.strict_filters = []
        
        if not options.timeout:
            options.timeout = 100000
    
    def _hydrate_options(self, query_options: QnAMakerOptions) -> QnAMakerOptions:
        """
        Combines QnAMakerOptions passed into the QnAMaker constructor with the options passed as arguments into get_answers().
        
        :return: QnAMakerOptions with options passed into constructor overwritten by new options passed into get_answers()

        :rtype: QnAMakerOptions
        """

        hydrated_options = copy(self._options)

        if query_options:
            if (
                query_options.score_threshold != hydrated_options.score_threshold 
                and query_options.score_threshold
            ):
                hydrated_options.score_threshold = query_options.score_threshold
            
            if (query_options.top != hydrated_options.top and query_options.top != 0):
                hydrated_options.top = query_options.top
            
            if (len(query_options.strict_filters) > 0):
                hydrated_options.strict_filters = query_options.strict_filters
            
            if (query_options.timeout != hydrated_options.timeout and query_options.timeout):
                hydrated_options.timeout = query_options.timeout

        return hydrated_options
    
    async def _query_qna_service(self, turn_context: TurnContext, options: QnAMakerOptions) -> [QueryResult]:
        url = f'{ self._endpoint.host }/knowledgebases/{ self._endpoint.knowledge_base_id }/generateAnswer'
        question = {
            'question': turn_context.activity.text,
            'top': options.top,
            'scoreThreshold': options.score_threshold,
            'strictFilters': options.strict_filters
        }
        serialized_content = json.dumps(question)
        headers = self._get_headers()

        # Convert miliseconds to seconds (as other BotBuilder SDKs accept timeout value in miliseconds)
        # aiohttp.ClientSession units are in seconds
        timeout = ClientTimeout(total=options.timeout/1000)

        response = await self._req_client.post(
            url, 
            data = serialized_content, 
            headers = headers, 
            timeout = timeout
        )

        result = await self._format_qna_result(response, options)

        return result
        
    async def _emit_trace_info(self, turn_context: TurnContext, result: [QueryResult], options: QnAMakerOptions):
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
    
    async def _format_qna_result(self, result, options: QnAMakerOptions) -> [QueryResult]:
        json_res = result
        if isinstance(result, ClientResponse):
            json_res = await result.json()

        answers_within_threshold = [
            { **answer,'score': answer['score']/100 } for answer in json_res['answers'] if answer['score']/100 > options.score_threshold
        ]
        sorted_answers = sorted(answers_within_threshold, key = lambda ans: ans['score'], reverse = True)

        # The old version of the protocol returns the id in a field called qnaId
        # The following translates this old structure to the new
        if self._is_legacy_protocol:
            for answer in answers_within_threshold:
                answer['id'] = answer.pop('qnaId', None)
    
        answers_as_query_results = list(map(lambda answer: QueryResult(**answer), sorted_answers))

        return answers_as_query_results
        
    def _get_headers(self):
        headers = { 
            'Content-Type': 'application/json',
            'User-Agent': self.get_user_agent()
        }

        if self._is_legacy_protocol:
            headers['Ocp-Apim-Subscription-Key'] = self._endpoint.endpoint_key
        else:
            headers['Authorization'] = f'EndpointKey {self._endpoint.endpoint_key}'
        
        return headers
    
    def get_user_agent(self):
        package_user_agent = f'{__title__}/{__version__}'
        uname = platform.uname()
        os_version = f'{uname.machine}-{uname.system}-{uname.version}'
        py_version = f'Python,Version={platform.python_version()}'
        platform_user_agent = f'({os_version}; {py_version})'
        user_agent = f'{package_user_agent} {platform_user_agent}'
        
        return user_agent
