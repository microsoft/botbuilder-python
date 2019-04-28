# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import json
import unittest
from os import path
from typing import Tuple
from unittest.mock import Mock, patch

import requests
from azure.cognitiveservices.language.luis.runtime import LUISRuntimeClient
from azure.cognitiveservices.language.luis.runtime.luis_runtime_client import (
    LUISRuntimeClientConfiguration,
)
from msrest import Deserializer
from requests.models import Response

from botbuilder.ai.luis import (
    IntentScore,
    LuisApplication,
    LuisPredictionOptions,
    LuisRecognizer,
    RecognizerResult,
    TopIntent,
)
from botbuilder.core import BotAdapter, TurnContext
from botbuilder.core.adapters import TestAdapter
from botbuilder.schema import (
    Activity,
    ActivityTypes,
    ChannelAccount,
    ConversationAccount,
)

from .null_adapter import NullAdapter


class LuisRecognizerTest(unittest.TestCase):
    _luisAppId: str = "b31aeaf3-3511-495b-a07f-571fc873214b"
    _subscriptionKey: str = "048ec46dc58e495482b0c447cfdbd291"
    _endpoint: str = "https://westus.api.cognitive.microsoft.com"

    def __init__(self, *args, **kwargs):
        super(LuisRecognizerTest, self).__init__(*args, **kwargs)
        self._mocked_results: RecognizerResult = RecognizerResult(
            intents={"Test": IntentScore(score=0.2), "Greeting": IntentScore(score=0.4)}
        )

    def test_luis_recognizer_construction(self):
        # Arrange
        endpoint = "https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/b31aeaf3-3511-495b-a07f-571fc873214b?verbose=true&timezoneOffset=-360&subscription-key=048ec46dc58e495482b0c447cfdbd291&q="

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

    def test_single_intent_simply_entity(self):
        utterance: str = "My name is Emad"
        response_path: str = "SingleIntent_SimplyEntity.json"

        _, result = LuisRecognizerTest._get_recognizer_result(utterance, response_path)

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

    def test_null_utterance(self):
        utterance: str = None
        response_path: str = "SingleIntent_SimplyEntity.json"  # The path is irrelevant in this case

        _, result = LuisRecognizerTest._get_recognizer_result(utterance, response_path)

        self.assertIsNotNone(result)
        self.assertIsNone(result.altered_text)
        self.assertEqual(utterance, result.text)
        self.assertIsNotNone(result.intents)
        self.assertEqual(1, len(result.intents))
        self.assertIsNotNone(result.intents[""])
        self.assertEqual(result.get_top_scoring_intent(), ("", 1.0))
        self.assertIsNotNone(result.entities)
        self.assertEqual(0, len(result.entities))

    def test_multiple_intents_prebuilt_entity(self):
        utterance: str = "Please deliver February 2nd 2001"
        response_path: str = "MultipleIntents_PrebuiltEntity.json"

        _, result = LuisRecognizerTest._get_recognizer_result(utterance, response_path)

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

    def test_multiple_intents_prebuilt_entities_with_multi_values(self):
        utterance: str = "Please deliver February 2nd 2001 in room 201"
        response_path: str = "MultipleIntents_PrebuiltEntitiesWithMultiValues.json"

        _, result = LuisRecognizerTest._get_recognizer_result(utterance, response_path)

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

    def test_multiple_intents_list_entity_with_single_value(self):
        utterance: str = "I want to travel on united"
        response_path: str = "MultipleIntents_ListEntityWithSingleValue.json"

        _, result = LuisRecognizerTest._get_recognizer_result(utterance, response_path)

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

    def test_multiple_intents_list_entity_with_multi_values(self):
        utterance: str = "I want to travel on DL"
        response_path: str = "MultipleIntents_ListEntityWithMultiValues.json"

        _, result = LuisRecognizerTest._get_recognizer_result(utterance, response_path)

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

    def test_multiple_intents_composite_entity_model(self):
        utterance: str = "Please deliver it to 98033 WA"
        response_path: str = "MultipleIntents_CompositeEntityModel.json"

        _, result = LuisRecognizerTest._get_recognizer_result(utterance, response_path)

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

    def test_multiple_date_time_entities(self):
        utterance: str = "Book a table on Friday or tomorrow at 5 or tomorrow at 4"
        response_path: str = "MultipleDateTimeEntities.json"

        _, result = LuisRecognizerTest._get_recognizer_result(utterance, response_path)

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

    def test_v1_datetime_resolution(self):
        utterance: str = "at 4"
        response_path: str = "V1DatetimeResolution.json"

        _, result = LuisRecognizerTest._get_recognizer_result(utterance, response_path)

        self.assertIsNotNone(result.entities["datetime_time"])
        self.assertEqual(1, len(result.entities["datetime_time"]))
        self.assertEqual("ampm", result.entities["datetime_time"][0]["comment"])
        self.assertEqual("T04", result.entities["datetime_time"][0]["time"])
        self.assertEqual(1, len(result.entities["$instance"]["datetime_time"]))

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

    def test_user_agent_contains_product_version(self):
        utterance: str = "please book from May 5 to June 6"
        response_path: str = "MultipleDateTimeEntities.json"  # it doesn't matter to use which file.

        recognizer, _ = LuisRecognizerTest._get_recognizer_result(
            utterance, response_path, bot_adapter=NullAdapter()
        )

        runtime: LUISRuntimeClient = recognizer._runtime
        config: LUISRuntimeClientConfiguration = runtime.config
        user_agent = config.user_agent

        # Verify we didn't unintentionally stamp on the user-agent from the client.
        self.assertTrue("azure-cognitiveservices-language-luis" in user_agent)

        # And that we added the bot.builder package details.
        self.assertTrue("botbuilder-ai/4" in user_agent)

    def assert_score(self, score: float) -> None:
        self.assertTrue(score >= 0)
        self.assertTrue(score <= 1)

    @classmethod
    def _get_recognizer_result(
        cls, utterance: str, response_file: str, bot_adapter: BotAdapter = TestAdapter()
    ) -> Tuple[LuisRecognizer, RecognizerResult]:
        response_json = LuisRecognizerTest._get_json_for_file(response_file)

        my_app = LuisApplication(
            LuisRecognizerTest._luisAppId,
            LuisRecognizerTest._subscriptionKey,
            endpoint="",
        )
        recognizer = LuisRecognizer(my_app, prediction_options=None)
        context = LuisRecognizerTest._get_context(utterance, bot_adapter)
        response = Mock(spec=Response)
        response.status_code = 200
        response.headers = {}
        response.reason = ""
        with patch("requests.Session.send", return_value=response):
            with patch(
                "msrest.serialization.Deserializer._unpack_content",
                return_value=response_json,
            ):
                result = recognizer.recognize(context)
                return recognizer, result

    @classmethod
    def _get_json_for_file(cls, response_file: str) -> object:
        curr_dir = path.dirname(path.abspath(__file__))
        response_path = path.join(curr_dir, "test_data", response_file)

        with open(response_path, "r", encoding="utf-8-sig") as f:
            response_str = f.read()
        response_json = json.loads(response_str)
        return response_json

    @classmethod
    def _get_luis_recognizer(
        cls, verbose: bool = False, options: LuisPredictionOptions = None
    ) -> LuisRecognizer:
        luis_app = LuisApplication(cls._luisAppId, cls._subscriptionKey, cls._endpoint)
        return LuisRecognizer(luis_app, options, verbose)

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
