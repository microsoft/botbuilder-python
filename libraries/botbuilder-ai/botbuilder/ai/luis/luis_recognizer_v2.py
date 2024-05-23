# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import Dict
from azure.cognitiveservices.language.luis.runtime import LUISRuntimeClient
from azure.cognitiveservices.language.luis.runtime.models import LuisResult
from msrest.authentication import CognitiveServicesCredentials
from botbuilder.core import (
    TurnContext,
    RecognizerResult,
)
from .luis_recognizer_internal import LuisRecognizerInternal
from .luis_recognizer_options_v2 import LuisRecognizerOptionsV2
from .luis_application import LuisApplication
from .luis_util import LuisUtil

from .activity_util import ActivityUtil


class LuisRecognizerV2(LuisRecognizerInternal):
    # The value type for a LUIS trace activity.
    luis_trace_type: str = "https://www.luis.ai/schemas/trace"

    # The context label for a LUIS trace activity.
    luis_trace_label: str = "Luis Trace"

    def __init__(
        self,
        luis_application: LuisApplication,
        luis_recognizer_options_v2: LuisRecognizerOptionsV2 = None,
    ):
        super().__init__(luis_application)
        credentials = CognitiveServicesCredentials(luis_application.endpoint_key)
        self._runtime = LUISRuntimeClient(luis_application.endpoint, credentials)
        self._runtime.config.add_user_agent(LuisUtil.get_user_agent())
        self._runtime.config.connection.timeout = (
            luis_recognizer_options_v2.timeout // 1000
        )
        self.luis_recognizer_options_v2 = (
            luis_recognizer_options_v2 or LuisRecognizerOptionsV2()
        )
        self._application = luis_application

    async def recognizer_internal(self, turn_context: TurnContext):
        utterance: str = (
            turn_context.activity.text if turn_context.activity is not None else None
        )
        luis_result: LuisResult = self._runtime.prediction.resolve(
            self._application.application_id,
            utterance,
            timezone_offset=self.luis_recognizer_options_v2.timezone_offset,
            verbose=self.luis_recognizer_options_v2.include_all_intents,
            staging=self.luis_recognizer_options_v2.staging,
            spell_check=self.luis_recognizer_options_v2.spell_check,
            bing_spell_check_subscription_key=self.luis_recognizer_options_v2.bing_spell_check_subscription_key,
            log=(
                self.luis_recognizer_options_v2.log
                if self.luis_recognizer_options_v2.log is not None
                else True
            ),
        )

        recognizer_result: RecognizerResult = RecognizerResult(
            text=utterance,
            altered_text=luis_result.altered_query,
            intents=LuisUtil.get_intents(luis_result),
            entities=LuisUtil.extract_entities_and_metadata(
                luis_result.entities,
                luis_result.composite_entities,
                (
                    self.luis_recognizer_options_v2.include_instance_data
                    if self.luis_recognizer_options_v2.include_instance_data is not None
                    else True
                ),
            ),
        )

        LuisUtil.add_properties(luis_result, recognizer_result)
        if self.luis_recognizer_options_v2.include_api_results:
            recognizer_result.properties["luisResult"] = luis_result

        await self._emit_trace_info(
            turn_context,
            luis_result,
            recognizer_result,
            self.luis_recognizer_options_v2,
        )

        return recognizer_result

    async def _emit_trace_info(
        self,
        turn_context: TurnContext,
        luis_result: LuisResult,
        recognizer_result: RecognizerResult,
        options: LuisRecognizerOptionsV2,
    ) -> None:
        trace_info: Dict[str, object] = {
            "recognizerResult": LuisUtil.recognizer_result_as_dict(recognizer_result),
            "luisModel": {"ModelID": self._application.application_id},
            "luisOptions": {"Staging": options.staging},
            "luisResult": LuisUtil.luis_result_as_dict(luis_result),
        }

        trace_activity = ActivityUtil.create_trace(
            turn_context.activity,
            "LuisRecognizer",
            trace_info,
            LuisRecognizerV2.luis_trace_type,
            LuisRecognizerV2.luis_trace_label,
        )

        await turn_context.send_activity(trace_activity)
