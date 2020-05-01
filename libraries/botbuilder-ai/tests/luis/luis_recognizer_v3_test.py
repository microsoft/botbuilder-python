# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

# pylint: disable=protected-access

import json
from os import path
from typing import Dict, Tuple, Union

from aiounittest import AsyncTestCase

from botbuilder.ai.luis import LuisRecognizerOptionsV3

from asynctest import CoroutineMock, patch

from botbuilder.ai.luis import LuisApplication, LuisPredictionOptions, LuisRecognizer
from botbuilder.ai.luis.luis_util import LuisUtil
from botbuilder.core import (
    BotAdapter,
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


class LuisRecognizerV3Test(AsyncTestCase):
    _luisAppId: str = "b31aeaf3-3511-495b-a07f-571fc873214b"
    _subscriptionKey: str = "048ec46dc58e495482b0c447cfdbd291"
    _endpoint: str = "https://westus.api.cognitive.microsoft.com"

    def __init__(self, *args, **kwargs):
        super(LuisRecognizerV3Test, self).__init__(*args, **kwargs)
        self._mocked_results: RecognizerResult = RecognizerResult(
            intents={"Test": IntentScore(score=0.2), "Greeting": IntentScore(score=0.4)}
        )
        self._empty_luis_response: Dict[str, object] = json.loads(
            '{ "query": null, "intents": [], "entities": [] }'
        )

    @staticmethod
    def _remove_none_property(dictionary: Dict[str, object]) -> Dict[str, object]:
        for key, value in list(dictionary.items()):
            if value is None:
                del dictionary[key]
            elif isinstance(value, dict):
                LuisRecognizerV3Test._remove_none_property(value)
        return dictionary

    @classmethod
    @patch('aiohttp.ClientSession.post')
    async def _get_recognizer_result(
        cls,
        utterance: str,
        response_json: Union[str, Dict[str, object]],
        mock_get,
        bot_adapter: BotAdapter = TestAdapter(),
        options: Union[LuisRecognizerOptionsV3, LuisPredictionOptions] = None,
        include_api_results: bool = False,
        telemetry_properties: Dict[str, str] = None,
        telemetry_metrics: Dict[str, float] = None,
        recognizer_class: type = LuisRecognizer,

    ) -> Tuple[LuisRecognizer, RecognizerResult]:
        if isinstance(response_json, str):
            response_json = LuisRecognizerV3Test._get_json_for_file(
                response_file=response_json
            )

        recognizer = LuisRecognizerV3Test._get_luis_recognizer(
            recognizer_class, include_api_results=include_api_results, options=options
        )
        context = LuisRecognizerV3Test._get_context(utterance, bot_adapter)
        mock_get.return_value.__aenter__.return_value.json = CoroutineMock(side_effect=[response_json])

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
        options: Union[LuisPredictionOptions, LuisRecognizerOptionsV3] = None,
        include_api_results: bool = False,
    ) -> LuisRecognizer:
        luis_app = LuisApplication(cls._luisAppId, cls._subscriptionKey, cls._endpoint)

        if isinstance(options, LuisRecognizerOptionsV3):
            LuisRecognizerOptionsV3.include_api_results = include_api_results

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

    # Luis V3 endpoint tests begin here
    async def _test_json_v3(self, response_file: str) -> None:
        # Arrange
        expected_json = LuisRecognizerV3Test._get_json_for_file(response_file)
        response_json = expected_json["v3"]["response"]
        utterance = expected_json.get("text")
        if utterance is None:
            utterance = expected_json.get("Text")

        test_options = expected_json["v3"]["options"]

        options = LuisRecognizerOptionsV3(
            include_all_intents = test_options["includeAllIntents"],
            include_instance_data=test_options["includeInstanceData"],
            log=test_options["log"],
            prefer_external_entities=test_options["preferExternalEntities"],
            slot=test_options["slot"],
            include_api_results = test_options["includeAPIResults"],
        )

        if "version" in test_options:
            options.version=test_options["version"]

        # dynamic_lists: List = None,
        # external_entities: List = None,
        # telemetry_client: BotTelemetryClient = NullTelemetryClient(),
        # log_personal_information: bool = False,)
        # ,

        # Act
        _, result = await LuisRecognizerV3Test._get_recognizer_result(
            utterance, response_json, options=options, include_api_results=True
        )

        # Assert
        actual_result_json = LuisUtil.recognizer_result_as_dict(result)
        del expected_json["v3"]
        del expected_json["sentiment"]
        trimmed_expected = LuisRecognizerV3Test._remove_none_property(expected_json)
        trimmed_actual = LuisRecognizerV3Test._remove_none_property(actual_result_json)
        self.assertEqual(trimmed_expected, trimmed_actual)

    async def test_composite1_v3(self):
        await self._test_json_v3("Composite1_v3.json")

    async def test_composite2_v3(self):
        await self._test_json_v3("Composite2_v3.json")

    async def test_composite3_v3(self):
        await self._test_json_v3("Composite3_v3.json")