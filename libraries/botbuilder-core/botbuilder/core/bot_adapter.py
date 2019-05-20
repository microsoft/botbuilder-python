# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from abc import ABC, abstractmethod
from typing import List, Callable, Awaitable
from botbuilder.schema import Activity, ConversationReference

from .bot_assert import BotAssert
from .turn_context import TurnContext
from .middleware_set import MiddlewareSet


class BotAdapter(ABC):
    def __init__(self, on_turn_error: Callable[[TurnContext, Exception], Awaitable] = None):
        self._middleware = MiddlewareSet()
        self.on_turn_error = on_turn_error

    @abstractmethod
    async def send_activities(self, context: TurnContext, activities: List[Activity]):
        """
        Sends a set of activities to the user. An array of responses from the server will be returned.
        :param activities:
        :return:
        """
        raise NotImplementedError()

    @abstractmethod
    async def update_activity(self, context: TurnContext, activity: Activity):
        """
        Replaces an existing activity.
        :param activity:
        :return:
        """
        raise NotImplementedError()

    @abstractmethod
    async def delete_activity(self, context: TurnContext, reference: ConversationReference):
        """
        Deletes an existing activity.
        :param reference:
        :return:
        """
        raise NotImplementedError()

    def use(self, middleware):
        """
        Registers a middleware handler with the adapter.
        :param middleware:
        :return:
        """
        self._middleware.use(middleware)

    async def run_middleware(self, context: TurnContext, callback: Callable[[TurnContext], Awaitable]= None):
        """
        Called by the parent class to run the adapters middleware set and calls the passed in `callback()` handler at
        the end of the chain.
        :param context:
        :param callback:
        :return:
        """
        BotAssert.context_not_none(context)

        if context.activity is not None:
            try:
                return await self._middleware.receive_activity_with_status(context, callback)
            except Exception as error:
                if self.on_turn_error is not None:
                    await self.on_turn_error(context, error)
                else:
                    raise error
        else:
            # callback to caller on proactive case
            if callback is not None:
                await callback(context)
