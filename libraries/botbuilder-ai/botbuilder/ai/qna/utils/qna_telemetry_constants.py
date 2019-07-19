# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from enum import Enum


class QnATelemetryConstants(str, Enum):
    """
    Default QnA event and property names logged using IBotTelemetryClient.
    """

    qna_message_event = "QnaMessage"
    """Event name"""
    knowledge_base_id_property = "knowledgeBaseId"
    answer_property = "answer"
    article_found_property = "articleFound"
    channel_id_property = "channelId"
    conversation_id_property = "conversationId"
    question_property = "question"
    matched_question_property = "matchedQuestion"
    question_id_property = "questionId"
    score_metric = "score"
    username_property = "username"
