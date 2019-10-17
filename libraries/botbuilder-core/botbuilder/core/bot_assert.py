# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import List

from botbuilder.schema import Activity, ConversationReference
from .middleware_set import Middleware
from .turn_context import TurnContext


class BotAssert:
    @staticmethod
    def activity_not_none(activity: Activity) -> None:
        """
        Checks that an activity object is not None
        :param activity: The activity object
        """
        if activity is None:
            raise TypeError(activity.__class__.__name__)

    @staticmethod
    def context_not_none(turn_context: TurnContext) -> None:
        """
        Checks that a context object is not None
        :param turn_context: The context object
        """
        if turn_context is None:
            raise TypeError(turn_context.__class__.__name__)

    @staticmethod
    def conversation_reference_not_none(reference: ConversationReference) -> None:
        """
        Checks that a conversation reference object is not None
        :param reference: The conversation reference object
        """
        if reference is None:
            raise TypeError(reference.__class__.__name__)

    @staticmethod
    def activity_list_not_none(activities: List[Activity]) -> None:
        """
        Checks that an activity list is not None
        :param activities: The activity list
        """
        if activities is None:
            raise TypeError(activities.__class__.__name__)

    @staticmethod
    def middleware_not_none(middleware: Middleware) -> None:
        """
        Checks that a middleware object is not None
        :param middleware: The middleware object
        """
        if middleware is None:
            raise TypeError(middleware.__class__.__name__)

    @staticmethod
    def middleware_list_not_none(middleware: List[Middleware]) -> None:
        """
        Checks that a middeware list is not None
        :param activities: The middleware list
        """
        if middleware is None:
            raise TypeError(middleware.__class__.__name__)
