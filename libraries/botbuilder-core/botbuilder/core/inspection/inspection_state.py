# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import BotState, Storage, TurnContext


class InspectionState(BotState):
    def __init__(self, storage: Storage):
        super().__init__(storage, self.__class__.__name__)

    def get_storage_key(
        self, turn_context: TurnContext
    ) -> str:  # pylint: disable=unused-argument
        return self.__class__.__name__
