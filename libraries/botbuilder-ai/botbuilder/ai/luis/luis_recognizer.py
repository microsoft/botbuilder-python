# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import json
from typing import Dict, List, Tuple, Union

from azure.cognitiveservices.language.luis.runtime import LUISRuntimeClient
from azure.cognitiveservices.language.luis.runtime.models import LuisResult
from msrest.authentication import CognitiveServicesCredentials

from botbuilder.core import (
    BotAssert,
    IntentScore,
    Recognizer,
    RecognizerResult,
    TurnContext,
)
from botbuilder.schema import ActivityTypes

from . import LuisApplication, LuisPredictionOptions, LuisTelemetryConstants
from .activity_util import ActivityUtil
from .luis_util import LuisUtil


class LuisRecognizer(Recognizer):
    """
    A LUIS based implementation of <see cref="IRecognizer"/>.
    """

    # The value type for a LUIS trace activity.
    luis_trace_type: str = "https://www.luis.ai/schemas/trace"

    # The context label for a LUIS trace activity.
    luis_trace_label: str = "Luis Trace"

    def __init__(
        self,
        application: Union[LuisApplication, str],
        prediction_options: LuisPredictionOptions = None,
        include_api_results: bool = False,
    ):
        """Initializes a new instance of the <see cref="LuisRecognizer"/> class.
        :param application: The LUIS application to use to recognize text.
        :type application: LuisApplication
        :param prediction_options: The LUIS prediction options to use, defaults to None
        :param prediction_options: LuisPredictionOptions, optional
        :param include_api_results: True to include raw LUIS API response, defaults to False
        :param include_api_results: bool, optional
        :raises TypeError:
        """

        if isinstance(application, LuisApplication):
            self._application = application
        elif isinstance(application, str):
            self._application = LuisApplication.from_application_endpoint(application)
        else:
            raise TypeError(
                "LuisRecognizer.__init__(): application is not an instance of LuisApplication or str."
            )

        self._options = prediction_options or LuisPredictionOptions()

        self._include_api_results = include_api_results

        self.telemetry_client = self._options.telemetry_client
        self.log_personal_information = self._options.log_personal_information

        credentials = CognitiveServicesCredentials(self._application.endpoint_key)
        self._runtime = LUISRuntimeClient(self._application.endpoint, credentials)
        self._runtime.config.add_user_agent(LuisUtil.get_user_agent())
        self._runtime.config.connection.timeout = self._options.timeout // 1000

    @staticmethod
    def top_intent(
        results: RecognizerResult, default_intent: str = "None", min_score: float = 0.0
    ) -> str:
        """Returns the name of the top scoring intent from a set of LUIS results.
        :param results: Result set to be searched.
        :type results: RecognizerResult
        :param default_intent: Intent name to return should a top intent be found, defaults to "None"
        :param default_intent: str, optional
        :param min_score: Minimum score needed for an intent to be considered as a top intent. If all intents in the
         set are below this threshold then the `defaultIntent` will be returned, defaults to 0.0
        :param min_score: float, optional
        :raises TypeError:
        :return: The top scoring intent name.
        :rtype: str
        """

        if results is None:
            raise TypeError("LuisRecognizer.top_intent(): results cannot be None.")

        top_intent: str = None
        top_score: float = -1.0
        if results.intents:
            for intent_name, intent_score in results.intents.items():
                score = intent_score.score
                if score > top_score and score >= min_score:
                    top_intent = intent_name
                    top_score = score

        return top_intent or default_intent

    async def recognize(  # pylint: disable=arguments-differ
        self,
        turn_context: TurnContext,
        telemetry_properties: Dict[str, str] = None,
        telemetry_metrics: Dict[str, float] = None,
        luis_prediction_options: LuisPredictionOptions = None,
    ) -> RecognizerResult:
        """Return results of the analysis (Suggested actions and intents).
        :param turn_context: Context object containing information for a single turn of conversation with a user.
        :type turn_context: TurnContext
        :param telemetry_properties: Additional properties to be logged to telemetry with the LuisResult event, defaults
         to None
        :param telemetry_properties: Dict[str, str], optional
        :param telemetry_metrics: Additional metrics to be logged to telemetry with the LuisResult event, defaults to
         None
        :param telemetry_metrics: Dict[str, float], optional
        :return: The LUIS results of the analysis of the current message text in the current turn's context activity.
        :rtype: RecognizerResult
        """

        return await self._recognize_internal(
            turn_context,
            telemetry_properties,
            telemetry_metrics,
            luis_prediction_options,
        )

    def on_recognizer_result(
        self,
        recognizer_result: RecognizerResult,
        turn_context: TurnContext,
        telemetry_properties: Dict[str, str] = None,
        telemetry_metrics: Dict[str, float] = None,
    ):
        """Invoked prior to a LuisResult being logged.
        :param recognizer_result: The Luis Results for the call.
        :type recognizer_result: RecognizerResult
        :param turn_context: Context object containing information for a single turn of conversation with a user.
        :type turn_context: TurnContext
        :param telemetry_properties: Additional properties to be logged to telemetry with the LuisResult event, defaults
         to None
        :param telemetry_properties: Dict[str, str], optional
        :param telemetry_metrics: Additional metrics to be logged to telemetry with the LuisResult event, defaults to
         None
        :param telemetry_metrics: Dict[str, float], optional
        """

        properties = self.fill_luis_event_properties(
            recognizer_result, turn_context, telemetry_properties
        )

        # Track the event
        self.telemetry_client.track_event(
            LuisTelemetryConstants.luis_result, properties, telemetry_metrics
        )

    @staticmethod
    def _get_top_k_intent_score(
        intent_names: List[str],
        intents: Dict[str, IntentScore],
        index: int,  # pylint: disable=unused-argument
    ) -> Tuple[str, str]:
        intent_name = ""
        intent_score = "0.00"
        if intent_names:
            intent_name = intent_names[0]
            if intents[intent_name] is not None:
                intent_score = "{:.2f}".format(intents[intent_name].score)

        return intent_name, intent_score

    def fill_luis_event_properties(
        self,
        recognizer_result: RecognizerResult,
        turn_context: TurnContext,
        telemetry_properties: Dict[str, str] = None,
    ) -> Dict[str, str]:
        """Fills the event properties for LuisResult event for telemetry.
        These properties are logged when the recognizer is called.
        :param recognizer_result: Last activity sent from user.
        :type recognizer_result: RecognizerResult
        :param turn_context: Context object containing information for a single turn of conversation with a user.
        :type turn_context: TurnContext
        :param telemetry_properties: Additional properties to be logged to telemetry with the LuisResult event,
         defaults to None
        :param telemetry_properties: Dict[str, str], optional
        :return: A dictionary that is sent as "Properties" to IBotTelemetryClient.TrackEvent method for the
         BotMessageSend event.
        :rtype: Dict[str, str]
        """

        intents = recognizer_result.intents
        top_two_intents = (
            sorted(intents.keys(), key=lambda k: intents[k].score, reverse=True)[:2]
            if intents
            else []
        )

        intent_name, intent_score = LuisRecognizer._get_top_k_intent_score(
            top_two_intents, intents, index=0
        )
        intent2_name, intent2_score = LuisRecognizer._get_top_k_intent_score(
            top_two_intents, intents, index=1
        )

        # Add the intent score and conversation id properties
        properties: Dict[str, str] = {
            LuisTelemetryConstants.application_id_property: self._application.application_id,
            LuisTelemetryConstants.intent_property: intent_name,
            LuisTelemetryConstants.intent_score_property: intent_score,
            LuisTelemetryConstants.intent2_property: intent2_name,
            LuisTelemetryConstants.intent_score2_property: intent2_score,
            LuisTelemetryConstants.from_id_property: turn_context.activity.from_property.id,
        }

        sentiment = recognizer_result.properties.get("sentiment")
        if sentiment is not None and isinstance(sentiment, Dict):
            label = sentiment.get("label")
            if label is not None:
                properties[LuisTelemetryConstants.sentiment_label_property] = str(label)

            score = sentiment.get("score")
            if score is not None:
                properties[LuisTelemetryConstants.sentiment_score_property] = str(score)

        entities = None
        if recognizer_result.entities is not None:
            entities = json.dumps(recognizer_result.entities)
        properties[LuisTelemetryConstants.entities_property] = entities

        # Use the LogPersonalInformation flag to toggle logging PII data, text is a common example
        if self.log_personal_information and turn_context.activity.text:
            properties[
                LuisTelemetryConstants.question_property
            ] = turn_context.activity.text

        # Additional Properties can override "stock" properties.
        if telemetry_properties is not None:
            for key in telemetry_properties:
                properties[key] = telemetry_properties[key]

        return properties

    async def _recognize_internal(
        self,
        turn_context: TurnContext,
        telemetry_properties: Dict[str, str],
        telemetry_metrics: Dict[str, float],
        luis_prediction_options: LuisPredictionOptions = None,
    ) -> RecognizerResult:

        BotAssert.context_not_none(turn_context)

        if turn_context.activity.type != ActivityTypes.message:
            return None

        utterance: str = turn_context.activity.text if turn_context.activity is not None else None
        recognizer_result: RecognizerResult = None
        luis_result: LuisResult = None

        if luis_prediction_options:
            options = self._merge_options(luis_prediction_options)
        else:
            options = self._options

        if not utterance or utterance.isspace():
            recognizer_result = RecognizerResult(
                text=utterance, intents={"": IntentScore(score=1.0)}, entities={}
            )
        else:
            luis_result = self._runtime.prediction.resolve(
                self._application.application_id,
                utterance,
                timezone_offset=options.timezone_offset,
                verbose=options.include_all_intents,
                staging=options.staging,
                spell_check=options.spell_check,
                bing_spell_check_subscription_key=options.bing_spell_check_subscription_key,
                log=options.log if options.log is not None else True,
            )

            recognizer_result = RecognizerResult(
                text=utterance,
                altered_text=luis_result.altered_query,
                intents=LuisUtil.get_intents(luis_result),
                entities=LuisUtil.extract_entities_and_metadata(
                    luis_result.entities,
                    luis_result.composite_entities,
                    options.include_instance_data
                    if options.include_instance_data is not None
                    else True,
                ),
            )
            LuisUtil.add_properties(luis_result, recognizer_result)
            if self._include_api_results:
                recognizer_result.properties["luisResult"] = luis_result

        # Log telemetry
        self.on_recognizer_result(
            recognizer_result, turn_context, telemetry_properties, telemetry_metrics
        )

        await self._emit_trace_info(
            turn_context, luis_result, recognizer_result, options
        )

        return recognizer_result

    async def _emit_trace_info(
        self,
        turn_context: TurnContext,
        luis_result: LuisResult,
        recognizer_result: RecognizerResult,
        options: LuisPredictionOptions,
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
            LuisRecognizer.luis_trace_type,
            LuisRecognizer.luis_trace_label,
        )

        await turn_context.send_activity(trace_activity)

    def _merge_options(
        self, user_defined_options: LuisPredictionOptions
    ) -> LuisPredictionOptions:
        merged_options = LuisPredictionOptions()
        merged_options.__dict__.update(user_defined_options.__dict__)
        return merged_options
