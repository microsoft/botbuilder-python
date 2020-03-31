# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
from typing import List

from botbuilder.dialogs import (
    WaterfallDialog,
    WaterfallStepContext,
    DialogContext,
    DialogTurnResult,
    Dialog,
    ObjectPath,
    DialogTurnStatus,
    DialogReason,
)
from botbuilder.schema import Activity, ActivityTypes

from .qnamaker_dialog_options import QnAMakerDialogOptions
from .. import (
    QnAMakerOptions,
    QnADialogResponseOptions,
    QnAMaker,
    QnAMakerEndpoint,
)
from ..models import QnARequestContext, Metadata, QueryResult, FeedbackRecord
from ..models.ranker_types import RankerTypes
from ..utils import QnACardBuilder


class QnAMakerDialog(WaterfallDialog):
    KEY_QNA_CONTEXT_DATA = "qnaContextData"
    KEY_PREVIOUS_QNA_ID = "prevQnAId"
    KEY_OPTIONS = "options"

    # Dialog Options parameters
    DEFAULT_THRESHOLD = 0.3
    DEFAULT_TOP_N = 3
    DEFAULT_NO_ANSWER = "No QnAMaker answers found."

    # Card parameters
    DEFAULT_CARD_TITLE = "Did you mean:"
    DEFAULT_CARD_NO_MATCH_TEXT = "None of the above."
    DEFAULT_CARD_NO_MATCH_RESPONSE = "Thanks for the feedback."

    # Value Properties
    PROPERTY_CURRENT_QUERY = "currentQuery"
    PROPERTY_QNA_DATA = "qnaData"

    def __init__(
        self,
        knowledgebase_id: str,
        endpoint_key: str,
        hostname: str,
        no_answer: Activity = None,
        threshold: float = DEFAULT_THRESHOLD,
        active_learning_card_title: str = DEFAULT_CARD_TITLE,
        card_no_match_text: str = DEFAULT_CARD_NO_MATCH_TEXT,
        top: int = DEFAULT_TOP_N,
        card_no_match_response: Activity = None,
        strict_filters: [Metadata] = None,
        dialog_id: str = "QnAMakerDialog",
    ):
        super().__init__(dialog_id)

        self.knowledgebase_id = knowledgebase_id
        self.endpoint_key = endpoint_key
        self.hostname = hostname
        self.no_answer = no_answer
        self.threshold = threshold
        self.active_learning_card_title = active_learning_card_title
        self.card_no_match_text = card_no_match_text
        self.top = top
        self.card_no_match_response = card_no_match_response
        self.strict_filters = strict_filters

        self.maximum_score_for_low_score_variation = 0.95

        self.add_step(self.__call_generate_answer)
        self.add_step(self.__call_train)
        self.add_step(self.__check_for_multiturn_prompt)
        self.add_step(self.__display_qna_result)

    async def begin_dialog(
        self, dialog_context: DialogContext, options: object = None
    ) -> DialogTurnResult:
        if not dialog_context:
            raise TypeError("DialogContext is required")

        if (
            dialog_context.context
            and dialog_context.context.activity
            and dialog_context.context.activity.type != ActivityTypes.message
        ):
            return Dialog.end_of_turn

        dialog_options = QnAMakerDialogOptions(
            options=self._get_qnamaker_options(dialog_context),
            response_options=self._get_qna_response_options(dialog_context),
        )

        if options:
            dialog_options = ObjectPath.assign(dialog_options, options)

        ObjectPath.set_path_value(
            dialog_context.active_dialog.state,
            QnAMakerDialog.KEY_OPTIONS,
            dialog_options,
        )

        return await super().begin_dialog(dialog_context, dialog_options)

    def _get_qnamaker_client(self, dialog_context: DialogContext) -> QnAMaker:
        endpoint = QnAMakerEndpoint(
            endpoint_key=self.endpoint_key,
            host=self.hostname,
            knowledge_base_id=self.knowledgebase_id,
        )

        options = self._get_qnamaker_options(dialog_context)

        return QnAMaker(endpoint, options)

    def _get_qnamaker_options(  # pylint: disable=unused-argument
        self, dialog_context: DialogContext
    ) -> QnAMakerOptions:
        return QnAMakerOptions(
            score_threshold=self.threshold,
            strict_filters=self.strict_filters,
            top=self.top,
            context=QnARequestContext(),
            qna_id=0,
            ranker_type=RankerTypes.DEFAULT,
            is_test=False,
        )

    def _get_qna_response_options(  # pylint: disable=unused-argument
        self, dialog_context: DialogContext
    ) -> QnADialogResponseOptions:
        return QnADialogResponseOptions(
            no_answer=self.no_answer,
            active_learning_card_title=self.active_learning_card_title
            or QnAMakerDialog.DEFAULT_CARD_TITLE,
            card_no_match_text=self.card_no_match_text
            or QnAMakerDialog.DEFAULT_CARD_NO_MATCH_TEXT,
            card_no_match_response=self.card_no_match_response,
        )

    async def __call_generate_answer(self, step_context: WaterfallStepContext):
        dialog_options: QnAMakerDialogOptions = ObjectPath.get_path_value(
            step_context.active_dialog.state, QnAMakerDialog.KEY_OPTIONS
        )

        # Resetting context and QnAId
        dialog_options.options.qna_id = 0
        dialog_options.options.context = QnARequestContext()

        # Storing the context info
        step_context.values[
            QnAMakerDialog.PROPERTY_CURRENT_QUERY
        ] = step_context.context.activity.text

        # -Check if previous context is present, if yes then put it with the query
        # -Check for id if query is present in reverse index.
        previous_context_data = ObjectPath.get_path_value(
            step_context.active_dialog.state, QnAMakerDialog.KEY_QNA_CONTEXT_DATA, {}
        )
        previous_qna_id = ObjectPath.get_path_value(
            step_context.active_dialog.state, QnAMakerDialog.KEY_PREVIOUS_QNA_ID, 0
        )

        if previous_qna_id > 0:
            dialog_options.options.context = QnARequestContext(
                previous_qna_id=previous_qna_id
            )

            current_qna_id = previous_context_data.get(
                step_context.context.activity.text
            )
            if current_qna_id:
                dialog_options.options.qna_id = current_qna_id

        # Calling QnAMaker to get response.
        qna_client = self._get_qnamaker_client(step_context)
        response = await qna_client.get_answers_raw(
            step_context.context, dialog_options.options
        )

        is_active_learning_enabled = response.active_learning_enabled
        step_context.values[QnAMakerDialog.PROPERTY_QNA_DATA] = response.answers

        # Resetting previous query.
        previous_qna_id = -1
        ObjectPath.set_path_value(
            step_context.active_dialog.state,
            QnAMakerDialog.KEY_PREVIOUS_QNA_ID,
            previous_qna_id,
        )

        # Check if active learning is enabled and send card
        # maximum_score_for_low_score_variation is the score above which no need to check for feedback.
        if (
            is_active_learning_enabled
            and response.answers
            and response.answers[0].score <= self.maximum_score_for_low_score_variation
        ):
            # Get filtered list of the response that support low score variation criteria.
            response.answers = qna_client.get_low_score_variation(response.answers)
            if len(response.answers) > 1:
                suggested_questions = [qna.questions[0] for qna in response.answers]
                message = QnACardBuilder.get_suggestions_card(
                    suggested_questions,
                    dialog_options.response_options.active_learning_card_title,
                    dialog_options.response_options.card_no_match_text,
                )
                await step_context.context.send_activity(message)

                ObjectPath.set_path_value(
                    step_context.active_dialog.state,
                    QnAMakerDialog.KEY_OPTIONS,
                    dialog_options,
                )

                await qna_client.close()

                return DialogTurnResult(DialogTurnStatus.Waiting)

        # If card is not shown, move to next step with top qna response.
        result = [response.answers[0]] if response.answers else []
        step_context.values[QnAMakerDialog.PROPERTY_QNA_DATA] = result
        ObjectPath.set_path_value(
            step_context.active_dialog.state, QnAMakerDialog.KEY_OPTIONS, dialog_options
        )

        await qna_client.close()

        return await step_context.next(result)

    async def __call_train(self, step_context: WaterfallStepContext):
        dialog_options: QnAMakerDialogOptions = ObjectPath.get_path_value(
            step_context.active_dialog.state, QnAMakerDialog.KEY_OPTIONS
        )
        train_responses: [QueryResult] = step_context.values[
            QnAMakerDialog.PROPERTY_QNA_DATA
        ]
        current_query = step_context.values[QnAMakerDialog.PROPERTY_CURRENT_QUERY]

        reply = step_context.context.activity.text

        if len(train_responses) > 1:
            qna_results = [
                result for result in train_responses if result.questions[0] == reply
            ]

            if qna_results:
                qna_result = qna_results[0]
                step_context.values[QnAMakerDialog.PROPERTY_QNA_DATA] = [qna_result]

                feedback_records = [
                    FeedbackRecord(
                        user_id=step_context.context.activity.id,
                        user_question=current_query,
                        qna_id=qna_result.id,
                    )
                ]

                # Call Active Learning Train API
                qna_client = self._get_qnamaker_client(step_context)
                await qna_client.call_train(feedback_records)
                await qna_client.close()

                return await step_context.next([qna_result])

            if (
                reply.lower()
                == dialog_options.response_options.card_no_match_text.lower()
            ):
                activity = dialog_options.response_options.card_no_match_response
                if not activity:
                    await step_context.context.send_activity(
                        QnAMakerDialog.DEFAULT_CARD_NO_MATCH_RESPONSE
                    )
                else:
                    await step_context.context.send_activity(activity)

                return await step_context.end_dialog()

            return await super().run_step(
                step_context, index=0, reason=DialogReason.BeginCalled, result=None
            )

        return await step_context.next(step_context.result)

    async def __check_for_multiturn_prompt(self, step_context: WaterfallStepContext):
        dialog_options: QnAMakerDialogOptions = ObjectPath.get_path_value(
            step_context.active_dialog.state, QnAMakerDialog.KEY_OPTIONS
        )

        response = step_context.result
        if response and isinstance(response, List):
            answer = response[0]
            if answer.context and answer.context.prompts:
                previous_context_data = ObjectPath.get_path_value(
                    step_context.active_dialog.state,
                    QnAMakerDialog.KEY_QNA_CONTEXT_DATA,
                )
                for prompt in answer.context.prompts:
                    previous_context_data[prompt.display_text] = prompt.qna_id

                ObjectPath.set_path_value(
                    step_context.active_dialog.state,
                    QnAMakerDialog.KEY_QNA_CONTEXT_DATA,
                    previous_context_data,
                )
                ObjectPath.set_path_value(
                    step_context.active_dialog.state,
                    QnAMakerDialog.KEY_PREVIOUS_QNA_ID,
                    answer.id,
                )
                ObjectPath.set_path_value(
                    step_context.active_dialog.state,
                    QnAMakerDialog.KEY_OPTIONS,
                    dialog_options,
                )

                # Get multi-turn prompts card activity.
                message = QnACardBuilder.get_qna_prompts_card(
                    answer, dialog_options.response_options.card_no_match_text
                )
                await step_context.context.send_activity(message)

                return DialogTurnResult(DialogTurnStatus.Waiting)

        return await step_context.next(step_context.result)

    async def __display_qna_result(self, step_context: WaterfallStepContext):
        dialog_options: QnAMakerDialogOptions = ObjectPath.get_path_value(
            step_context.active_dialog.state, QnAMakerDialog.KEY_OPTIONS
        )

        reply = step_context.context.activity.text
        if reply.lower() == dialog_options.response_options.card_no_match_text.lower():
            activity = dialog_options.response_options.card_no_match_response
            if not activity:
                await step_context.context.send_activity(
                    QnAMakerDialog.DEFAULT_CARD_NO_MATCH_RESPONSE
                )
            else:
                await step_context.context.send_activity(activity)

            return await step_context.end_dialog()

        # If previous QnAId is present, replace the dialog
        previous_qna_id = ObjectPath.get_path_value(
            step_context.active_dialog.state, QnAMakerDialog.KEY_PREVIOUS_QNA_ID
        )
        if previous_qna_id > 0:
            return await super().run_step(
                step_context, index=0, reason=DialogReason.BeginCalled, result=None
            )

        # If response is present then show that response, else default answer.
        response = step_context.result
        if response and isinstance(response, List):
            await step_context.context.send_activity(response[0].answer)
        else:
            activity = dialog_options.response_options.no_answer
            if not activity:
                await step_context.context.send_activity(
                    QnAMakerDialog.DEFAULT_NO_ANSWER
                )
            else:
                await step_context.context.send_activity(activity)

        return await step_context.end_dialog()
