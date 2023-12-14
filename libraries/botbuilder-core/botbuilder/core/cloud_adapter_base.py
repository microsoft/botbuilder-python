# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from abc import ABC
from asyncio import sleep
from copy import Error
from http import HTTPStatus
from typing import Awaitable, Callable, List, Union
from uuid import uuid4

from botbuilder.core.invoke_response import InvokeResponse

from botbuilder.schema import (
    Activity,
    ActivityEventNames,
    ActivityTypes,
    ConversationAccount,
    ConversationReference,
    ConversationResourceResponse,
    ConversationParameters,
    DeliveryModes,
    ExpectedReplies,
    ResourceResponse,
)
from botframework.connector import Channels, ConnectorClient
from botframework.connector.auth import (
    AuthenticationConstants,
    BotFrameworkAuthentication,
    ClaimsIdentity,
)
from botframework.connector.auth.authenticate_request_result import (
    AuthenticateRequestResult,
)
from botframework.connector.auth.connector_factory import ConnectorFactory
from botframework.connector.auth.user_token_client import UserTokenClient
from .bot_adapter import BotAdapter
from .conversation_reference_extension import get_continuation_activity
from .turn_context import TurnContext


class CloudAdapterBase(BotAdapter, ABC):
    CONNECTOR_FACTORY_KEY = "ConnectorFactory"
    USER_TOKEN_CLIENT_KEY = "UserTokenClient"

    def __init__(
        self, bot_framework_authentication: BotFrameworkAuthentication
    ) -> None:
        super().__init__()

        if not bot_framework_authentication:
            raise TypeError("Expected BotFrameworkAuthentication but got None instead")

        self.bot_framework_authentication = bot_framework_authentication

    async def send_activities(
        self, context: TurnContext, activities: List[Activity]
    ) -> List[ResourceResponse]:
        if not context:
            raise TypeError("Expected TurnContext but got None instead")

        if activities is None:
            raise TypeError("Expected Activities list but got None instead")

        if len(activities) == 0:
            raise TypeError("Expecting one or more activities, but the list was empty.")

        responses = []

        for activity in activities:
            activity.id = None

            response = ResourceResponse()

            if activity.type == "delay":
                delay_time = int((activity.value or 1000) / 1000)
                await sleep(delay_time)
            elif activity.type == ActivityTypes.invoke_response:
                context.turn_state[self._INVOKE_RESPONSE_KEY] = activity
            elif (
                activity.type == ActivityTypes.trace
                and activity.channel_id != Channels.emulator
            ):
                # no-op
                pass
            else:
                connector_client: ConnectorClient = context.turn_state.get(
                    self.BOT_CONNECTOR_CLIENT_KEY
                )
                if not connector_client:
                    raise Error("Unable to extract ConnectorClient from turn context.")

                if activity.reply_to_id:
                    response = await connector_client.conversations.reply_to_activity(
                        activity.conversation.id, activity.reply_to_id, activity
                    )
                else:
                    response = (
                        await connector_client.conversations.send_to_conversation(
                            activity.conversation.id, activity
                        )
                    )

            response = response or ResourceResponse(id=activity.id or "")

            responses.append(response)

        return responses

    async def update_activity(self, context: TurnContext, activity: Activity):
        if not context:
            raise TypeError("Expected TurnContext but got None instead")

        if activity is None:
            raise TypeError("Expected Activity but got None instead")

        connector_client: ConnectorClient = context.turn_state.get(
            self.BOT_CONNECTOR_CLIENT_KEY
        )
        if not connector_client:
            raise Error("Unable to extract ConnectorClient from turn context.")

        response = await connector_client.conversations.update_activity(
            activity.conversation.id, activity.reply_to_id, activity
        )

        response_id = response.id if response and response.id else None

        return ResourceResponse(id=response_id) if response_id else None

    async def delete_activity(
        self, context: TurnContext, reference: ConversationReference
    ):
        if not context:
            raise TypeError("Expected TurnContext but got None instead")

        if not reference:
            raise TypeError("Expected ConversationReference but got None instead")

        connector_client: ConnectorClient = context.turn_state.get(
            self.BOT_CONNECTOR_CLIENT_KEY
        )
        if not connector_client:
            raise Error("Unable to extract ConnectorClient from turn context.")

        await connector_client.conversations.delete_activity(
            reference.conversation.id, reference.activity_id
        )

    async def continue_conversation(  # pylint: disable=arguments-differ
        self,
        reference: ConversationReference,
        callback: Callable,
        bot_app_id: str,
    ):
        """
        Sends a proactive message to a conversation.
        Call this method to proactively send a message to a conversation.
        Most channels require a user to initiate a conversation with a bot before the bot can send activities
        to the user.

        :param reference: A reference to the conversation to continue.
        :type reference: :class:`botbuilder.schema.ConversationReference`
        :param callback: The method to call for the resulting bot turn.
        :type callback: :class:`typing.Callable`
        :param bot_app_id: The application Id of the bot. This is the appId returned by the Azure portal registration,
        and is generally found in the `MicrosoftAppId` parameter in `config.py`.
        :type bot_app_id: :class:`typing.str`
        """
        return await self.process_proactive(
            self.create_claims_identity(bot_app_id),
            get_continuation_activity(reference),
            None,
            callback,
        )

    async def continue_conversation_with_claims(
        self,
        claims_identity: ClaimsIdentity,
        reference: ConversationReference,
        audience: str,
        logic: Callable[[TurnContext], Awaitable],
    ):
        return await self.process_proactive(
            claims_identity, get_continuation_activity(reference), audience, logic
        )

    async def create_conversation(  # pylint: disable=arguments-differ
        self,
        bot_app_id: str,
        callback: Callable[[TurnContext], Awaitable] = None,
        conversation_parameters: ConversationParameters = None,
        channel_id: str = None,
        service_url: str = None,
        audience: str = None,
    ):
        if not service_url:
            raise TypeError(
                "CloudAdapter.create_conversation(): service_url is required."
            )
        if not conversation_parameters:
            raise TypeError(
                "CloudAdapter.create_conversation(): conversation_parameters is required."
            )
        if not callback:
            raise TypeError("CloudAdapter.create_conversation(): callback is required.")

        # Create a ClaimsIdentity, to create the connector and for adding to the turn context.
        claims_identity = self.create_claims_identity(bot_app_id)
        claims_identity.claims[AuthenticationConstants.SERVICE_URL_CLAIM] = service_url

        # create the connectror factory
        connector_factory = self.bot_framework_authentication.create_connector_factory(
            claims_identity
        )

        # Create the connector client to use for outbound requests.
        connector_client = await connector_factory.create(service_url, audience)

        # Make the actual create conversation call using the connector.
        create_conversation_result = (
            await connector_client.conversations.create_conversation(
                conversation_parameters
            )
        )

        # Create the create activity to communicate the results to the application.
        create_activity = self._create_create_activity(
            create_conversation_result, channel_id, service_url, conversation_parameters
        )

        # Create a UserTokenClient instance for the application to use. (For example, in the OAuthPrompt.)
        user_token_client = (
            await self.bot_framework_authentication.create_user_token_client(
                claims_identity
            )
        )

        # Create a turn context and run the pipeline.
        context = self._create_turn_context(
            create_activity,
            claims_identity,
            None,
            connector_client,
            user_token_client,
            callback,
            connector_factory,
        )

        # Run the pipeline
        await self.run_pipeline(context, callback)

    async def process_proactive(
        self,
        claims_identity: ClaimsIdentity,
        continuation_activity: Activity,
        audience: str,
        logic: Callable[[TurnContext], Awaitable],
    ):
        # Create the connector factory and  the inbound request, extracting parameters and then create a
        # connector for outbound requests.
        connector_factory = self.bot_framework_authentication.create_connector_factory(
            claims_identity
        )

        # Create the connector client to use for outbound requests.
        connector_client = await connector_factory.create(
            continuation_activity.service_url, audience
        )

        # Create a UserTokenClient instance for the application to use. (For example, in the OAuthPrompt.)
        user_token_client = (
            await self.bot_framework_authentication.create_user_token_client(
                claims_identity
            )
        )

        # Create a turn context and run the pipeline.
        context = self._create_turn_context(
            continuation_activity,
            claims_identity,
            audience,
            connector_client,
            user_token_client,
            logic,
            connector_factory,
        )

        # Run the pipeline
        await self.run_pipeline(context, logic)

    async def process_activity(
        self,
        auth_header_or_authenticate_request_result: Union[
            str, AuthenticateRequestResult
        ],
        activity: Activity,
        logic: Callable[[TurnContext], Awaitable],
    ):
        """
        Creates a turn context and runs the middleware pipeline for an incoming activity.

        :param auth_header: The HTTP authentication header of the request
        :type auth_header: :class:`typing.Union[typing.str, AuthenticateRequestResult]`
        :param activity: The incoming activity
        :type activity: :class:`Activity`
        :param logic: The logic to execute at the end of the adapter's middleware pipeline.
        :type logic: :class:`typing.Callable`

        :return: A task that represents the work queued to execute.

        .. remarks::
            This class processes an activity received by the bots web server. This includes any messages
            sent from a user and is the method that drives what's often referred to as the
            bots *reactive messaging* flow.
            Call this method to reactively send a message to a conversation.
            If the task completes successfully, then an :class:`InvokeResponse` is returned;
            otherwise. `null` is returned.
        """
        # Authenticate the inbound request, extracting parameters and create a ConnectorFactory for creating a
        # Connector for outbound requests.
        authenticate_request_result = (
            await self.bot_framework_authentication.authenticate_request(
                activity, auth_header_or_authenticate_request_result
            )
            if isinstance(auth_header_or_authenticate_request_result, str)
            else auth_header_or_authenticate_request_result
        )

        # Set the caller_id on the activity
        activity.caller_id = authenticate_request_result.caller_id

        # Create the connector client to use for outbound requests.
        connector_client = (
            await authenticate_request_result.connector_factory.create(
                activity.service_url, authenticate_request_result.audience
            )
            if authenticate_request_result.connector_factory
            else None
        )

        if not connector_client:
            raise Error("Unable to extract ConnectorClient from turn context.")

        # Create a UserTokenClient instance for the application to use.
        # (For example, it would be used in a sign-in prompt.)
        user_token_client = (
            await self.bot_framework_authentication.create_user_token_client(
                authenticate_request_result.claims_identity
            )
        )

        # Create a turn context and run the pipeline.
        context = self._create_turn_context(
            activity,
            authenticate_request_result.claims_identity,
            authenticate_request_result.audience,
            connector_client,
            user_token_client,
            logic,
            authenticate_request_result.connector_factory,
        )

        # Run the pipeline
        await self.run_pipeline(context, logic)

        # If there are any results they will have been left on the TurnContext.
        return self._process_turn_results(context)

    def create_claims_identity(self, bot_app_id: str = "") -> ClaimsIdentity:
        return ClaimsIdentity(
            {
                AuthenticationConstants.AUDIENCE_CLAIM: bot_app_id,
                AuthenticationConstants.APP_ID_CLAIM: bot_app_id,
            },
            True,
        )

    def _create_create_activity(
        self,
        create_conversation_result: ConversationResourceResponse,
        channel_id: str,
        service_url: str,
        conversation_parameters: ConversationParameters,
    ) -> Activity:
        # Create a conversation update activity to represent the result.
        activity = Activity.create_event_activity()
        activity.name = ActivityEventNames.create_conversation
        activity.channel_id = channel_id
        activity.service_url = service_url
        activity.id = create_conversation_result.activity_id or str(uuid4())
        activity.conversation = ConversationAccount(
            id=create_conversation_result.id,
            tenant_id=conversation_parameters.tenant_id,
        )
        activity.channel_data = conversation_parameters.channel_data
        activity.recipient = conversation_parameters.bot

        return activity

    def _create_turn_context(
        self,
        activity: Activity,
        claims_identity: ClaimsIdentity,
        oauth_scope: str,
        connector_client: ConnectorClient,
        user_token_client: UserTokenClient,
        logic: Callable[[TurnContext], Awaitable],
        connector_factory: ConnectorFactory,
    ) -> TurnContext:
        context = TurnContext(self, activity)

        context.turn_state[self.BOT_IDENTITY_KEY] = claims_identity
        context.turn_state[self.BOT_CONNECTOR_CLIENT_KEY] = connector_client
        context.turn_state[self.USER_TOKEN_CLIENT_KEY] = user_token_client

        context.turn_state[self.BOT_CALLBACK_HANDLER_KEY] = logic

        context.turn_state[self.CONNECTOR_FACTORY_KEY] = connector_factory
        context.turn_state[self.BOT_OAUTH_SCOPE_KEY] = oauth_scope

        return context

    def _process_turn_results(self, context: TurnContext) -> InvokeResponse:
        # Handle ExpectedReplies scenarios where all activities have been
        # buffered and sent back at once in an invoke response.
        if context.activity.delivery_mode == DeliveryModes.expect_replies:
            return InvokeResponse(
                status=HTTPStatus.OK,
                body=ExpectedReplies(activities=context.buffered_reply_activities),
            )

        # Handle Invoke scenarios where the bot will return a specific body and return code.
        if context.activity.type == ActivityTypes.invoke:
            activity_invoke_response: Activity = context.turn_state.get(
                self._INVOKE_RESPONSE_KEY
            )
            if not activity_invoke_response:
                return InvokeResponse(status=HTTPStatus.NOT_IMPLEMENTED)

            return activity_invoke_response.value

        # No body to return
        return None
