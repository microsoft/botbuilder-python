# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from enum import Enum


class LuisTelemetryConstants(str, Enum):
    """
    The IBotTelemetryClient event and property names that logged by default.
    """

    luis_result = "LuisResult"
    """Event name"""
    application_id_property = "applicationId"
    intent_property = "intent"
    intent_score_property = "intentScore"
    intent2_property = "intent2"
    intent_score2_property = "intentScore2"
    entities_property = "entities"
    question_property = "question"
    activity_id_property = "activityId"
    sentiment_label_property = "sentimentLabel"
    sentiment_score_property = "sentimentScore"
    from_id_property = "fromId"
