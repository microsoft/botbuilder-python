# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from abc import ABC, abstractmethod
from typing import List, Callable, Awaitable
from botbuilder.schema import Activity, ConversationReference, ResourceResponse
from botframework.connector.auth import ClaimsIdentity

from . import conversation_reference_extension
from .bot_assert import BotAssert
from .turn_context import TurnContext
from .middleware_set import MiddlewareSet


class BotAdapter(ABC):
    def __init__(
        self, on_turn_error: Callable[[TurnContext, Exception], Awaitable] = None
    ):
        self._middleware = MiddlewareSet()
        self.on_turn_error = on_turn_error

    @abstractmethod
    async def send_activities(
        self, context: TurnContext, activities: List[Activity]
    ) -> List[ResourceResponse]:
        """
        Sends a set of activities to the user. An array of responses from the server will be returned.
        :param context:
        :param activities:
        :return:
        """
        raise NotImplementedError()

    @abstractmethod
    async def update_activity(self, context: TurnContext, activity: Activity):
        """
        Replaces an existing activity.
        :param context:
        :param activity:
        :return:
        """
        raise NotImplementedError()

    @abstractmethod
    async def delete_activity(
        self, context: TurnContext, reference: ConversationReference
    ):
        """
        Deletes an existing activity.
        :param context:
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
        return self

    async def continue_conversation(
        self,
        reference: ConversationReference,
        callback: Callable,
        bot_id: str = None,  # pylint: disable=unused-argument
        claims_identity: ClaimsIdentity = None,  # pylint: disable=unused-argument
    ):
        """
        Sends a proactive message to a conversation. Call this method to proactively send a message to a conversation.
        Most _channels require a user to initiate a conversation with a bot before the bot can send activities
        to the user.
        :param bot_id: The application ID of the bot. This parameter is ignored in
        single tenant the Adpters (Console, Test, etc) but is critical to the BotFrameworkAdapter
        which is multi-tenant aware. </param>
        :param reference: A reference to the conversation to continue.</param>
        :param callback: The method to call for the resulting bot turn.</param>
        :param claims_identity:
        """
        context = TurnContext(
            self, conversation_reference_extension.get_continuation_activity(reference)
        )
        return await self.run_pipeline(context, callback)

    async def run_pipeline(
        self, context: TurnContext, callback: Callable[[TurnContext], Awaitable] = None
    ):
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
                return await self._middleware.receive_activity_with_status(
                    context, callback
                )
            except Exception as error:
                if self.on_turn_error is not None:
                    await self.on_turn_error(context, error)
                else:
                    raise error
        else:
            # callback to caller on proactive case
            if callback is not None:
                await callback(context)
