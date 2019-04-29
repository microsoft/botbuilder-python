# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import json
import aiounittest, unittest, requests
from msrest import Deserializer
from os import path
from requests.models import Response
from typing import List, Tuple
from uuid import uuid4
from unittest.mock import Mock, patch, MagicMock
from asyncio import Future



from botbuilder.ai.qna import Metadata, QnAMakerEndpoint, QnAMaker, QnAMakerOptions, QnATelemetryConstants, QueryResult
from botbuilder.core import BotAdapter, BotTelemetryClient, NullTelemetryClient, TurnContext
from botbuilder.core.adapters import TestAdapter
from botbuilder.schema import Activity, ActivityTypes, ChannelAccount, ResourceResponse, ConversationAccount


class QnaApplicationTest(aiounittest.AsyncTestCase):
    _knowledge_base_id: str = 'a090f9f3-2f8e-41d1-a581-4f7a49269a0c'
    _endpoint_key: str = '4a439d5b-163b-47c3-b1d1-168cc0db5608'
    _host: str = 'https://ashleyNlpBot1-qnahost.azurewebsites.net/qnamaker'

    tests_endpoint = QnAMakerEndpoint(_knowledge_base_id, _endpoint_key, _host)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self._mocked_results: QueryResult(

        # )

    def test_qnamaker_construction(self):
        # Arrange
        endpoint = self.tests_endpoint

        # Act
        qna = QnAMaker(endpoint)
        endpoint = qna._endpoint

        # Assert
        self.assertEqual('a090f9f3-2f8e-41d1-a581-4f7a49269a0c', endpoint.knowledge_base_id)
        self.assertEqual('4a439d5b-163b-47c3-b1d1-168cc0db5608', endpoint.endpoint_key)
        self.assertEqual('https://ashleyNlpBot1-qnahost.azurewebsites.net/qnamaker', endpoint.host)


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

        #Assert
        self.assertIsNotNone(result)
        self.assertEqual(1, len(result['answers']))
        self.assertTrue(question in first_answer['questions'])
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
        self.assertEqual(has_at_least_1_ans,  len(result['answers']) >= 1 and len(result['answers']) <= options.top)
        self.assertTrue(question in first_answer['questions'])
        self.assertTrue(first_answer['answer'])
        self.assertEqual('is a movie', first_answer['answer'])
        self.assertTrue(first_answer['score'] >= options.score_threshold)
        self.assertEqual('movie', first_metadata['name'])
        self.assertEqual('disney', first_metadata['value'])
    
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
        response = Mock(spec=Response)
        response.status_code = 200
        response.headers = {}
        response.reason = ''

        with patch('requests.post', return_value=response):
            with patch('botbuilder.ai.qna.QnAMaker._format_qna_result', return_value=response_json):
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
        test_adapter = TestAdapter()
        activity = Activity(
            type = ActivityTypes.message,
            text = utterance,
            conversation = ConversationAccount(),
            recipient = ChannelAccount(),
            from_property = ChannelAccount(),
        )

        return TurnContext(test_adapter, activity)











