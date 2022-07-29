# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import math

from typing import List
from ..models import QueryResult

MINIMUM_SCORE_FOR_LOW_SCORE_VARIATION = 20.0
PREVIOUS_LOW_SCORE_VARIATION_MULTIPLIER = 0.7
MAX_LOW_SCORE_VARIATION_MULTIPLIER = 1.0
MAX_SCORE_FOR_LOW_SCORE_VARIATION = 95.0


class ActiveLearningUtils:
    """Active learning helper class"""

    @staticmethod
    def get_low_score_variation(
        qna_search_results: List[QueryResult],
    ) -> List[QueryResult]:
        """
        Returns a list of QnA search results, which have low score variation.

        Parameters:
        -----------

        qna_serach_results: A list of QnA QueryResults returned from the QnA GenerateAnswer API call.
        """

        if not qna_search_results:
            return []

        if len(qna_search_results) == 1:
            return qna_search_results

        filtered_qna_search_result: List[QueryResult] = []
        top_answer_score = qna_search_results[0].score * 100
        prev_score = top_answer_score

        if (
            MINIMUM_SCORE_FOR_LOW_SCORE_VARIATION
            < top_answer_score
            <= MAX_SCORE_FOR_LOW_SCORE_VARIATION
        ):
            filtered_qna_search_result.append(qna_search_results[0])

            for idx in range(1, len(qna_search_results)):
                current_score = qna_search_results[idx].score * 100

                if ActiveLearningUtils._include_for_clustering(
                    prev_score, current_score, PREVIOUS_LOW_SCORE_VARIATION_MULTIPLIER
                ) and ActiveLearningUtils._include_for_clustering(
                    top_answer_score, current_score, MAX_LOW_SCORE_VARIATION_MULTIPLIER
                ):
                    prev_score = current_score
                    filtered_qna_search_result.append(qna_search_results[idx])

        return filtered_qna_search_result

    @staticmethod
    def _include_for_clustering(
        prev_score: float, current_score: float, multiplier: float
    ) -> bool:
        return (prev_score - current_score) < (multiplier * math.sqrt(prev_score))
