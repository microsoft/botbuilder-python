# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

# pylint: disable=protected-access

import json
from os import path
from typing import List, Dict
import unittest
from unittest.mock import patch
from aiohttp import ClientSession

import aiounittest
from botbuilder.ai.qna import QnAMakerEndpoint, QnAMaker, QnAMakerOptions
from botbuilder.ai.qna.models import (
    FeedbackRecord,
    Metadata,
    QueryResult,
    QnARequestContext,
)
from botbuilder.ai.qna.utils import QnATelemetryConstants
from botbuilder.core import BotAdapter, BotTelemetryClient, TurnContext
from botbuilder.core.adapters import TestAdapter
from botbuilder.schema import (
    Activity,
    ActivityTypes,
    ChannelAccount,
    ConversationAccount,
)


class TestContext(TurnContext):
    def __init__(self, request):
        super().__init__(TestAdapter(), request)
        self.sent: List[Activity] = list()

        self.on_send_activities(self.capture_sent_activities)

    async def capture_sent_activities(
        self, context: TurnContext, activities, next
    ):  # pylint: disable=unused-argument
        self.sent += activities
        context.responded = True


class QnaApplicationTest(aiounittest.AsyncTestCase):
    # Note this is NOT a real QnA Maker application ID nor a real QnA Maker subscription-key
    # theses are GUIDs edited to look right to the parsing and validation code.

    _knowledge_base_id: str = "f028d9k3-7g9z-11d3-d300-2b8x98227q8w"
    _endpoint_key: str = "1k997n7w-207z-36p3-j2u1-09tas20ci6011"
    _host: str = "https://dummyqnahost.azurewebsites.net/qnamaker"

    tests_endpoint = QnAMakerEndpoint(_knowledge_base_id, _endpoint_key, _host)

    def test_qnamaker_construction(self):
        # Arrange
        endpoint = self.tests_endpoint

        # Act
        qna = QnAMaker(endpoint)
        endpoint = qna._endpoint

        # Assert
        self.assertEqual(
            "f028d9k3-7g9z-11d3-d300-2b8x98227q8w", endpoint.knowledge_base_id
        )
        self.assertEqual("1k997n7w-207z-36p3-j2u1-09tas20ci6011", endpoint.endpoint_key)
        self.assertEqual(
            "https://dummyqnahost.azurewebsites.net/qnamaker", endpoint.host
        )

    def test_endpoint_with_empty_kbid(self):
        empty_kbid = ""

        with self.assertRaises(TypeError):
            QnAMakerEndpoint(empty_kbid, self._endpoint_key, self._host)

    def test_endpoint_with_empty_endpoint_key(self):
        empty_endpoint_key = ""

        with self.assertRaises(TypeError):
            QnAMakerEndpoint(self._knowledge_base_id, empty_endpoint_key, self._host)

    def test_endpoint_with_emptyhost(self):
        with self.assertRaises(TypeError):
            QnAMakerEndpoint(self._knowledge_base_id, self._endpoint_key, "")

    def test_qnamaker_with_none_endpoint(self):
        with self.assertRaises(TypeError):
            QnAMaker(None)

    def test_set_default_options_with_no_options_arg(self):
        qna_without_options = QnAMaker(self.tests_endpoint)
        options = qna_without_options._generate_answer_helper.options

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
            strict_filters=[Metadata("movie", "disney")],
        )

        qna_with_options = QnAMaker(self.tests_endpoint, options)
        actual_options = qna_with_options._generate_answer_helper.options

        expected_threshold = 0.8
        expected_timeout = 9000
        expected_top = 5
        expected_strict_filters = [Metadata("movie", "disney")]

        self.assertEqual(expected_threshold, actual_options.score_threshold)
        self.assertEqual(expected_timeout, actual_options.timeout)
        self.assertEqual(expected_top, actual_options.top)
        self.assertEqual(
            expected_strict_filters[0].name, actual_options.strict_filters[0].name
        )
        self.assertEqual(
            expected_strict_filters[0].value, actual_options.strict_filters[0].value
        )

    async def test_returns_answer(self):
        # Arrange
        question: str = "how do I clean the stove?"
        response_path: str = "ReturnsAnswer.json"

        # Act
        result = await QnaApplicationTest._get_service_result(question, response_path)

        first_answer = result[0]

        # Assert
        self.assertIsNotNone(result)
        self.assertEqual(1, len(result))
        self.assertEqual(
            "BaseCamp: You can use a damp rag to clean around the Power Pack",
            first_answer.answer,
        )

    async def test_active_learning_enabled_status(self):
        # Arrange
        question: str = "how do I clean the stove?"
        response_path: str = "ReturnsAnswer.json"

        # Act
        result = await QnaApplicationTest._get_service_result_raw(
            question, response_path
        )

        # Assert
        self.assertIsNotNone(result)
        self.assertEqual(1, len(result.answers))
        self.assertFalse(result.active_learning_enabled)

    async def test_returns_answer_using_options(self):
        # Arrange
        question: str = "up"
        response_path: str = "AnswerWithOptions.json"
        options = QnAMakerOptions(
            score_threshold=0.8, top=5, strict_filters=[Metadata("movie", "disney")]
        )

        # Act
        result = await QnaApplicationTest._get_service_result(
            question, response_path, options=options
        )

        first_answer = result[0]
        has_at_least_1_ans = True
        first_metadata = first_answer.metadata[0]

        # Assert
        self.assertIsNotNone(result)
        self.assertEqual(has_at_least_1_ans, len(result) >= 1)
        self.assertTrue(first_answer.answer[0])
        self.assertEqual("is a movie", first_answer.answer)
        self.assertTrue(first_answer.score >= options.score_threshold)
        self.assertEqual("movie", first_metadata.name)
        self.assertEqual("disney", first_metadata.value)

    async def test_trace_test(self):
        activity = Activity(
            type=ActivityTypes.message,
            text="how do I clean the stove?",
            conversation=ConversationAccount(),
            recipient=ChannelAccount(),
            from_property=ChannelAccount(),
        )

        response_json = QnaApplicationTest._get_json_for_file("ReturnsAnswer.json")
        qna = QnAMaker(QnaApplicationTest.tests_endpoint)

        context = TestContext(activity)

        with patch(
            "aiohttp.ClientSession.post",
            return_value=aiounittest.futurized(response_json),
        ):
            result = await qna.get_answers(context)

            qna_trace_activities = list(
                filter(
                    lambda act: act.type == "trace" and act.name == "QnAMaker",
                    context.sent,
                )
            )
            trace_activity = qna_trace_activities[0]

            self.assertEqual("trace", trace_activity.type)
            self.assertEqual("QnAMaker", trace_activity.name)
            self.assertEqual("QnAMaker Trace", trace_activity.label)
            self.assertEqual(
                "https://www.qnamaker.ai/schemas/trace", trace_activity.value_type
            )
            self.assertEqual(True, hasattr(trace_activity, "value"))
            self.assertEqual(True, hasattr(trace_activity.value, "message"))
            self.assertEqual(True, hasattr(trace_activity.value, "query_results"))
            self.assertEqual(True, hasattr(trace_activity.value, "score_threshold"))
            self.assertEqual(True, hasattr(trace_activity.value, "top"))
            self.assertEqual(True, hasattr(trace_activity.value, "strict_filters"))
            self.assertEqual(
                self._knowledge_base_id, trace_activity.value.knowledge_base_id
            )

            return result

    async def test_returns_answer_with_timeout(self):
        question: str = "how do I clean the stove?"
        options = QnAMakerOptions(timeout=999999)
        qna = QnAMaker(QnaApplicationTest.tests_endpoint, options)
        context = QnaApplicationTest._get_context(question, TestAdapter())
        response_json = QnaApplicationTest._get_json_for_file("ReturnsAnswer.json")

        with patch(
            "aiohttp.ClientSession.post",
            return_value=aiounittest.futurized(response_json),
        ):
            result = await qna.get_answers(context, options)

            self.assertIsNotNone(result)
            self.assertEqual(
                options.timeout, qna._generate_answer_helper.options.timeout
            )

    async def test_telemetry_returns_answer(self):
        # Arrange
        question: str = "how do I clean the stove?"
        response_json = QnaApplicationTest._get_json_for_file("ReturnsAnswer.json")
        telemetry_client = unittest.mock.create_autospec(BotTelemetryClient)
        log_personal_information = True
        context = QnaApplicationTest._get_context(question, TestAdapter())
        qna = QnAMaker(
            QnaApplicationTest.tests_endpoint,
            telemetry_client=telemetry_client,
            log_personal_information=log_personal_information,
        )

        # Act
        with patch(
            "aiohttp.ClientSession.post",
            return_value=aiounittest.futurized(response_json),
        ):
            results = await qna.get_answers(context)

            telemetry_args = telemetry_client.track_event.call_args_list[0][1]
            telemetry_properties = telemetry_args["properties"]
            telemetry_metrics = telemetry_args["measurements"]
            number_of_args = len(telemetry_args)
            first_answer = telemetry_args["properties"][
                QnATelemetryConstants.answer_property
            ]
            expected_answer = (
                "BaseCamp: You can use a damp rag to clean around the Power Pack"
            )

            # Assert - Check Telemetry logged.
            self.assertEqual(1, telemetry_client.track_event.call_count)
            self.assertEqual(3, number_of_args)
            self.assertEqual("QnaMessage", telemetry_args["name"])
            self.assertTrue("answer" in telemetry_properties)
            self.assertTrue("knowledgeBaseId" in telemetry_properties)
            self.assertTrue("matchedQuestion" in telemetry_properties)
            self.assertTrue("question" in telemetry_properties)
            self.assertTrue("questionId" in telemetry_properties)
            self.assertTrue("articleFound" in telemetry_properties)
            self.assertEqual(expected_answer, first_answer)
            self.assertTrue("score" in telemetry_metrics)
            self.assertEqual(1, telemetry_metrics["score"])

            # Assert - Validate we didn't break QnA functionality.
            self.assertIsNotNone(results)
            self.assertEqual(1, len(results))
            self.assertEqual(expected_answer, results[0].answer)
            self.assertEqual("Editorial", results[0].source)

    async def test_telemetry_returns_answer_when_no_answer_found_in_kb(self):
        # Arrange
        question: str = "gibberish question"
        response_json = QnaApplicationTest._get_json_for_file("NoAnswerFoundInKb.json")
        telemetry_client = unittest.mock.create_autospec(BotTelemetryClient)
        qna = QnAMaker(
            QnaApplicationTest.tests_endpoint,
            telemetry_client=telemetry_client,
            log_personal_information=True,
        )
        context = QnaApplicationTest._get_context(question, TestAdapter())

        # Act
        with patch(
            "aiohttp.ClientSession.post",
            return_value=aiounittest.futurized(response_json),
        ):
            results = await qna.get_answers(context)

            telemetry_args = telemetry_client.track_event.call_args_list[0][1]
            telemetry_properties = telemetry_args["properties"]
            number_of_args = len(telemetry_args)
            first_answer = telemetry_args["properties"][
                QnATelemetryConstants.answer_property
            ]
            expected_answer = "No Qna Answer matched"
            expected_matched_question = "No Qna Question matched"

            # Assert - Check Telemetry logged.
            self.assertEqual(1, telemetry_client.track_event.call_count)
            self.assertEqual(3, number_of_args)
            self.assertEqual("QnaMessage", telemetry_args["name"])
            self.assertTrue("answer" in telemetry_properties)
            self.assertTrue("knowledgeBaseId" in telemetry_properties)
            self.assertTrue("matchedQuestion" in telemetry_properties)
            self.assertEqual(
                expected_matched_question,
                telemetry_properties[QnATelemetryConstants.matched_question_property],
            )
            self.assertTrue("question" in telemetry_properties)
            self.assertTrue("questionId" in telemetry_properties)
            self.assertTrue("articleFound" in telemetry_properties)
            self.assertEqual(expected_answer, first_answer)

            # Assert - Validate we didn't break QnA functionality.
            self.assertIsNotNone(results)
            self.assertEqual(0, len(results))

    async def test_telemetry_pii(self):
        # Arrange
        question: str = "how do I clean the stove?"
        response_json = QnaApplicationTest._get_json_for_file("ReturnsAnswer.json")
        telemetry_client = unittest.mock.create_autospec(BotTelemetryClient)
        log_personal_information = False
        context = QnaApplicationTest._get_context(question, TestAdapter())
        qna = QnAMaker(
            QnaApplicationTest.tests_endpoint,
            telemetry_client=telemetry_client,
            log_personal_information=log_personal_information,
        )

        # Act
        with patch(
            "aiohttp.ClientSession.post",
            return_value=aiounittest.futurized(response_json),
        ):
            results = await qna.get_answers(context)

            telemetry_args = telemetry_client.track_event.call_args_list[0][1]
            telemetry_properties = telemetry_args["properties"]
            telemetry_metrics = telemetry_args["measurements"]
            number_of_args = len(telemetry_args)
            first_answer = telemetry_args["properties"][
                QnATelemetryConstants.answer_property
            ]
            expected_answer = (
                "BaseCamp: You can use a damp rag to clean around the Power Pack"
            )

            # Assert - Validate PII properties not logged.
            self.assertEqual(1, telemetry_client.track_event.call_count)
            self.assertEqual(3, number_of_args)
            self.assertEqual("QnaMessage", telemetry_args["name"])
            self.assertTrue("answer" in telemetry_properties)
            self.assertTrue("knowledgeBaseId" in telemetry_properties)
            self.assertTrue("matchedQuestion" in telemetry_properties)
            self.assertTrue("question" not in telemetry_properties)
            self.assertTrue("questionId" in telemetry_properties)
            self.assertTrue("articleFound" in telemetry_properties)
            self.assertEqual(expected_answer, first_answer)
            self.assertTrue("score" in telemetry_metrics)
            self.assertEqual(1, telemetry_metrics["score"])

            # Assert - Validate we didn't break QnA functionality.
            self.assertIsNotNone(results)
            self.assertEqual(1, len(results))
            self.assertEqual(expected_answer, results[0].answer)
            self.assertEqual("Editorial", results[0].source)

    async def test_telemetry_override(self):
        # Arrange
        question: str = "how do I clean the stove?"
        response_json = QnaApplicationTest._get_json_for_file("ReturnsAnswer.json")
        context = QnaApplicationTest._get_context(question, TestAdapter())
        options = QnAMakerOptions(top=1)
        telemetry_client = unittest.mock.create_autospec(BotTelemetryClient)
        log_personal_information = False

        # Act - Override the QnAMaker object to log custom stuff and honor params passed in.
        telemetry_properties: Dict[str, str] = {"id": "MyId"}
        qna = QnaApplicationTest.OverrideTelemetry(
            QnaApplicationTest.tests_endpoint,
            options,
            None,
            telemetry_client,
            log_personal_information,
        )
        with patch(
            "aiohttp.ClientSession.post",
            return_value=aiounittest.futurized(response_json),
        ):
            results = await qna.get_answers(context, options, telemetry_properties)

            telemetry_args = telemetry_client.track_event.call_args_list
            first_call_args = telemetry_args[0][0]
            first_call_properties = first_call_args[1]
            second_call_args = telemetry_args[1][0]
            second_call_properties = second_call_args[1]
            expected_answer = (
                "BaseCamp: You can use a damp rag to clean around the Power Pack"
            )

            # Assert
            self.assertEqual(2, telemetry_client.track_event.call_count)
            self.assertEqual(2, len(first_call_args))
            self.assertEqual("QnaMessage", first_call_args[0])
            self.assertEqual(2, len(first_call_properties))
            self.assertTrue("my_important_property" in first_call_properties)
            self.assertEqual(
                "my_important_value", first_call_properties["my_important_property"]
            )
            self.assertTrue("id" in first_call_properties)
            self.assertEqual("MyId", first_call_properties["id"])

            self.assertEqual("my_second_event", second_call_args[0])
            self.assertTrue("my_important_property2" in second_call_properties)
            self.assertEqual(
                "my_important_value2", second_call_properties["my_important_property2"]
            )

            # Validate we didn't break QnA functionality.
            self.assertIsNotNone(results)
            self.assertEqual(1, len(results))
            self.assertEqual(expected_answer, results[0].answer)
            self.assertEqual("Editorial", results[0].source)

    async def test_telemetry_additional_props_metrics(self):
        # Arrange
        question: str = "how do I clean the stove?"
        response_json = QnaApplicationTest._get_json_for_file("ReturnsAnswer.json")
        context = QnaApplicationTest._get_context(question, TestAdapter())
        options = QnAMakerOptions(top=1)
        telemetry_client = unittest.mock.create_autospec(BotTelemetryClient)
        log_personal_information = False

        # Act
        with patch(
            "aiohttp.ClientSession.post",
            return_value=aiounittest.futurized(response_json),
        ):
            qna = QnAMaker(
                QnaApplicationTest.tests_endpoint,
                options,
                None,
                telemetry_client,
                log_personal_information,
            )
            telemetry_properties: Dict[str, str] = {
                "my_important_property": "my_important_value"
            }
            telemetry_metrics: Dict[str, float] = {"my_important_metric": 3.14159}

            results = await qna.get_answers(
                context, None, telemetry_properties, telemetry_metrics
            )

            # Assert - Added properties were added.
            telemetry_args = telemetry_client.track_event.call_args_list[0][1]
            telemetry_properties = telemetry_args["properties"]
            expected_answer = (
                "BaseCamp: You can use a damp rag to clean around the Power Pack"
            )

            self.assertEqual(1, telemetry_client.track_event.call_count)
            self.assertEqual(3, len(telemetry_args))
            self.assertEqual("QnaMessage", telemetry_args["name"])
            self.assertTrue("knowledgeBaseId" in telemetry_properties)
            self.assertTrue("question" not in telemetry_properties)
            self.assertTrue("matchedQuestion" in telemetry_properties)
            self.assertTrue("questionId" in telemetry_properties)
            self.assertTrue("answer" in telemetry_properties)
            self.assertTrue(expected_answer, telemetry_properties["answer"])
            self.assertTrue("my_important_property" in telemetry_properties)
            self.assertEqual(
                "my_important_value", telemetry_properties["my_important_property"]
            )

            tracked_metrics = telemetry_args["measurements"]

            self.assertEqual(2, len(tracked_metrics))
            self.assertTrue("score" in tracked_metrics)
            self.assertTrue("my_important_metric" in tracked_metrics)
            self.assertEqual(3.14159, tracked_metrics["my_important_metric"])

            # Assert - Validate we didn't break QnA functionality.
            self.assertIsNotNone(results)
            self.assertEqual(1, len(results))
            self.assertEqual(expected_answer, results[0].answer)
            self.assertEqual("Editorial", results[0].source)

    async def test_telemetry_additional_props_override(self):
        question: str = "how do I clean the stove?"
        response_json = QnaApplicationTest._get_json_for_file("ReturnsAnswer.json")
        context = QnaApplicationTest._get_context(question, TestAdapter())
        options = QnAMakerOptions(top=1)
        telemetry_client = unittest.mock.create_autospec(BotTelemetryClient)
        log_personal_information = False

        # Act - Pass in properties during QnA invocation that override default properties
        # NOTE: We are invoking this with PII turned OFF, and passing a PII property (originalQuestion).
        qna = QnAMaker(
            QnaApplicationTest.tests_endpoint,
            options,
            None,
            telemetry_client,
            log_personal_information,
        )
        telemetry_properties = {
            "knowledge_base_id": "my_important_value",
            "original_question": "my_important_value2",
        }
        telemetry_metrics = {"score": 3.14159}

        with patch(
            "aiohttp.ClientSession.post",
            return_value=aiounittest.futurized(response_json),
        ):
            results = await qna.get_answers(
                context, None, telemetry_properties, telemetry_metrics
            )

            # Assert - Added properties were added.
            tracked_args = telemetry_client.track_event.call_args_list[0][1]
            tracked_properties = tracked_args["properties"]
            expected_answer = (
                "BaseCamp: You can use a damp rag to clean around the Power Pack"
            )
            tracked_metrics = tracked_args["measurements"]

            self.assertEqual(1, telemetry_client.track_event.call_count)
            self.assertEqual(3, len(tracked_args))
            self.assertEqual("QnaMessage", tracked_args["name"])
            self.assertTrue("knowledge_base_id" in tracked_properties)
            self.assertEqual(
                "my_important_value", tracked_properties["knowledge_base_id"]
            )
            self.assertTrue("original_question" in tracked_properties)
            self.assertTrue("matchedQuestion" in tracked_properties)
            self.assertEqual(
                "my_important_value2", tracked_properties["original_question"]
            )
            self.assertTrue("question" not in tracked_properties)
            self.assertTrue("questionId" in tracked_properties)
            self.assertTrue("answer" in tracked_properties)
            self.assertEqual(expected_answer, tracked_properties["answer"])
            self.assertTrue("my_important_property" not in tracked_properties)
            self.assertEqual(1, len(tracked_metrics))
            self.assertTrue("score" in tracked_metrics)
            self.assertEqual(3.14159, tracked_metrics["score"])

            # Assert - Validate we didn't break QnA functionality.
            self.assertIsNotNone(results)
            self.assertEqual(1, len(results))
            self.assertEqual(expected_answer, results[0].answer)
            self.assertEqual("Editorial", results[0].source)

    async def test_telemetry_fill_props_override(self):
        # Arrange
        question: str = "how do I clean the stove?"
        response_json = QnaApplicationTest._get_json_for_file("ReturnsAnswer.json")
        context: TurnContext = QnaApplicationTest._get_context(question, TestAdapter())
        options = QnAMakerOptions(top=1)
        telemetry_client = unittest.mock.create_autospec(BotTelemetryClient)
        log_personal_information = False

        # Act - Pass in properties during QnA invocation that override default properties
        #       In addition Override with derivation.  This presents an interesting question of order of setting
        #       properties.
        #       If I want to override "originalQuestion" property:
        #           - Set in "Stock" schema
        #           - Set in derived QnAMaker class
        #           - Set in GetAnswersAsync
        #       Logically, the GetAnswersAync should win.  But ultimately OnQnaResultsAsync decides since it is the last
        #       code to touch the properties before logging (since it actually logs the event).
        qna = QnaApplicationTest.OverrideFillTelemetry(
            QnaApplicationTest.tests_endpoint,
            options,
            None,
            telemetry_client,
            log_personal_information,
        )
        telemetry_properties: Dict[str, str] = {
            "knowledgeBaseId": "my_important_value",
            "matchedQuestion": "my_important_value2",
        }
        telemetry_metrics: Dict[str, float] = {"score": 3.14159}

        with patch(
            "aiohttp.ClientSession.post",
            return_value=aiounittest.futurized(response_json),
        ):
            results = await qna.get_answers(
                context, None, telemetry_properties, telemetry_metrics
            )

            # Assert - Added properties were added.
            first_call_args = telemetry_client.track_event.call_args_list[0][0]
            first_properties = first_call_args[1]
            expected_answer = (
                "BaseCamp: You can use a damp rag to clean around the Power Pack"
            )
            first_metrics = first_call_args[2]

            self.assertEqual(2, telemetry_client.track_event.call_count)
            self.assertEqual(3, len(first_call_args))
            self.assertEqual("QnaMessage", first_call_args[0])
            self.assertEqual(6, len(first_properties))
            self.assertTrue("knowledgeBaseId" in first_properties)
            self.assertEqual("my_important_value", first_properties["knowledgeBaseId"])
            self.assertTrue("matchedQuestion" in first_properties)
            self.assertEqual("my_important_value2", first_properties["matchedQuestion"])
            self.assertTrue("questionId" in first_properties)
            self.assertTrue("answer" in first_properties)
            self.assertEqual(expected_answer, first_properties["answer"])
            self.assertTrue("articleFound" in first_properties)
            self.assertTrue("my_important_property" in first_properties)
            self.assertEqual(
                "my_important_value", first_properties["my_important_property"]
            )

            self.assertEqual(1, len(first_metrics))
            self.assertTrue("score" in first_metrics)
            self.assertEqual(3.14159, first_metrics["score"])

            # Assert - Validate we didn't break QnA functionality.
            self.assertIsNotNone(results)
            self.assertEqual(1, len(results))
            self.assertEqual(expected_answer, results[0].answer)
            self.assertEqual("Editorial", results[0].source)

    async def test_call_train(self):
        feedback_records = []

        feedback1 = FeedbackRecord(
            qna_id=1, user_id="test", user_question="How are you?"
        )

        feedback2 = FeedbackRecord(qna_id=2, user_id="test", user_question="What up??")

        feedback_records.extend([feedback1, feedback2])

        with patch.object(
            QnAMaker, "call_train", return_value=None
        ) as mocked_call_train:
            qna = QnAMaker(QnaApplicationTest.tests_endpoint)
            qna.call_train(feedback_records)

            mocked_call_train.assert_called_once_with(feedback_records)

    async def test_should_filter_low_score_variation(self):
        options = QnAMakerOptions(top=5)
        qna = QnAMaker(QnaApplicationTest.tests_endpoint, options)
        question: str = "Q11"
        context = QnaApplicationTest._get_context(question, TestAdapter())
        response_json = QnaApplicationTest._get_json_for_file("TopNAnswer.json")

        with patch(
            "aiohttp.ClientSession.post",
            return_value=aiounittest.futurized(response_json),
        ):
            results = await qna.get_answers(context)
            self.assertEqual(4, len(results), "Should have received 4 answers.")

            filtered_results = qna.get_low_score_variation(results)
            self.assertEqual(
                3,
                len(filtered_results),
                "Should have 3 filtered answers after low score variation.",
            )

    async def test_should_answer_with_is_test_true(self):
        options = QnAMakerOptions(top=1, is_test=True)
        qna = QnAMaker(QnaApplicationTest.tests_endpoint)
        question: str = "Q11"
        context = QnaApplicationTest._get_context(question, TestAdapter())
        response_json = QnaApplicationTest._get_json_for_file(
            "QnaMaker_IsTest_true.json"
        )

        with patch(
            "aiohttp.ClientSession.post",
            return_value=aiounittest.futurized(response_json),
        ):
            results = await qna.get_answers(context, options=options)
            self.assertEqual(0, len(results), "Should have received zero answer.")

    async def test_should_answer_with_ranker_type_question_only(self):
        options = QnAMakerOptions(top=1, ranker_type="QuestionOnly")
        qna = QnAMaker(QnaApplicationTest.tests_endpoint)
        question: str = "Q11"
        context = QnaApplicationTest._get_context(question, TestAdapter())
        response_json = QnaApplicationTest._get_json_for_file(
            "QnaMaker_RankerType_QuestionOnly.json"
        )

        with patch(
            "aiohttp.ClientSession.post",
            return_value=aiounittest.futurized(response_json),
        ):
            results = await qna.get_answers(context, options=options)
            self.assertEqual(2, len(results), "Should have received two answers.")

    async def test_should_answer_with_prompts(self):
        options = QnAMakerOptions(top=2)
        qna = QnAMaker(QnaApplicationTest.tests_endpoint, options)
        question: str = "how do I clean the stove?"
        turn_context = QnaApplicationTest._get_context(question, TestAdapter())
        response_json = QnaApplicationTest._get_json_for_file("AnswerWithPrompts.json")

        with patch(
            "aiohttp.ClientSession.post",
            return_value=aiounittest.futurized(response_json),
        ):
            results = await qna.get_answers(turn_context, options)
            self.assertEqual(1, len(results), "Should have received 1 answers.")
            self.assertEqual(
                1, len(results[0].context.prompts), "Should have received 1 prompt."
            )

    async def test_should_answer_with_high_score_provided_context(self):
        qna = QnAMaker(QnaApplicationTest.tests_endpoint)
        question: str = "where can I buy?"
        context = QnARequestContext(
            previous_qna_id=5, prvious_user_query="how do I clean the stove?"
        )
        options = QnAMakerOptions(top=2, qna_id=55, context=context)
        turn_context = QnaApplicationTest._get_context(question, TestAdapter())
        response_json = QnaApplicationTest._get_json_for_file(
            "AnswerWithHighScoreProvidedContext.json"
        )

        with patch(
            "aiohttp.ClientSession.post",
            return_value=aiounittest.futurized(response_json),
        ):
            results = await qna.get_answers(turn_context, options)
            self.assertEqual(1, len(results), "Should have received 1 answers.")
            self.assertEqual(1, results[0].score, "Score should be high.")

    async def test_should_answer_with_high_score_provided_qna_id(self):
        qna = QnAMaker(QnaApplicationTest.tests_endpoint)
        question: str = "where can I buy?"

        options = QnAMakerOptions(top=2, qna_id=55)
        turn_context = QnaApplicationTest._get_context(question, TestAdapter())
        response_json = QnaApplicationTest._get_json_for_file(
            "AnswerWithHighScoreProvidedContext.json"
        )

        with patch(
            "aiohttp.ClientSession.post",
            return_value=aiounittest.futurized(response_json),
        ):
            results = await qna.get_answers(turn_context, options)
            self.assertEqual(1, len(results), "Should have received 1 answers.")
            self.assertEqual(1, results[0].score, "Score should be high.")

    async def test_should_answer_with_low_score_without_provided_context(self):
        qna = QnAMaker(QnaApplicationTest.tests_endpoint)
        question: str = "where can I buy?"
        options = QnAMakerOptions(top=2, context=None)

        turn_context = QnaApplicationTest._get_context(question, TestAdapter())
        response_json = QnaApplicationTest._get_json_for_file(
            "AnswerWithLowScoreProvidedWithoutContext.json"
        )

        with patch(
            "aiohttp.ClientSession.post",
            return_value=aiounittest.futurized(response_json),
        ):
            results = await qna.get_answers(turn_context, options)
            self.assertEqual(
                2, len(results), "Should have received more than one answers."
            )
            self.assertEqual(True, results[0].score < 1, "Score should be low.")

    @classmethod
    async def _get_service_result(
        cls,
        utterance: str,
        response_file: str,
        bot_adapter: BotAdapter = TestAdapter(),
        options: QnAMakerOptions = None,
    ) -> [dict]:
        response_json = QnaApplicationTest._get_json_for_file(response_file)

        qna = QnAMaker(QnaApplicationTest.tests_endpoint)
        context = QnaApplicationTest._get_context(utterance, bot_adapter)

        with patch(
            "aiohttp.ClientSession.post",
            return_value=aiounittest.futurized(response_json),
        ):
            result = await qna.get_answers(context, options)

            return result

    @classmethod
    async def _get_service_result_raw(
        cls,
        utterance: str,
        response_file: str,
        bot_adapter: BotAdapter = TestAdapter(),
        options: QnAMakerOptions = None,
    ) -> [dict]:
        response_json = QnaApplicationTest._get_json_for_file(response_file)

        qna = QnAMaker(QnaApplicationTest.tests_endpoint)
        context = QnaApplicationTest._get_context(utterance, bot_adapter)

        with patch(
            "aiohttp.ClientSession.post",
            return_value=aiounittest.futurized(response_json),
        ):
            result = await qna.get_answers_raw(context, options)

            return result

    @classmethod
    def _get_json_for_file(cls, response_file: str) -> object:
        curr_dir = path.dirname(path.abspath(__file__))
        response_path = path.join(curr_dir, "test_data", response_file)

        with open(response_path, "r", encoding="utf-8-sig") as file:
            response_str = file.read()
        response_json = json.loads(response_str)

        return response_json

    @staticmethod
    def _get_context(question: str, bot_adapter: BotAdapter) -> TurnContext:
        test_adapter = bot_adapter or TestAdapter()
        activity = Activity(
            type=ActivityTypes.message,
            text=question,
            conversation=ConversationAccount(),
            recipient=ChannelAccount(),
            from_property=ChannelAccount(),
        )

        return TurnContext(test_adapter, activity)

    class OverrideTelemetry(QnAMaker):
        def __init__(  # pylint: disable=useless-super-delegation
            self,
            endpoint: QnAMakerEndpoint,
            options: QnAMakerOptions,
            http_client: ClientSession,
            telemetry_client: BotTelemetryClient,
            log_personal_information: bool,
        ):
            super().__init__(
                endpoint,
                options,
                http_client,
                telemetry_client,
                log_personal_information,
            )

        async def on_qna_result(  # pylint: disable=unused-argument
            self,
            query_results: [QueryResult],
            turn_context: TurnContext,
            telemetry_properties: Dict[str, str] = None,
            telemetry_metrics: Dict[str, float] = None,
        ):
            properties = telemetry_properties or {}

            # get_answers overrides derived class
            properties["my_important_property"] = "my_important_value"

            # Log event
            self.telemetry_client.track_event(
                QnATelemetryConstants.qna_message_event, properties
            )

            # Create 2nd event.
            second_event_properties = {"my_important_property2": "my_important_value2"}
            self.telemetry_client.track_event(
                "my_second_event", second_event_properties
            )

    class OverrideFillTelemetry(QnAMaker):
        def __init__(  # pylint: disable=useless-super-delegation
            self,
            endpoint: QnAMakerEndpoint,
            options: QnAMakerOptions,
            http_client: ClientSession,
            telemetry_client: BotTelemetryClient,
            log_personal_information: bool,
        ):
            super().__init__(
                endpoint,
                options,
                http_client,
                telemetry_client,
                log_personal_information,
            )

        async def on_qna_result(
            self,
            query_results: [QueryResult],
            turn_context: TurnContext,
            telemetry_properties: Dict[str, str] = None,
            telemetry_metrics: Dict[str, float] = None,
        ):
            event_data = await self.fill_qna_event(
                query_results, turn_context, telemetry_properties, telemetry_metrics
            )

            # Add my property.
            event_data.properties.update(
                {"my_important_property": "my_important_value"}
            )

            # Log QnaMessage event.
            self.telemetry_client.track_event(
                QnATelemetryConstants.qna_message_event,
                event_data.properties,
                event_data.metrics,
            )

            # Create second event.
            second_event_properties: Dict[str, str] = {
                "my_important_property2": "my_important_value2"
            }

            self.telemetry_client.track_event("MySecondEvent", second_event_properties)
