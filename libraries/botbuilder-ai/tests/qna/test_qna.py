# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import json
import aiounittest, unittest, requests
from os import path
from requests.models import Response
from typing import List, Tuple
from uuid import uuid4
from unittest.mock import Mock, patch, MagicMock
from asyncio import Future
from aiohttp import ClientSession, ClientTimeout

from botbuilder.ai.qna import Metadata, QnAMakerEndpoint, QnAMaker, QnAMakerOptions, QnATelemetryConstants, QueryResult
from botbuilder.core import BotAdapter, BotTelemetryClient, NullTelemetryClient, TurnContext
from botbuilder.core.adapters import TestAdapter
from botbuilder.schema import Activity, ActivityTypes, ChannelAccount, ResourceResponse, ConversationAccount
 
class TestContext(TurnContext):
    def __init__(self, request):
        super().__init__(TestAdapter(), request)
        self.sent: List[Activity] = list()

        self.on_send_activities(self.capture_sent_activities)

    async def capture_sent_activities(self, context: TurnContext, activities, next):
        self.sent += activities
        context.responded = True

class QnaApplicationTest(aiounittest.AsyncTestCase):
    # Note this is NOT a real LUIS application ID nor a real LUIS subscription-key
    # theses are GUIDs edited to look right to the parsing and validation code.
    _knowledge_base_id: str = 'f028d9k3-7g9z-11d3-d300-2b8x98227q8w'
    _endpoint_key: str = '1k997n7w-207z-36p3-j2u1-09tas20ci6011'
    _host: str = 'https://dummyqnahost.azurewebsites.net/qnamaker'

    tests_endpoint = QnAMakerEndpoint(_knowledge_base_id, _endpoint_key, _host)


    def test_qnamaker_construction(self):
        # Arrange
        endpoint = self.tests_endpoint

        # Act
        qna = QnAMaker(endpoint)
        endpoint = qna._endpoint

        # Assert
        self.assertEqual('f028d9k3-7g9z-11d3-d300-2b8x98227q8w', endpoint.knowledge_base_id)
        self.assertEqual('1k997n7w-207z-36p3-j2u1-09tas20ci6011', endpoint.endpoint_key)
        self.assertEqual('https://dummyqnahost.azurewebsites.net/qnamaker', endpoint.host)

    def test_endpoint_with_empty_kbid(self):
        empty_kbid = ''

        with self.assertRaises(TypeError):
            QnAMakerEndpoint(
                empty_kbid,
                self._endpoint_key,
                self._host
        )
    
    def test_endpoint_with_empty_endpoint_key(self):
        empty_endpoint_key = ''

        with self.assertRaises(TypeError):
            QnAMakerEndpoint(
                self._knowledge_base_id,
                empty_endpoint_key,
                self._host
            )

    def test_endpoint_with_emptyhost(self):
        with self.assertRaises(TypeError):
            QnAMakerEndpoint(
                self._knowledge_base_id,
                self._endpoint_key,
                ''
            )
    
    def test_qnamaker_with_none_endpoint(self):
        with self.assertRaises(TypeError):
            QnAMaker(None)
    
    def test_v2_legacy_endpoint(self):
        v2_hostname = 'https://westus.api.cognitive.microsoft.com/qnamaker/v2.0'

        v2_legacy_endpoint = QnAMakerEndpoint(
            self._knowledge_base_id,
            self._endpoint_key,
            v2_hostname
        )

        with self.assertRaises(ValueError):
            QnAMaker(v2_legacy_endpoint)
    
    def test_legacy_protocol(self):
        v3_hostname = 'https://westus.api.cognitive.microsoft.com/qnamaker/v3.0'
        v3_legacy_endpoint = QnAMakerEndpoint(
            self._knowledge_base_id,
            self._endpoint_key,
            v3_hostname
        )
        legacy_qna = QnAMaker(v3_legacy_endpoint)
        is_legacy = True

        v4_hostname = 'https://UpdatedNonLegacyQnaHostName.azurewebsites.net/qnamaker'
        nonlegacy_endpoint = QnAMakerEndpoint(
            self._knowledge_base_id,
            self._endpoint_key,
            v4_hostname
        )
        v4_qna = QnAMaker(nonlegacy_endpoint)

        self.assertEqual(is_legacy, legacy_qna._is_legacy_protocol)
        self.assertNotEqual(is_legacy, v4_qna._is_legacy_protocol)

    def test_set_default_options_with_no_options_arg(self):
        qna_without_options = QnAMaker(self.tests_endpoint)

        options = qna_without_options._options

        default_threshold = 0.3
        default_top = 1
        default_strict_filters = []

        self.assertEqual(default_threshold, options.score_threshold)
        self.assertEqual(default_top, options.top)
        self.assertEqual(default_strict_filters, options.strict_filters)

    def test_options_passed_to_ctor(self):
        options = QnAMakerOptions(
            score_threshold=0.8,
            timeout=9000,
            top=5,
            strict_filters=[Metadata('movie', 'disney')]
        )

        qna_with_options = QnAMaker(self.tests_endpoint, options)
        actual_options = qna_with_options._options

        expected_threshold = 0.8
        expected_timeout = 9000
        expected_top = 5
        expected_strict_filters = [Metadata('movie', 'disney')]

        self.assertEqual(expected_threshold, actual_options.score_threshold)
        self.assertEqual(expected_timeout, actual_options.timeout)
        self.assertEqual(expected_top, actual_options.top)
        self.assertEqual(expected_strict_filters[0].name, actual_options.strict_filters[0].name)
        self.assertEqual(expected_strict_filters[0].value, actual_options.strict_filters[0].value)

    async def test_returns_answer(self):
        # Arrange
        question: str = 'how do I clean the stove?'
        response_path: str = 'ReturnsAnswer.json'

        # Act
        result = await QnaApplicationTest._get_service_result(
            question, 
            response_path
        )

        first_answer = result['answers'][0]

        # If question yields no questions in KB
        # QnAMaker v4.0 API returns 'answer': 'No good match found in KB.' and questions: []
        no_ans_found_in_kb = False
        if len(result['answers']) and first_answer['score'] == 0:
            no_ans_found_in_kb = True
        
        #Assert
        self.assertIsNotNone(result)
        self.assertEqual(1, len(result['answers']))
        self.assertTrue(question in first_answer['questions'] or no_ans_found_in_kb)
        self.assertEqual('BaseCamp: You can use a damp rag to clean around the Power Pack', first_answer['answer'])

    async def test_returns_answer_using_options(self):
        # Arrange
        question: str = 'up'
        response_path: str = 'AnswerWithOptions.json'
        options = QnAMakerOptions(
            score_threshold = 0.8,
            top = 5,
            strict_filters = [{
                'name': 'movie',
                'value': 'disney'
            }]
        )

        # Act
        result = await QnaApplicationTest._get_service_result(
            question, 
            response_path, 
            options=options
        )

        first_answer = result['answers'][0]
        has_at_least_1_ans = True
        first_metadata = first_answer['metadata'][0]

        # Assert
        self.assertIsNotNone(result)
        self.assertEqual(has_at_least_1_ans,  len(result) >= 1 and len(result) <= options.top)
        self.assertTrue(question in first_answer['questions'])
        self.assertTrue(first_answer['answer'])
        self.assertEqual('is a movie', first_answer['answer'])
        self.assertTrue(first_answer['score'] >= options.score_threshold)
        self.assertEqual('movie', first_metadata['name'])
        self.assertEqual('disney', first_metadata['value'])
    
    async def test_trace_test(self):
        activity = Activity(
            type = ActivityTypes.message,
            text = 'how do I clean the stove?',
            conversation = ConversationAccount(),
            recipient = ChannelAccount(),
            from_property = ChannelAccount(),
        )

        response_json = QnaApplicationTest._get_json_for_file('ReturnsAnswer.json')
        qna = QnAMaker(QnaApplicationTest.tests_endpoint)

        context = TestContext(activity)
        response = Mock(spec=Response)
        response.status_code = 200
        response.headers = {}
        response.reason = ''

        with patch('aiohttp.ClientSession.post', return_value=response):
            with patch('botbuilder.ai.qna.QnAMaker._query_qna_service', return_value=aiounittest.futurized(response_json)):
                result = await qna.get_answers(context)
                
                qna_trace_activities = list(filter(lambda act: act.type == 'trace' and act.name == 'QnAMaker', context.sent))
                trace_activity = qna_trace_activities[0]

                self.assertEqual('trace', trace_activity.type)
                self.assertEqual('QnAMaker', trace_activity.name)
                self.assertEqual('QnAMaker Trace', trace_activity.label)
                self.assertEqual('https://www.qnamaker.ai/schemas/trace', trace_activity.value_type)
                self.assertEqual(True, hasattr(trace_activity, 'value'))
                self.assertEqual(True, hasattr(trace_activity.value, 'message'))
                self.assertEqual(True, hasattr(trace_activity.value, 'query_results'))
                self.assertEqual(True, hasattr(trace_activity.value, 'score_threshold'))
                self.assertEqual(True, hasattr(trace_activity.value, 'top'))
                self.assertEqual(True, hasattr(trace_activity.value, 'strict_filters'))
                self.assertEqual(self._knowledge_base_id, trace_activity.value.knowledge_base_id[0])

                return result

    async def test_returns_answer_with_timeout(self):
        question: str = 'how do I clean the stove?'
        options = QnAMakerOptions(timeout=999999)
        qna = QnAMaker(QnaApplicationTest.tests_endpoint, options)
        context = QnaApplicationTest._get_context(question, TestAdapter())
        response = Mock(spec=Response)
        response.status_code = 200
        response.headers = {}
        response.reason = ''
        response_json = QnaApplicationTest._get_json_for_file('ReturnsAnswer.json')

        with patch('aiohttp.ClientSession.post', return_value=response):
            with patch('botbuilder.ai.qna.QnAMaker._query_qna_service', return_value=aiounittest.futurized(response_json)):
                result = await qna.get_answers(context, options)
                
                self.assertIsNotNone(result)
                self.assertEqual(options.timeout, qna._options.timeout)



    @classmethod
    async def _get_service_result(
        cls,
        utterance: str,
        response_file: str,
        bot_adapter: BotAdapter = TestAdapter(),
        options: QnAMakerOptions = None
    ) -> [dict]:
        response_json =  QnaApplicationTest._get_json_for_file(response_file)
        
        qna = QnAMaker(QnaApplicationTest.tests_endpoint)
        context = QnaApplicationTest._get_context(utterance, bot_adapter)

        response = aiounittest.futurized(Mock(return_value=Response))
        response.status_code = 200
        response.headers = {}
        response.reason = ''

        with patch('aiohttp.ClientSession.post', return_value=response):
            with patch('botbuilder.ai.qna.QnAMaker._query_qna_service', return_value=aiounittest.futurized(response_json)):
                result = await qna.get_answers(context, options)

                return result

    @classmethod
    def _get_json_for_file(cls, response_file: str) -> object:
        curr_dir = path.dirname(path.abspath(__file__))
        response_path = path.join(curr_dir, "test_data", response_file)

        with open(response_path, "r", encoding="utf-8-sig") as f:
            response_str = f.read()
        response_json = json.loads(response_str)

        return response_json

    @staticmethod
    def _get_context(utterance: str, bot_adapter: BotAdapter) -> TurnContext:
        test_adapter = bot_adapter or TestAdapter()
        activity = Activity(
            type = ActivityTypes.message,
            text = utterance,
            conversation = ConversationAccount(),
            recipient = ChannelAccount(),
            from_property = ChannelAccount(),
        )

        return TurnContext(test_adapter, activity)

