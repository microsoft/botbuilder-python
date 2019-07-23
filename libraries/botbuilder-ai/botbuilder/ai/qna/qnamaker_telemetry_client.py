# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from abc import ABC, abstractmethod
from typing import Dict
from botbuilder.core import BotTelemetryClient, TurnContext
from .qnamaker_options import QnAMakerOptions


class QnAMakerTelemetryClient(ABC):
    def __init__(
        self, log_personal_information: bool, telemetry_client: BotTelemetryClient
    ):
        self.log_personal_information = (log_personal_information,)
        self.telemetry_client = telemetry_client

    @abstractmethod
    def get_answers(
        self,
        context: TurnContext,
        options: QnAMakerOptions = None,
        telemetry_properties: Dict[str, str] = None,
        telemetry_metrics: Dict[str, float] = None,
    ):
        raise NotImplementedError(
            "QnAMakerTelemetryClient.get_answers(): is not implemented."
        )
