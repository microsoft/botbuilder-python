# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import json
from typing import Dict, List, NamedTuple, Union
from aiohttp import ClientSession, ClientTimeout

from botbuilder.schema import Activity
from botbuilder.core import BotTelemetryClient, NullTelemetryClient, TurnContext

from .models import FeedbackRecord, QueryResult, QueryResults
from .utils import (
    ActiveLearningUtils,
    GenerateAnswerUtils,
    QnATelemetryConstants,
    TrainUtils,
)
from .qnamaker_endpoint import QnAMakerEndpoint
from .qnamaker_options import QnAMakerOptions
from .qnamaker_telemetry_client import QnAMakerTelemetryClient

from .. import __title__, __version__


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
        log_personal_information: bool = None,
    ):
        super().__init__(log_personal_information, telemetry_client)

        if not isinstance(endpoint, QnAMakerEndpoint):
            raise TypeError(
                "QnAMaker.__init__(): endpoint is not an instance of QnAMakerEndpoint"
            )

        self._endpoint: str = endpoint

        opt = options or QnAMakerOptions()
        self._validate_options(opt)

        instance_timeout = ClientTimeout(total=opt.timeout / 1000)
        self._http_client = http_client or ClientSession(timeout=instance_timeout)

        self.telemetry_client: Union[BotTelemetryClient, NullTelemetryClient] = (
            telemetry_client or NullTelemetryClient()
        )

        self.log_personal_information = log_personal_information or False

        self._generate_answer_helper = GenerateAnswerUtils(
            self.telemetry_client, self._endpoint, options, self._http_client
        )
        self._active_learning_train_helper = TrainUtils(
            self._endpoint, self._http_client
        )

    async def close(self):
        await self._http_client.close()

    async def get_answers(
        self,
        context: TurnContext,
        options: QnAMakerOptions = None,
        telemetry_properties: Dict[str, str] = None,
        telemetry_metrics: Dict[str, int] = None,
    ) -> [QueryResult]:
        """
        Generates answers from the knowledge base.

        :return: A list of answers for the user's query, sorted in decreasing order of ranking score.
        :rtype: :class:`typing.List[QueryResult]`
        """
        result = await self.get_answers_raw(
            context, options, telemetry_properties, telemetry_metrics
        )

        return result.answers

    async def get_answers_raw(
        self,
        context: TurnContext,
        options: QnAMakerOptions = None,
        telemetry_properties: Dict[str, str] = None,
        telemetry_metrics: Dict[str, int] = None,
    ) -> QueryResults:
        """
        Generates raw answers from the knowledge base.

        :return: A list of answers for the user's query, sorted in decreasing order of ranking score.
        :rtype: :class:`QueryResult`
        """
        if not context:
            raise TypeError("QnAMaker.get_answers(): context cannot be None.")

        if not isinstance(context.activity, Activity):
            raise TypeError(
                "QnAMaker.get_answers(): TurnContext's activity must be an Activity instance."
            )

        result = await self._generate_answer_helper.get_answers_raw(context, options)

        await self.on_qna_result(
            result.answers, context, telemetry_properties, telemetry_metrics
        )

        return result

    def get_low_score_variation(self, query_result: QueryResult) -> List[QueryResult]:
        """
        Filters the ambiguous question for active learning.

        :param query_result: User query output.
        :type query_result: :class:`QueryResult`
        :return: Filtered array of ambiguous questions.
        :rtype: :class:`typing.List[QueryResult]`
        """
        return ActiveLearningUtils.get_low_score_variation(query_result)

    async def call_train(self, feedback_records: List[FeedbackRecord]):
        """
        Sends feedback to the knowledge base.

        :param feedback_records: Feedback records.
        :type feedback_records: :class:`typing.List[FeedbackRecord]`
        """
        return await self._active_learning_train_helper.call_train(feedback_records)

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

        # Track the event
        self.telemetry_client.track_event(
            name=QnATelemetryConstants.qna_message_event,
            properties=event_data.properties,
            measurements=event_data.metrics,
        )

    async def fill_qna_event(
        self,
        query_results: [QueryResult],
        turn_context: TurnContext,
        telemetry_properties: Dict[str, str] = None,
        telemetry_metrics: Dict[str, float] = None,
    ) -> EventData:
        """
        Fills the event properties and metrics for the QnaMessage event for telemetry.

        :param query_results: QnA service results.
        :type quert_results: :class:`QueryResult`
        :param turn_context: Context object containing information for a single turn of conversation with a user.
        :type turn_context: :class:`botbuilder.core.TurnContext`
        :param telemetry_properties: Properties to add/override for the event.
        :type telemetry_properties: :class:`typing.Dict[str, str]`
        :param telemetry_metrics: Metrics to add/override for the event.
        :type telemetry_metrics: :class:`typing.Dict[str, float]`
        :return: Event properties and metrics for the QnaMessage event for telemetry.
        :rtype: :class:`EventData`
        """

        properties: Dict[str, str] = dict()
        metrics: Dict[str, float] = dict()

        properties[QnATelemetryConstants.knowledge_base_id_property] = (
            self._endpoint.knowledge_base_id
        )

        text: str = turn_context.activity.text
        user_name: str = turn_context.activity.from_property.name

        # Use the LogPersonalInformation flag to toggle logging PII data; text and username are common examples.
        if self.log_personal_information:
            if text:
                properties[QnATelemetryConstants.question_property] = text

            if user_name:
                properties[QnATelemetryConstants.username_property] = user_name

        # Fill in Qna Results (found or not).
        if self._has_matched_answer_in_kb(query_results):
            query_result = query_results[0]

            result_properties = {
                QnATelemetryConstants.matched_question_property: json.dumps(
                    query_result.questions
                ),
                QnATelemetryConstants.question_id_property: str(query_result.id),
                QnATelemetryConstants.answer_property: query_result.answer,
                QnATelemetryConstants.article_found_property: "true",
            }
            properties.update(result_properties)

            metrics[QnATelemetryConstants.score_metric] = query_result.score
        else:
            no_match_properties = {
                QnATelemetryConstants.matched_question_property: "No Qna Question matched",
                QnATelemetryConstants.question_id_property: "No Qna Question Id matched",
                QnATelemetryConstants.answer_property: "No Qna Answer matched",
                QnATelemetryConstants.article_found_property: "false",
            }

            properties.update(no_match_properties)

        # Additional Properties can override "stock" properties.
        if telemetry_properties:
            properties.update(telemetry_properties)

        # Additional Metrics can override "stock" metrics.
        if telemetry_metrics:
            metrics.update(telemetry_metrics)

        return EventData(properties=properties, metrics=metrics)

    def _validate_options(self, options: QnAMakerOptions):
        if not options.score_threshold:
            options.score_threshold = 0.3

        if not options.top:
            options.top = 1

        if options.score_threshold < 0 or options.score_threshold > 1:
            raise ValueError("Score threshold should be a value between 0 and 1")

        if options.top < 1:
            raise ValueError("QnAMakerOptions.top should be an integer greater than 0")

        if not options.strict_filters:
            options.strict_filters = []

        if not options.timeout:
            options.timeout = 100000

    def _has_matched_answer_in_kb(self, query_results: [QueryResult]) -> bool:
        if query_results:
            if query_results[0].id != -1:
                return True

        return False
