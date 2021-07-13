# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from abc import ABC, abstractmethod
from typing import List, Callable, Awaitable
from botbuilder.schema import (
    Activity,
    ConversationReference,
    ConversationParameters,
    ResourceResponse,
)
from botframework.connector.auth import AppCredentials, ClaimsIdentity

from . import conversation_reference_extension
from .bot_assert import BotAssert
from .turn_context import TurnContext
from .middleware_set import MiddlewareSet


class BotAdapter(ABC):
    BOT_IDENTITY_KEY = "BotIdentity"
    BOT_OAUTH_SCOPE_KEY = "botbuilder.core.BotAdapter.OAuthScope"
    BOT_CONNECTOR_CLIENT_KEY = "ConnectorClient"
    BOT_CALLBACK_HANDLER_KEY = "BotCallbackHandler"
    _INVOKE_RESPONSE_KEY = "BotFrameworkAdapter.InvokeResponse"

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

        :param context: The context object for the turn.
        :type context: :class:`TurnContext`
        :param activities: The activities to send.
        :type activities: :class:`typing.List[Activity]`
        :return:
        """
        raise NotImplementedError()

    @abstractmethod
    async def update_activity(self, context: TurnContext, activity: Activity):
        """
        Replaces an existing activity.

        :param context: The context object for the turn.
        :type context: :class:`TurnContext`
        :param activity: New replacement activity.
        :type activity: :class:`botbuilder.schema.Activity`
        :return:
        """
        raise NotImplementedError()

    @abstractmethod
    async def delete_activity(
        self, context: TurnContext, reference: ConversationReference
    ):
        """
        Deletes an existing activity.

        :param context: The context object for the turn.
        :type context: :class:`TurnContext`
        :param reference: Conversation reference for the activity to delete.
        :type reference: :class:`botbuilder.schema.ConversationReference`
        :return:
        """
        raise NotImplementedError()

    def use(self, middleware):
        """
        Registers a middleware handler with the adapter.

        :param middleware: The middleware to register.
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
        audience: str = None,  # pylint: disable=unused-argument
    ):
        """
        Sends a proactive message to a conversation. Call this method to proactively send a message to a conversation.
        Most channels require a user to initiate a conversation with a bot before the bot can send activities
        to the user.

        :param bot_id: The application ID of the bot. This parameter is ignored in
        single tenant the Adapters (Console, Test, etc) but is critical to the BotFrameworkAdapter
        which is multi-tenant aware.
        :param reference: A reference to the conversation to continue.
        :type reference: :class:`botbuilder.schema.ConversationReference`
        :param callback: The method to call for the resulting bot turn.
        :type callback: :class:`typing.Callable`
        :param claims_identity: A :class:`botframework.connector.auth.ClaimsIdentity` for the conversation.
        :type claims_identity: :class:`botframework.connector.auth.ClaimsIdentity`
        :param audience:A value signifying the recipient of the proactive message.
        :type audience: str
        """
        context = TurnContext(
            self, conversation_reference_extension.get_continuation_activity(reference)
        )
        return await self.run_pipeline(context, callback)

    async def create_conversation(
        self,
        reference: ConversationReference,
        logic: Callable[[TurnContext], Awaitable] = None,
        conversation_parameters: ConversationParameters = None,
        channel_id: str = None,
        service_url: str = None,
        credentials: AppCredentials = None,
    ):
        """
        Starts a new conversation with a user. Used to direct message to a member of a group.

        :param reference: The conversation reference that contains the tenant
        :type reference: :class:`botbuilder.schema.ConversationReference`
        :param logic: The logic to use for the creation of the conversation
        :type logic: :class:`typing.Callable`
        :param conversation_parameters: The information to use to create the conversation
        :type conversation_parameters:
        :param channel_id: The ID for the channel.
        :type channel_id: :class:`typing.str`
        :param service_url: The channel's service URL endpoint.
        :type service_url: :class:`typing.str`
        :param credentials: The application credentials for the bot.
        :type credentials: :class:`botframework.connector.auth.AppCredentials`

        :raises: It raises a generic exception error.

        :return: A task representing the work queued to execute.

        .. remarks::
            To start a conversation, your bot must know its account information and the user's
            account information on that channel.
            Most channels only support initiating a direct message (non-group) conversation.
            The adapter attempts to create a new conversation on the channel, and
            then sends a conversation update activity through its middleware pipeline
            to the the callback method.
            If the conversation is established with the specified users, the ID of the activity
            will contain the ID of the new conversation.
        """
        raise Exception("Not Implemented")

    async def run_pipeline(
        self, context: TurnContext, callback: Callable[[TurnContext], Awaitable] = None
    ):
        """
        Called by the parent class to run the adapters middleware set and calls the passed in `callback()` handler at
        the end of the chain.

        :param context: The context object for the turn.
        :type context: :class:`TurnContext`
        :param callback: A callback method to run at the end of the pipeline.
        :type callback: :class:`typing.Callable[[TurnContext], Awaitable]`
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
