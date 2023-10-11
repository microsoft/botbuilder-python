# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

# pylint: disable=protected-access

import json
from os import path
from typing import Dict, Tuple, Union
from unittest import mock
from unittest.mock import MagicMock, Mock

from aiounittest import AsyncTestCase
from msrest import Deserializer
from requests import Session
from requests.models import Response

from botbuilder.ai.luis import LuisApplication, LuisPredictionOptions, LuisRecognizer
from botbuilder.ai.luis.luis_util import LuisUtil
from botbuilder.core import (
    BotAdapter,
    BotTelemetryClient,
    IntentScore,
    RecognizerResult,
    TurnContext,
)
from botbuilder.core.adapters import TestAdapter
from botbuilder.schema import (
    Activity,
    ActivityTypes,
    ChannelAccount,
    ConversationAccount,
)
from null_adapter import NullAdapter
from override_fill_recognizer import OverrideFillRecognizer
from telemetry_override_recognizer import TelemetryOverrideRecognizer


class LuisRecognizerTest(AsyncTestCase):
    _luisAppId: str = "b31aeaf3-3511-495b-a07f-571fc873214b"
    _subscriptionKey: str = "048ec46dc58e495482b0c447cfdbd291"
    _endpoint: str = "https://westus.api.cognitive.microsoft.com"

    def __init__(self, *args, **kwargs):
        super(LuisRecognizerTest, self).__init__(*args, **kwargs)
        self._mocked_results: RecognizerResult = RecognizerResult(
            intents={"Test": IntentScore(score=0.2), "Greeting": IntentScore(score=0.4)}
        )
        self._empty_luis_response: Dict[str, object] = json.loads(
            '{ "query": null, "intents": [], "entities": [] }'
        )

    def test_luis_recognizer_construction(self):
        # Arrange
        endpoint = (
            "https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/"
            "b31aeaf3-3511-495b-a07f-571fc873214b?verbose=true&timezoneOffset=-360"
            "&subscription-key=048ec46dc58e495482b0c447cfdbd291&q="
        )

        # Act
        recognizer = LuisRecognizer(endpoint)

        # Assert
        app = recognizer._application
        self.assertEqual("b31aeaf3-3511-495b-a07f-571fc873214b", app.application_id)
        self.assertEqual("048ec46dc58e495482b0c447cfdbd291", app.endpoint_key)
        self.assertEqual("https://westus.api.cognitive.microsoft.com", app.endpoint)

    def test_none_endpoint(self):
        # Arrange
        my_app = LuisApplication(
            LuisRecognizerTest._luisAppId,
            LuisRecognizerTest._subscriptionKey,
            endpoint=None,
        )

        # Assert
        recognizer = LuisRecognizer(my_app, prediction_options=None)

        # Assert
        app = recognizer._application
        self.assertEqual("https://westus.api.cognitive.microsoft.com", app.endpoint)

    def test_empty_endpoint(self):
        # Arrange
        my_app = LuisApplication(
            LuisRecognizerTest._luisAppId,
            LuisRecognizerTest._subscriptionKey,
            endpoint="",
        )

        # Assert
        recognizer = LuisRecognizer(my_app, prediction_options=None)

        # Assert
        app = recognizer._application
        self.assertEqual("https://westus.api.cognitive.microsoft.com", app.endpoint)

    def test_luis_recognizer_none_luis_app_arg(self):
        with self.assertRaises(TypeError):
            LuisRecognizer(application=None)

    async def test_single_intent_simply_entity(self):
        utterance: str = "My name is Emad"
        response_path: str = "SingleIntent_SimplyEntity.json"

        _, result = await LuisRecognizerTest._get_recognizer_result(
            utterance, response_path
        )

        self.assertIsNotNone(result)
        self.assertIsNone(result.altered_text)
        self.assertEqual(utterance, result.text)
        self.assertIsNotNone(result.intents)
        self.assertEqual(1, len(result.intents))
        self.assertIsNotNone(result.intents["SpecifyName"])
        self.assert_score(result.intents["SpecifyName"].score)
        self.assertIsNotNone(result.entities)
        self.assertIsNotNone(result.entities["Name"])
        self.assertEqual("emad", result.entities["Name"][0])
        self.assertIsNotNone(result.entities["$instance"])
        self.assertIsNotNone(result.entities["$instance"]["Name"])
        self.assertEqual(11, result.entities["$instance"]["Name"][0]["startIndex"])
        self.assertEqual(15, result.entities["$instance"]["Name"][0]["endIndex"])
        self.assert_score(result.entities["$instance"]["Name"][0]["score"])

    async def test_null_utterance(self):
        utterance: str = None
        response_path: str = (
            "SingleIntent_SimplyEntity.json"  # The path is irrelevant in this case
        )

        _, result = await LuisRecognizerTest._get_recognizer_result(
            utterance, response_path
        )

        self.assertIsNotNone(result)
        self.assertIsNone(result.altered_text)
        self.assertEqual(utterance, result.text)
        self.assertIsNotNone(result.intents)
        self.assertEqual(1, len(result.intents))
        self.assertIsNotNone(result.intents[""])
        self.assertEqual(result.get_top_scoring_intent(), ("", 1.0))
        self.assertIsNotNone(result.entities)
        self.assertEqual(0, len(result.entities))

    async def test_multiple_intents_prebuilt_entity(self):
        utterance: str = "Please deliver February 2nd 2001"
        response_path: str = "MultipleIntents_PrebuiltEntity.json"

        _, result = await LuisRecognizerTest._get_recognizer_result(
            utterance, response_path
        )

        self.assertIsNotNone(result)
        self.assertEqual(utterance, result.text)
        self.assertIsNotNone(result.intents)
        self.assertTrue(len(result.intents) > 1)
        self.assertIsNotNone(result.intents["Delivery"])
        self.assertTrue(
            result.intents["Delivery"].score > 0
            and result.intents["Delivery"].score <= 1
        )
        self.assertEqual("Delivery", result.get_top_scoring_intent().intent)
        self.assertTrue(result.get_top_scoring_intent().score > 0)
        self.assertIsNotNone(result.entities)
        self.assertIsNotNone(result.entities["number"])
        self.assertEqual(2001, int(result.entities["number"][0]))
        self.assertIsNotNone(result.entities["ordinal"])
        self.assertEqual(2, int(result.entities["ordinal"][0]))
        self.assertIsNotNone(result.entities["datetime"][0])
        self.assertEqual("2001-02-02", result.entities["datetime"][0]["timex"][0])
        self.assertIsNotNone(result.entities["$instance"]["number"])
        self.assertEqual(
            28, int(result.entities["$instance"]["number"][0]["startIndex"])
        )
        self.assertEqual(32, int(result.entities["$instance"]["number"][0]["endIndex"]))
        self.assertEqual("2001", result.text[28:32])
        self.assertIsNotNone(result.entities["$instance"]["datetime"])
        self.assertEqual(15, result.entities["$instance"]["datetime"][0]["startIndex"])
        self.assertEqual(32, result.entities["$instance"]["datetime"][0]["endIndex"])
        self.assertEqual(
            "february 2nd 2001", result.entities["$instance"]["datetime"][0]["text"]
        )

    async def test_multiple_intents_prebuilt_entities_with_multi_values(self):
        utterance: str = "Please deliver February 2nd 2001 in room 201"
        response_path: str = "MultipleIntents_PrebuiltEntitiesWithMultiValues.json"

        _, result = await LuisRecognizerTest._get_recognizer_result(
            utterance, response_path
        )

        self.assertIsNotNone(result)
        self.assertIsNotNone(result.text)
        self.assertEqual(utterance, result.text)
        self.assertIsNotNone(result.intents)
        self.assertIsNotNone(result.intents["Delivery"])
        self.assertIsNotNone(result.entities)
        self.assertIsNotNone(result.entities["number"])
        self.assertEqual(2, len(result.entities["number"]))
        self.assertTrue(201 in map(int, result.entities["number"]))
        self.assertTrue(2001 in map(int, result.entities["number"]))
        self.assertIsNotNone(result.entities["datetime"][0])
        self.assertEqual("2001-02-02", result.entities["datetime"][0]["timex"][0])

    async def test_multiple_intents_list_entity_with_single_value(self):
        utterance: str = "I want to travel on united"
        response_path: str = "MultipleIntents_ListEntityWithSingleValue.json"

        _, result = await LuisRecognizerTest._get_recognizer_result(
            utterance, response_path
        )

        self.assertIsNotNone(result)
        self.assertIsNotNone(result.text)
        self.assertEqual(utterance, result.text)
        self.assertIsNotNone(result.intents)
        self.assertIsNotNone(result.intents["Travel"])
        self.assertIsNotNone(result.entities)
        self.assertIsNotNone(result.entities["Airline"])
        self.assertEqual("United", result.entities["Airline"][0][0])
        self.assertIsNotNone(result.entities["$instance"])
        self.assertIsNotNone(result.entities["$instance"]["Airline"])
        self.assertEqual(20, result.entities["$instance"]["Airline"][0]["startIndex"])
        self.assertEqual(26, result.entities["$instance"]["Airline"][0]["endIndex"])
        self.assertEqual("united", result.entities["$instance"]["Airline"][0]["text"])

    async def test_multiple_intents_list_entity_with_multi_values(self):
        utterance: str = "I want to travel on DL"
        response_path: str = "MultipleIntents_ListEntityWithMultiValues.json"

        _, result = await LuisRecognizerTest._get_recognizer_result(
            utterance, response_path
        )

        self.assertIsNotNone(result)
        self.assertIsNotNone(result.text)
        self.assertEqual(utterance, result.text)
        self.assertIsNotNone(result.intents)
        self.assertIsNotNone(result.intents["Travel"])
        self.assertIsNotNone(result.entities)
        self.assertIsNotNone(result.entities["Airline"])
        self.assertEqual(2, len(result.entities["Airline"][0]))
        self.assertTrue("Delta" in result.entities["Airline"][0])
        self.assertTrue("Virgin" in result.entities["Airline"][0])
        self.assertIsNotNone(result.entities["$instance"])
        self.assertIsNotNone(result.entities["$instance"]["Airline"])
        self.assertEqual(20, result.entities["$instance"]["Airline"][0]["startIndex"])
        self.assertEqual(22, result.entities["$instance"]["Airline"][0]["endIndex"])
        self.assertEqual("dl", result.entities["$instance"]["Airline"][0]["text"])

    async def test_multiple_intents_composite_entity_model(self):
        utterance: str = "Please deliver it to 98033 WA"
        response_path: str = "MultipleIntents_CompositeEntityModel.json"

        _, result = await LuisRecognizerTest._get_recognizer_result(
            utterance, response_path
        )

        self.assertIsNotNone(result)
        self.assertIsNotNone(result.text)
        self.assertEqual(utterance, result.text)
        self.assertIsNotNone(result.intents)
        self.assertIsNotNone(result.intents["Delivery"])
        self.assertIsNotNone(result.entities)
        self.assertIsNone(result.entities.get("number"))
        self.assertIsNone(result.entities.get("State"))
        self.assertIsNotNone(result.entities["Address"])
        self.assertEqual(98033, result.entities["Address"][0]["number"][0])
        self.assertEqual("wa", result.entities["Address"][0]["State"][0])
        self.assertIsNotNone(result.entities["$instance"])
        self.assertIsNone(result.entities["$instance"].get("number"))
        self.assertIsNone(result.entities["$instance"].get("State"))
        self.assertIsNotNone(result.entities["$instance"]["Address"])
        self.assertEqual(21, result.entities["$instance"]["Address"][0]["startIndex"])
        self.assertEqual(29, result.entities["$instance"]["Address"][0]["endIndex"])
        self.assert_score(result.entities["$instance"]["Address"][0]["score"])
        self.assertIsNotNone(result.entities["Address"][0]["$instance"])
        self.assertIsNotNone(result.entities["Address"][0]["$instance"]["number"])
        self.assertEqual(
            21, result.entities["Address"][0]["$instance"]["number"][0]["startIndex"]
        )
        self.assertEqual(
            26, result.entities["Address"][0]["$instance"]["number"][0]["endIndex"]
        )
        self.assertEqual(
            "98033", result.entities["Address"][0]["$instance"]["number"][0]["text"]
        )
        self.assertIsNotNone(result.entities["Address"][0]["$instance"]["State"])
        self.assertEqual(
            27, result.entities["Address"][0]["$instance"]["State"][0]["startIndex"]
        )
        self.assertEqual(
            29, result.entities["Address"][0]["$instance"]["State"][0]["endIndex"]
        )
        self.assertEqual(
            "wa", result.entities["Address"][0]["$instance"]["State"][0]["text"]
        )
        self.assertEqual("WA", result.text[27:29])
        self.assert_score(
            result.entities["Address"][0]["$instance"]["State"][0]["score"]
        )

    async def test_multiple_date_time_entities(self):
        utterance: str = "Book a table on Friday or tomorrow at 5 or tomorrow at 4"
        response_path: str = "MultipleDateTimeEntities.json"

        _, result = await LuisRecognizerTest._get_recognizer_result(
            utterance, response_path
        )

        self.assertIsNotNone(result.entities["datetime"])
        self.assertEqual(3, len(result.entities["datetime"]))
        self.assertEqual(1, len(result.entities["datetime"][0]["timex"]))
        self.assertEqual("XXXX-WXX-5", result.entities["datetime"][0]["timex"][0])
        self.assertEqual(1, len(result.entities["datetime"][0]["timex"]))
        self.assertEqual(2, len(result.entities["datetime"][1]["timex"]))
        self.assertEqual(2, len(result.entities["datetime"][2]["timex"]))
        self.assertTrue(result.entities["datetime"][1]["timex"][0].endswith("T05"))
        self.assertTrue(result.entities["datetime"][1]["timex"][1].endswith("T17"))
        self.assertTrue(result.entities["datetime"][2]["timex"][0].endswith("T04"))
        self.assertTrue(result.entities["datetime"][2]["timex"][1].endswith("T16"))
        self.assertEqual(3, len(result.entities["$instance"]["datetime"]))

    async def test_v1_datetime_resolution(self):
        utterance: str = "at 4"
        response_path: str = "V1DatetimeResolution.json"

        _, result = await LuisRecognizerTest._get_recognizer_result(
            utterance, response_path
        )

        self.assertIsNotNone(result.entities["datetime_time"])
        self.assertEqual(1, len(result.entities["datetime_time"]))
        self.assertEqual("ampm", result.entities["datetime_time"][0]["comment"])
        self.assertEqual("T04", result.entities["datetime_time"][0]["time"])
        self.assertEqual(1, len(result.entities["$instance"]["datetime_time"]))

    async def test_trace_activity(self):
        # Arrange
        utterance: str = "My name is Emad"
        response_path: str = "TraceActivity.json"

        # add async support to magic mock.
        async def async_magic():
            pass

        MagicMock.__await__ = lambda x: async_magic().__await__()

        # Act
        with mock.patch.object(TurnContext, "send_activity") as mock_send_activity:
            await LuisRecognizerTest._get_recognizer_result(utterance, response_path)
            trace_activity: Activity = mock_send_activity.call_args[0][0]

        # Assert
        self.assertIsNotNone(trace_activity)
        self.assertEqual(LuisRecognizer.luis_trace_type, trace_activity.value_type)
        self.assertEqual(LuisRecognizer.luis_trace_label, trace_activity.label)

        luis_trace_info = trace_activity.value
        self.assertIsNotNone(luis_trace_info)
        self.assertIsNotNone(luis_trace_info["recognizerResult"])
        self.assertIsNotNone(luis_trace_info["luisResult"])
        self.assertIsNotNone(luis_trace_info["luisOptions"])
        self.assertIsNotNone(luis_trace_info["luisModel"])

        recognizer_result: RecognizerResult = luis_trace_info["recognizerResult"]
        self.assertEqual(utterance, recognizer_result["text"])
        self.assertIsNotNone(recognizer_result["intents"]["SpecifyName"])
        self.assertEqual(utterance, luis_trace_info["luisResult"]["query"])
        self.assertEqual(
            LuisRecognizerTest._luisAppId, luis_trace_info["luisModel"]["ModelID"]
        )
        self.assertIsNone(luis_trace_info["luisOptions"]["Staging"])

    def test_top_intent_returns_top_intent(self):
        greeting_intent: str = LuisRecognizer.top_intent(self._mocked_results)
        self.assertEqual(greeting_intent, "Greeting")

    def test_top_intent_returns_default_intent_if_min_score_is_higher(self):
        default_intent: str = LuisRecognizer.top_intent(
            self._mocked_results, min_score=0.5
        )
        self.assertEqual(default_intent, "None")

    def test_top_intent_returns_default_intent_if_provided(self):
        default_intent: str = LuisRecognizer.top_intent(
            self._mocked_results, "Test2", 0.5
        )
        self.assertEqual(default_intent, "Test2")

    def test_top_intent_throws_type_error_if_results_is_none(self):
        none_results: RecognizerResult = None
        with self.assertRaises(TypeError):
            LuisRecognizer.top_intent(none_results)

    def test_top_intent_returns_top_intent_if_score_equals_min_score(self):
        default_intent: str = LuisRecognizer.top_intent(
            self._mocked_results, min_score=0.4
        )
        self.assertEqual(default_intent, "Greeting")

    def test_telemetry_construction(self):
        # Arrange
        # Note this is NOT a real LUIS application ID nor a real LUIS subscription-key
        # theses are GUIDs edited to look right to the parsing and validation code.
        endpoint = (
            "https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/"
            "b31aeaf3-3511-495b-a07f-571fc873214b?verbose=true&timezoneOffset=-360"
            "&subscription-key=048ec46dc58e495482b0c447cfdbd291&q="
        )

        # Act
        recognizer = LuisRecognizer(endpoint)

        # Assert
        app = recognizer._application
        self.assertEqual("b31aeaf3-3511-495b-a07f-571fc873214b", app.application_id)
        self.assertEqual("048ec46dc58e495482b0c447cfdbd291", app.endpoint_key)
        self.assertEqual("https://westus.api.cognitive.microsoft.com", app.endpoint)

    async def test_telemetry_override_on_log_async(self):
        # Arrange
        utterance: str = "please book from May 5 to June 6"
        response_json: Dict[str, object] = self._empty_luis_response
        telemetry_client = mock.create_autospec(BotTelemetryClient)
        options = LuisPredictionOptions(
            telemetry_client=telemetry_client, log_personal_information=False
        )
        telemetry_properties: Dict[str, str] = {"test": "testvalue", "foo": "foovalue"}

        # Act
        await LuisRecognizerTest._get_recognizer_result(
            utterance,
            response_json,
            bot_adapter=NullAdapter(),
            options=options,
            telemetry_properties=telemetry_properties,
        )

        # Assert
        self.assertEqual(1, telemetry_client.track_event.call_count)
        args = telemetry_client.track_event.call_args[0]
        self.assertEqual("LuisResult", args[0])
        self.assertTrue("applicationId" in args[1])
        self.assertTrue("intent" in args[1])
        self.assertTrue("intentScore" in args[1])
        self.assertTrue("fromId" in args[1])
        self.assertTrue("entities" in args[1])

    async def test_telemetry_pii_logged_async(self):
        # Arrange
        utterance: str = "please book from May 5 to June 6"
        response_json: Dict[str, object] = self._empty_luis_response
        telemetry_client = mock.create_autospec(BotTelemetryClient)
        options = LuisPredictionOptions(
            telemetry_client=telemetry_client, log_personal_information=True
        )

        # Act
        await LuisRecognizerTest._get_recognizer_result(
            utterance,
            response_json,
            bot_adapter=NullAdapter(),
            options=options,
            telemetry_properties=None,
        )

        # Assert
        self.assertEqual(1, telemetry_client.track_event.call_count)
        args = telemetry_client.track_event.call_args[0]
        self.assertEqual("LuisResult", args[0])
        self.assertEqual(8, len(args[1]))
        self.assertTrue("applicationId" in args[1])
        self.assertTrue("intent" in args[1])
        self.assertTrue("intentScore" in args[1])
        self.assertTrue("intent2" in args[1])
        self.assertTrue("intentScore2" in args[1])
        self.assertTrue("fromId" in args[1])
        self.assertTrue("entities" in args[1])
        self.assertTrue("question" in args[1])

    async def test_telemetry_no_pii_logged_async(self):
        # Arrange
        utterance: str = "please book from May 5 to June 6"
        response_json: Dict[str, object] = self._empty_luis_response
        telemetry_client = mock.create_autospec(BotTelemetryClient)
        options = LuisPredictionOptions(
            telemetry_client=telemetry_client, log_personal_information=False
        )

        # Act
        await LuisRecognizerTest._get_recognizer_result(
            utterance,
            response_json,
            bot_adapter=NullAdapter(),
            options=options,
            telemetry_properties=None,
        )

        # Assert
        self.assertEqual(1, telemetry_client.track_event.call_count)
        args = telemetry_client.track_event.call_args[0]
        self.assertEqual("LuisResult", args[0])
        self.assertEqual(7, len(args[1]))
        self.assertTrue("applicationId" in args[1])
        self.assertTrue("intent" in args[1])
        self.assertTrue("intentScore" in args[1])
        self.assertTrue("intent2" in args[1])
        self.assertTrue("intentScore2" in args[1])
        self.assertTrue("fromId" in args[1])
        self.assertTrue("entities" in args[1])
        self.assertFalse("question" in args[1])

    async def test_telemetry_override_on_derive_async(self):
        # Arrange
        utterance: str = "please book from May 5 to June 6"
        response_json: Dict[str, object] = self._empty_luis_response
        telemetry_client = mock.create_autospec(BotTelemetryClient)
        options = LuisPredictionOptions(
            telemetry_client=telemetry_client, log_personal_information=False
        )
        telemetry_properties: Dict[str, str] = {"test": "testvalue", "foo": "foovalue"}

        # Act
        await LuisRecognizerTest._get_recognizer_result(
            utterance,
            response_json,
            bot_adapter=NullAdapter(),
            options=options,
            telemetry_properties=telemetry_properties,
            recognizer_class=TelemetryOverrideRecognizer,
        )

        # Assert
        self.assertEqual(2, telemetry_client.track_event.call_count)
        call0_args = telemetry_client.track_event.call_args_list[0][0]
        self.assertEqual("LuisResult", call0_args[0])
        self.assertTrue("MyImportantProperty" in call0_args[1])
        self.assertTrue(call0_args[1]["MyImportantProperty"] == "myImportantValue")
        self.assertTrue("test" in call0_args[1])
        self.assertTrue(call0_args[1]["test"] == "testvalue")
        self.assertTrue("foo" in call0_args[1])
        self.assertTrue(call0_args[1]["foo"] == "foovalue")
        call1_args = telemetry_client.track_event.call_args_list[1][0]
        self.assertEqual("MySecondEvent", call1_args[0])
        self.assertTrue("MyImportantProperty2" in call1_args[1])
        self.assertTrue(call1_args[1]["MyImportantProperty2"] == "myImportantValue2")

    async def test_telemetry_override_fill_async(self):
        # Arrange
        utterance: str = "please book from May 5 to June 6"
        response_json: Dict[str, object] = self._empty_luis_response
        telemetry_client = mock.create_autospec(BotTelemetryClient)
        options = LuisPredictionOptions(
            telemetry_client=telemetry_client, log_personal_information=False
        )
        additional_properties: Dict[str, str] = {"test": "testvalue", "foo": "foovalue"}
        additional_metrics: Dict[str, str] = {"moo": 3.14159, "boo": 2.11}

        # Act
        await LuisRecognizerTest._get_recognizer_result(
            utterance,
            response_json,
            bot_adapter=NullAdapter(),
            options=options,
            telemetry_properties=additional_properties,
            telemetry_metrics=additional_metrics,
            recognizer_class=OverrideFillRecognizer,
        )

        # Assert
        self.assertEqual(2, telemetry_client.track_event.call_count)
        call0_args = telemetry_client.track_event.call_args_list[0][0]
        self.assertEqual("LuisResult", call0_args[0])
        self.assertTrue("MyImportantProperty" in call0_args[1])
        self.assertTrue(call0_args[1]["MyImportantProperty"] == "myImportantValue")
        self.assertTrue("test" in call0_args[1])
        self.assertTrue(call0_args[1]["test"] == "testvalue")
        self.assertTrue("foo" in call0_args[1])
        self.assertTrue(call0_args[1]["foo"] == "foovalue")
        self.assertTrue("moo" in call0_args[2])
        self.assertTrue(call0_args[2]["moo"] == 3.14159)
        self.assertTrue("boo" in call0_args[2])
        self.assertTrue(call0_args[2]["boo"] == 2.11)

        call1_args = telemetry_client.track_event.call_args_list[1][0]
        self.assertEqual("MySecondEvent", call1_args[0])
        self.assertTrue("MyImportantProperty2" in call1_args[1])
        self.assertTrue(call1_args[1]["MyImportantProperty2"] == "myImportantValue2")

    async def test_telemetry_no_override_async(self):
        # Arrange
        utterance: str = "please book from May 5 to June 6"
        response_json: Dict[str, object] = self._empty_luis_response
        telemetry_client = mock.create_autospec(BotTelemetryClient)
        options = LuisPredictionOptions(
            telemetry_client=telemetry_client, log_personal_information=False
        )

        # Act
        await LuisRecognizerTest._get_recognizer_result(
            utterance, response_json, bot_adapter=NullAdapter(), options=options
        )

        # Assert
        self.assertEqual(1, telemetry_client.track_event.call_count)
        call0_args = telemetry_client.track_event.call_args_list[0][0]
        self.assertEqual("LuisResult", call0_args[0])
        self.assertTrue("intent" in call0_args[1])
        self.assertTrue("intentScore" in call0_args[1])
        self.assertTrue("fromId" in call0_args[1])
        self.assertTrue("entities" in call0_args[1])

    def test_pass_luis_prediction_options_to_recognizer(self):
        # Arrange
        my_app = LuisApplication(
            LuisRecognizerTest._luisAppId,
            LuisRecognizerTest._subscriptionKey,
            endpoint=None,
        )

        luis_prediction_options = LuisPredictionOptions(
            log_personal_information=True,
            include_all_intents=True,
            include_instance_data=True,
        )

        # Assert
        recognizer = LuisRecognizer(my_app)
        merged_options = recognizer._merge_options(luis_prediction_options)
        self.assertTrue(merged_options.log_personal_information)
        self.assertTrue(merged_options.include_all_intents)
        self.assertTrue(merged_options.include_instance_data)
        self.assertFalse(recognizer._options.log_personal_information)
        self.assertFalse(recognizer._options.include_all_intents)
        self.assertFalse(recognizer._options.include_instance_data)

    def test_dont_pass_luis_prediction_options_to_recognizer(self):
        # Arrange
        my_app = LuisApplication(
            LuisRecognizerTest._luisAppId,
            LuisRecognizerTest._subscriptionKey,
            endpoint=None,
        )

        # Assert
        recognizer = LuisRecognizer(my_app)
        self.assertFalse(recognizer._options.log_personal_information)
        self.assertFalse(recognizer._options.include_all_intents)
        self.assertFalse(recognizer._options.include_instance_data)

    async def test_composite1(self):
        await self._test_json("Composite1.json")

    async def test_composite2(self):
        await self._test_json("Composite2.json")

    async def test_composite3(self):
        await self._test_json("Composite3.json")

    async def test_prebuilt_domains(self):
        await self._test_json("Prebuilt.json")

    async def test_patterns(self):
        await self._test_json("Patterns.json")

    def assert_score(self, score: float) -> None:
        self.assertTrue(score >= 0)
        self.assertTrue(score <= 1)

    async def _test_json(self, response_file: str) -> None:
        # Arrange
        expected_json = LuisRecognizerTest._get_json_for_file(response_file)
        response_json = expected_json["luisResult"]
        utterance = expected_json.get("text")
        if utterance is None:
            utterance = expected_json.get("Text")

        options = LuisPredictionOptions(include_all_intents=True)

        # Act
        _, result = await LuisRecognizerTest._get_recognizer_result(
            utterance, response_json, options=options, include_api_results=True
        )

        # Assert
        actual_result_json = LuisUtil.recognizer_result_as_dict(result)
        trimmed_expected = LuisRecognizerTest._remove_none_property(expected_json)
        trimmed_actual = LuisRecognizerTest._remove_none_property(actual_result_json)
        self.assertEqual(trimmed_expected, trimmed_actual)

    @staticmethod
    def _remove_none_property(dictionary: Dict[str, object]) -> Dict[str, object]:
        for key, value in list(dictionary.items()):
            if value is None:
                del dictionary[key]
            elif isinstance(value, dict):
                LuisRecognizerTest._remove_none_property(value)
        return dictionary

    @classmethod
    async def _get_recognizer_result(
        cls,
        utterance: str,
        response_json: Union[str, Dict[str, object]],
        bot_adapter: BotAdapter = TestAdapter(),
        options: LuisPredictionOptions = None,
        include_api_results: bool = False,
        telemetry_properties: Dict[str, str] = None,
        telemetry_metrics: Dict[str, float] = None,
        recognizer_class: type = LuisRecognizer,
    ) -> Tuple[LuisRecognizer, RecognizerResult]:
        if isinstance(response_json, str):
            response_json = LuisRecognizerTest._get_json_for_file(
                response_file=response_json
            )

        recognizer = LuisRecognizerTest._get_luis_recognizer(
            recognizer_class, include_api_results=include_api_results, options=options
        )
        context = LuisRecognizerTest._get_context(utterance, bot_adapter)
        response = Mock(spec=Response)
        response.status_code = 200
        response.headers = {}
        response.reason = ""
        with mock.patch.object(Session, "send", return_value=response):
            with mock.patch.object(
                Deserializer, "_unpack_content", return_value=response_json
            ):
                result = await recognizer.recognize(
                    context, telemetry_properties, telemetry_metrics
                )
                return recognizer, result

    @classmethod
    def _get_json_for_file(cls, response_file: str) -> Dict[str, object]:
        curr_dir = path.dirname(path.abspath(__file__))
        response_path = path.join(curr_dir, "test_data", response_file)

        with open(response_path, "r", encoding="utf-8-sig") as file:
            response_str = file.read()
        response_json = json.loads(response_str)
        return response_json

    @classmethod
    def _get_luis_recognizer(
        cls,
        recognizer_class: type,
        options: LuisPredictionOptions = None,
        include_api_results: bool = False,
    ) -> LuisRecognizer:
        luis_app = LuisApplication(cls._luisAppId, cls._subscriptionKey, cls._endpoint)
        return recognizer_class(
            luis_app,
            prediction_options=options,
            include_api_results=include_api_results,
        )

    @staticmethod
    def _get_context(utterance: str, bot_adapter: BotAdapter) -> TurnContext:
        activity = Activity(
            type=ActivityTypes.message,
            text=utterance,
            conversation=ConversationAccount(),
            recipient=ChannelAccount(),
            from_property=ChannelAccount(),
        )
        return TurnContext(bot_adapter, activity)
