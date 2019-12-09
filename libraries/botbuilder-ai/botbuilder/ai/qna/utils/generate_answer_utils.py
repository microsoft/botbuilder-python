# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from copy import copy
from typing import List, Union

from aiohttp import ClientResponse, ClientSession

from botbuilder.core import BotTelemetryClient, NullTelemetryClient, TurnContext
from botbuilder.schema import Activity

from .http_request_utils import HttpRequestUtils

from ..qnamaker_endpoint import QnAMakerEndpoint
from ..qnamaker_options import QnAMakerOptions
from ..models import (
    GenerateAnswerRequestBody,
    QnAMakerTraceInfo,
    QueryResult,
    QueryResults,
)

QNAMAKER_TRACE_NAME = "QnAMaker"
QNAMAKER_TRACE_LABEL = "QnAMaker Trace"
QNAMAKER_TRACE_TYPE = "https://www.qnamaker.ai/schemas/trace"


class GenerateAnswerUtils:
    """
    Helper class for Generate Answer API, which is used to make queries to
    a single QnA Maker knowledge base and return the result.
    """

    def __init__(
        self,
        telemetry_client: Union[BotTelemetryClient, NullTelemetryClient],
        endpoint: QnAMakerEndpoint,
        options: QnAMakerOptions,
        http_client: ClientSession,
    ):
        """
        Parameters:
        -----------

        telemetry_client: Telemetry client.

        endpoint: QnA Maker endpoint details.

        options: QnA Maker options to configure the instance.

        http_client: HTTP client.
        """
        self._telemetry_client = telemetry_client
        self._endpoint = endpoint

        self.options = (
            options if isinstance(options, QnAMakerOptions) else QnAMakerOptions()
        )
        self._validate_options(self.options)

        self._http_client = http_client

    async def get_answers(
        self, context: TurnContext, options: QnAMakerOptions = None
    ) -> List[QueryResult]:
        result: QueryResults = await self.get_answers_raw(context, options)

        return result

    async def get_answers_raw(
        self, context: TurnContext, options: QnAMakerOptions = None
    ) -> QueryResults:
        if not isinstance(context, TurnContext):
            raise TypeError(
                "GenerateAnswerUtils.get_answers(): context must be an instance of TurnContext"
            )

        hydrated_options = self._hydrate_options(options)
        self._validate_options(hydrated_options)

        result: QueryResults = await self._query_qna_service(context, hydrated_options)

        await self._emit_trace_info(context, result.answers, hydrated_options)

        return result

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

    def _hydrate_options(self, query_options: QnAMakerOptions) -> QnAMakerOptions:
        """
        Combines QnAMakerOptions passed into the QnAMaker constructor
        with the options passed as arguments into get_answers().
        Return:
        -------
        QnAMakerOptions with options passed into constructor overwritten by new options passed into get_answers()

        rtype:
        ------
        QnAMakerOptions
        """

        hydrated_options = copy(self.options)

        if query_options:
            if (
                query_options.score_threshold != hydrated_options.score_threshold
                and query_options.score_threshold
            ):
                hydrated_options.score_threshold = query_options.score_threshold

            if query_options.top != hydrated_options.top and query_options.top != 0:
                hydrated_options.top = query_options.top

            if query_options.strict_filters:
                hydrated_options.strict_filters = query_options.strict_filters

            if (
                query_options.timeout != hydrated_options.timeout
                and query_options.timeout
            ):
                hydrated_options.timeout = query_options.timeout

            hydrated_options.context = query_options.context
            hydrated_options.qna_id = query_options.qna_id
            hydrated_options.is_test = query_options.is_test
            hydrated_options.ranker_type = query_options.ranker_type

        return hydrated_options

    async def _query_qna_service(
        self, turn_context: TurnContext, options: QnAMakerOptions
    ) -> QueryResults:
        url = f"{ self._endpoint.host }/knowledgebases/{ self._endpoint.knowledge_base_id }/generateAnswer"

        question = GenerateAnswerRequestBody(
            question=turn_context.activity.text,
            top=options.top,
            score_threshold=options.score_threshold,
            strict_filters=options.strict_filters,
            context=options.context,
            qna_id=options.qna_id,
            is_test=options.is_test,
            ranker_type=options.ranker_type,
        )

        http_request_helper = HttpRequestUtils(self._http_client)

        response: ClientResponse = await http_request_helper.execute_http_request(
            url, question, self._endpoint, options.timeout
        )

        result: QueryResults = await self._format_qna_result(response, options)

        return result

    async def _emit_trace_info(
        self, context: TurnContext, result: List[QueryResult], options: QnAMakerOptions
    ):
        trace_info = QnAMakerTraceInfo(
            message=context.activity,
            query_results=result,
            knowledge_base_id=self._endpoint.knowledge_base_id,
            score_threshold=options.score_threshold,
            top=options.top,
            strict_filters=options.strict_filters,
            context=options.context,
            qna_id=options.qna_id,
            is_test=options.is_test,
            ranker_type=options.ranker_type,
        )

        trace_activity = Activity(
            label=QNAMAKER_TRACE_LABEL,
            name=QNAMAKER_TRACE_NAME,
            type="trace",
            value=trace_info,
            value_type=QNAMAKER_TRACE_TYPE,
        )

        await context.send_activity(trace_activity)

    async def _format_qna_result(
        self, result, options: QnAMakerOptions
    ) -> QueryResults:
        json_res = result
        if isinstance(result, ClientResponse):
            json_res = await result.json()

        answers_within_threshold = [
            {**answer, "score": answer["score"] / 100}
            for answer in json_res["answers"]
            if answer["score"] / 100 > options.score_threshold
        ]
        sorted_answers = sorted(
            answers_within_threshold, key=lambda ans: ans["score"], reverse=True
        )

        answers_as_query_results = list(
            map(lambda answer: QueryResult(**answer), sorted_answers)
        )

        active_learning_enabled = (
            json_res["activeLearningEnabled"]
            if "activeLearningEnabled" in json_res
            else True
        )

        query_answer_response = QueryResults(
            answers_as_query_results, active_learning_enabled
        )

        return query_answer_response
