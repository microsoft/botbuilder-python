# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

# pylint: disable=too-many-lines

import asyncio
import base64
import json
import os
import uuid
from http import HTTPStatus
from typing import List, Callable, Awaitable, Union, Dict
from msrest.serialization import Model

from botframework.connector import Channels, EmulatorApiClient
from botframework.connector.aio import ConnectorClient
from botframework.connector.auth import (
    AuthenticationConfiguration,
    AuthenticationConstants,
    ChannelValidation,
    ChannelProvider,
    ClaimsIdentity,
    GovernmentChannelValidation,
    GovernmentConstants,
    MicrosoftAppCredentials,
    JwtTokenValidation,
    CredentialProvider,
    SimpleCredentialProvider,
    SkillValidation,
    AppCredentials,
    SimpleChannelProvider,
    MicrosoftGovernmentAppCredentials,
)
from botframework.connector.token_api import TokenApiClient
from botframework.connector.token_api.models import (
    TokenStatus,
    TokenExchangeRequest,
    SignInUrlResponse,
    TokenResponse as ConnectorTokenResponse,
)
from botbuilder.schema import (
    Activity,
    ActivityEventNames,
    ActivityTypes,
    ChannelAccount,
    ConversationAccount,
    ConversationParameters,
    ConversationReference,
    ExpectedReplies,
    InvokeResponse,
    TokenResponse,
    ResourceResponse,
    DeliveryModes,
    CallerIdConstants,
)

from . import __version__
from .bot_adapter import BotAdapter
from .oauth import (
    ConnectorClientBuilder,
    ExtendedUserTokenProvider,
)
from .turn_context import TurnContext
from .conversation_reference_extension import get_continuation_activity

USER_AGENT = f"Microsoft-BotFramework/3.1 (BotBuilder Python/{__version__})"
OAUTH_ENDPOINT = "https://api.botframework.com"
US_GOV_OAUTH_ENDPOINT = "https://api.botframework.azure.us"


class TokenExchangeState(Model):
    """TokenExchangeState

    :param connection_name: The connection name that was used.
    :type connection_name: str
    :param conversation: Gets or sets a reference to the conversation.
    :type conversation: ~botframework.connector.models.ConversationReference
    :param relates_to: Gets or sets a reference to a related parent conversation for this token exchange.
    :type relates_to: ~botframework.connector.models.ConversationReference
    :param bot_ur: The URL of the bot messaging endpoint.
    :type bot_ur: str
    :param ms_app_id: The bot's registered application ID.
    :type ms_app_id: str
    """

    _attribute_map = {
        "connection_name": {"key": "connectionName", "type": "str"},
        "conversation": {"key": "conversation", "type": "ConversationReference"},
        "relates_to": {"key": "relatesTo", "type": "ConversationReference"},
        "bot_url": {"key": "connectionName", "type": "str"},
        "ms_app_id": {"key": "msAppId", "type": "str"},
    }

    def __init__(
        self,
        *,
        connection_name: str = None,
        conversation=None,
        relates_to=None,
        bot_url: str = None,
        ms_app_id: str = None,
        **kwargs,
    ) -> None:
        super(TokenExchangeState, self).__init__(**kwargs)
        self.connection_name = connection_name
        self.conversation = conversation
        self.relates_to = relates_to
        self.bot_url = bot_url
        self.ms_app_id = ms_app_id


class BotFrameworkAdapterSettings:
    def __init__(
        self,
        app_id: str,
        app_password: str = None,
        channel_auth_tenant: str = None,
        oauth_endpoint: str = None,
        open_id_metadata: str = None,
        channel_provider: ChannelProvider = None,
        auth_configuration: AuthenticationConfiguration = None,
        app_credentials: AppCredentials = None,
        credential_provider: CredentialProvider = None,
    ):
        """
        Contains the settings used to initialize a :class:`BotFrameworkAdapter` instance.

        :param app_id: The bot application ID.
        :type app_id: str
        :param app_password: The bot application password.
        the value os the `MicrosoftAppPassword` parameter in the `config.py` file.
        :type app_password: str
        :param channel_auth_tenant: The channel tenant to use in conversation
        :type channel_auth_tenant: str
        :param oauth_endpoint:
        :type oauth_endpoint: str
        :param open_id_metadata:
        :type open_id_metadata: str
        :param channel_provider: The channel provider
        :type channel_provider: :class:`botframework.connector.auth.ChannelProvider`.  Defaults to SimpleChannelProvider
        if one isn't specified.
        :param auth_configuration:
        :type auth_configuration: :class:`botframework.connector.auth.AuthenticationConfiguration`
        :param credential_provider: Defaults to SimpleCredentialProvider if one isn't specified.
        :param app_credentials: Allows for a custom AppCredentials.  Used, for example, for CertificateAppCredentials.
        """

        self.app_id = app_id
        self.app_password = app_password
        self.app_credentials = app_credentials
        self.channel_auth_tenant = channel_auth_tenant
        self.oauth_endpoint = oauth_endpoint
        self.channel_provider = (
            channel_provider if channel_provider else SimpleChannelProvider()
        )
        self.credential_provider = (
            credential_provider
            if credential_provider
            else SimpleCredentialProvider(self.app_id, self.app_password)
        )
        self.auth_configuration = auth_configuration or AuthenticationConfiguration()

        # If no open_id_metadata values were passed in the settings, check the
        # process' Environment Variable.
        self.open_id_metadata = (
            open_id_metadata
            if open_id_metadata
            else os.environ.get(AuthenticationConstants.BOT_OPEN_ID_METADATA_KEY)
        )


class BotFrameworkAdapter(
    BotAdapter, ExtendedUserTokenProvider, ConnectorClientBuilder
):
    """
    Defines an adapter to connect a bot to a service endpoint.

    .. remarks::
        The bot adapter encapsulates authentication processes and sends activities to and
        receives activities from the Bot Connector Service. When your bot receives an activity,
        the adapter creates a context object, passes it to your bot's application logic, and
        sends responses back to the user's channel.
        The adapter processes and directs incoming activities in through the bot middleware
        pipeline to your bot’s logic and then back out again.
        As each activity flows in and out of the bot, each piece of middleware can inspect or act
        upon the activity, both before and after the bot logic runs.
    """

    def __init__(self, settings: BotFrameworkAdapterSettings):
        """
        Initializes a new instance of the :class:`BotFrameworkAdapter` class.

        :param settings: The settings to initialize the adapter
        :type settings: :class:`BotFrameworkAdapterSettings`
        """
        super(BotFrameworkAdapter, self).__init__()
        self.settings = settings or BotFrameworkAdapterSettings("", "")

        self._credentials = self.settings.app_credentials
        self._credential_provider = SimpleCredentialProvider(
            self.settings.app_id, self.settings.app_password
        )

        self._channel_provider = self.settings.channel_provider

        self._is_emulating_oauth_cards = False

        if self.settings.open_id_metadata:
            ChannelValidation.open_id_metadata_endpoint = self.settings.open_id_metadata
            GovernmentChannelValidation.OPEN_ID_METADATA_ENDPOINT = (
                self.settings.open_id_metadata
            )

        # There is a significant boost in throughput if we reuse a ConnectorClient
        self._connector_client_cache: Dict[str, ConnectorClient] = {}

        # Cache for appCredentials to speed up token acquisition (a token is not requested unless is expired)
        self._app_credential_map: Dict[str, AppCredentials] = {}

    async def continue_conversation(
        self,
        reference: ConversationReference,
        callback: Callable,
        bot_id: str = None,
        claims_identity: ClaimsIdentity = None,
        audience: str = None,
    ):
        """
        Continues a conversation with a user.

        :param reference: A reference to the conversation to continue
        :type reference: :class:`botbuilder.schema.ConversationReference
        :param callback: The method to call for the resulting bot turn
        :type callback: :class:`typing.Callable`
        :param bot_id: The application Id of the bot. This is the appId returned by the Azure portal registration,
        and is generally found in the `MicrosoftAppId` parameter in `config.py`.
        :type bot_id: :class:`typing.str`
        :param claims_identity: The bot claims identity
        :type claims_identity: :class:`botframework.connector.auth.ClaimsIdentity`
        :param audience:
        :type audience: :class:`typing.str`

        :raises: It raises an argument null exception.

        :return: A task that represents the work queued to execute.

        .. remarks::
            This is often referred to as the bots *proactive messaging* flow as it lets the bot proactively
            send messages to a conversation or user that are already in a communication.
            Scenarios such as sending notifications or coupons to a user are enabled by this function.
        """

        if not reference:
            raise TypeError(
                "Expected reference: ConversationReference but got None instead"
            )
        if not callback:
            raise TypeError("Expected callback: Callable but got None instead")

        # This has to have either a bot_id, in which case a ClaimsIdentity will be created, or
        # a ClaimsIdentity.  In either case, if an audience isn't supplied one will be created.
        if not (bot_id or claims_identity):
            raise TypeError("Expected bot_id or claims_identity")

        if bot_id and not claims_identity:
            claims_identity = ClaimsIdentity(
                claims={
                    AuthenticationConstants.AUDIENCE_CLAIM: bot_id,
                    AuthenticationConstants.APP_ID_CLAIM: bot_id,
                },
                is_authenticated=True,
            )

        if not audience:
            audience = self.__get_botframework_oauth_scope()

        context = TurnContext(self, get_continuation_activity(reference))
        context.turn_state[BotAdapter.BOT_IDENTITY_KEY] = claims_identity
        context.turn_state[BotAdapter.BOT_CALLBACK_HANDLER_KEY] = callback
        context.turn_state[BotAdapter.BOT_OAUTH_SCOPE_KEY] = audience

        client = await self.create_connector_client(
            reference.service_url, claims_identity, audience
        )
        context.turn_state[BotAdapter.BOT_CONNECTOR_CLIENT_KEY] = client

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

        try:
            if not service_url:
                service_url = reference.service_url
                if not service_url:
                    raise TypeError(
                        "BotFrameworkAdapter.create_conversation(): service_url or reference.service_url is required."
                    )

            if not channel_id:
                channel_id = reference.channel_id
                if not channel_id:
                    raise TypeError(
                        "BotFrameworkAdapter.create_conversation(): channel_id or reference.channel_id is required."
                    )

            parameters = (
                conversation_parameters
                if conversation_parameters
                else ConversationParameters(
                    bot=reference.bot, members=[reference.user], is_group=False
                )
            )

            # Mix in the tenant ID if specified. This is required for MS Teams.
            if (
                reference
                and reference.conversation
                and reference.conversation.tenant_id
            ):
                # Putting tenant_id in channel_data is a temporary while we wait for the Teams API to be updated
                if parameters.channel_data is None:
                    parameters.channel_data = {}
                parameters.channel_data["tenant"] = {
                    "tenantId": reference.conversation.tenant_id
                }

                # Permanent solution is to put tenant_id in parameters.tenant_id
                parameters.tenant_id = reference.conversation.tenant_id

            # This is different from C# where credentials are required in the method call.
            # Doing this for compatibility.
            app_credentials = (
                credentials
                if credentials
                else await self.__get_app_credentials(
                    self.settings.app_id, self.__get_botframework_oauth_scope()
                )
            )

            # Create conversation
            client = self._get_or_create_connector_client(service_url, app_credentials)

            resource_response = await client.conversations.create_conversation(
                parameters
            )

            event_activity = Activity(
                type=ActivityTypes.event,
                name=ActivityEventNames.create_conversation,
                channel_id=channel_id,
                service_url=service_url,
                id=(
                    resource_response.activity_id
                    if resource_response.activity_id
                    else str(uuid.uuid4())
                ),
                conversation=ConversationAccount(
                    id=resource_response.id,
                    tenant_id=parameters.tenant_id,
                ),
                channel_data=parameters.channel_data,
                recipient=parameters.bot,
            )

            context = self._create_context(event_activity)
            context.turn_state[BotAdapter.BOT_CONNECTOR_CLIENT_KEY] = client

            claims_identity = ClaimsIdentity(
                claims={
                    AuthenticationConstants.AUDIENCE_CLAIM: app_credentials.microsoft_app_id,
                    AuthenticationConstants.APP_ID_CLAIM: app_credentials.microsoft_app_id,
                    AuthenticationConstants.SERVICE_URL_CLAIM: service_url,
                },
                is_authenticated=True,
            )
            context.turn_state[BotAdapter.BOT_IDENTITY_KEY] = claims_identity

            return await self.run_pipeline(context, logic)

        except Exception as error:
            raise error

    async def process_activity(self, req, auth_header: str, logic: Callable):
        """
        Creates a turn context and runs the middleware pipeline for an incoming activity.

        :param req: The incoming activity
        :type req: :class:`typing.str`
        :param auth_header: The HTTP authentication header of the request
        :type auth_header: :class:`typing.str`
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
        activity = await self.parse_request(req)
        auth_header = auth_header or ""
        identity = await self._authenticate_request(activity, auth_header)
        return await self.process_activity_with_identity(activity, identity, logic)

    async def process_activity_with_identity(
        self, activity: Activity, identity: ClaimsIdentity, logic: Callable
    ):
        context = self._create_context(activity)

        activity.caller_id = await self.__generate_callerid(identity)
        context.turn_state[BotAdapter.BOT_IDENTITY_KEY] = identity
        context.turn_state[BotAdapter.BOT_CALLBACK_HANDLER_KEY] = logic

        # The OAuthScope is also stored on the TurnState to get the correct AppCredentials if fetching
        # a token is required.
        scope = (
            JwtTokenValidation.get_app_id_from_claims(identity.claims)
            if SkillValidation.is_skill_claim(identity.claims)
            else self.__get_botframework_oauth_scope()
        )
        context.turn_state[BotAdapter.BOT_OAUTH_SCOPE_KEY] = scope

        client = await self.create_connector_client(
            activity.service_url, identity, scope
        )
        context.turn_state[BotAdapter.BOT_CONNECTOR_CLIENT_KEY] = client

        # Fix to assign tenant_id from channelData to Conversation.tenant_id.
        # MS Teams currently sends the tenant ID in channelData and the correct behavior is to expose
        # this value in Activity.Conversation.tenant_id.
        # This code copies the tenant ID from channelData to Activity.Conversation.tenant_id.
        # Once MS Teams sends the tenant_id in the Conversation property, this code can be removed.
        if (
            Channels.ms_teams == context.activity.channel_id
            and context.activity.conversation is not None
            and not context.activity.conversation.tenant_id
            and context.activity.channel_data
        ):
            teams_channel_data = context.activity.channel_data
            if teams_channel_data.get("tenant", {}).get("id", None):
                context.activity.conversation.tenant_id = str(
                    teams_channel_data["tenant"]["id"]
                )

        await self.run_pipeline(context, logic)

        # Handle ExpectedReplies scenarios where the all the activities have been buffered and sent back at once
        # in an invoke response.
        # Return the buffered activities in the response.  In this case, the invoker
        # should deserialize accordingly:
        #    activities = ExpectedReplies().deserialize(response.body).activities
        if context.activity.delivery_mode == DeliveryModes.expect_replies:
            expected_replies = ExpectedReplies(
                activities=context.buffered_reply_activities
            ).serialize()
            return InvokeResponse(status=int(HTTPStatus.OK), body=expected_replies)

        # Handle Invoke scenarios, which deviate from the request/request model in that
        # the Bot will return a specific body and return code.
        if activity.type == ActivityTypes.invoke:
            invoke_response = context.turn_state.get(
                BotFrameworkAdapter._INVOKE_RESPONSE_KEY  # pylint: disable=protected-access
            )
            if invoke_response is None:
                return InvokeResponse(status=int(HTTPStatus.NOT_IMPLEMENTED))
            return InvokeResponse(
                status=invoke_response.value.status,
                body=invoke_response.value.body,
            )

        return None

    async def __generate_callerid(self, claims_identity: ClaimsIdentity) -> str:
        # Is the bot accepting all incoming messages?
        is_auth_disabled = await self._credential_provider.is_authentication_disabled()
        if is_auth_disabled:
            # Return None so that the callerId is cleared.
            return None

        # Is the activity from another bot?
        if SkillValidation.is_skill_claim(claims_identity.claims):
            app_id = JwtTokenValidation.get_app_id_from_claims(claims_identity.claims)
            return f"{CallerIdConstants.bot_to_bot_prefix}{app_id}"

        # Is the activity from Public Azure?
        if not self._channel_provider or self._channel_provider.is_public_azure():
            return CallerIdConstants.public_azure_channel

        # Is the activity from Azure Gov?
        if self._channel_provider and self._channel_provider.is_government():
            return CallerIdConstants.us_gov_channel

        # Return None so that the callerId is cleared.
        return None

    async def _authenticate_request(
        self, request: Activity, auth_header: str
    ) -> ClaimsIdentity:
        """
        Allows for the overriding of authentication in unit tests.

        :param request: The request to authenticate
        :type request: :class:`botbuilder.schema.Activity`
        :param auth_header: The authentication header

        :raises: A permission exception error.

        :return: The request claims identity
        :rtype: :class:`botframework.connector.auth.ClaimsIdentity`
        """
        claims = await JwtTokenValidation.authenticate_request(
            request,
            auth_header,
            self._credential_provider,
            await self.settings.channel_provider.get_channel_service(),
            self.settings.auth_configuration,
        )

        if not claims.is_authenticated:
            raise PermissionError("Unauthorized Access. Request is not authorized")

        return claims

    def _create_context(self, activity):
        """
        Allows for the overriding of the context object in unit tests and derived adapters.
        :param activity:
        :return:
        """
        return TurnContext(self, activity)

    @staticmethod
    async def parse_request(req):
        """
        Parses and validates request
        :param req:
        :return:
        """

        async def validate_activity(activity: Activity):
            if not isinstance(activity.type, str):
                raise TypeError(
                    "BotFrameworkAdapter.parse_request(): invalid or missing activity type."
                )
            return True

        if not isinstance(req, Activity):
            # If the req is a raw HTTP Request, try to deserialize it into an Activity and return the Activity.
            if getattr(req, "body_exists", False):
                try:
                    body = await req.json()
                    activity = Activity().deserialize(body)
                    is_valid_activity = await validate_activity(activity)
                    if is_valid_activity:
                        return activity
                except Exception as error:
                    raise error
            elif "body" in req:
                try:
                    activity = Activity().deserialize(req["body"])
                    is_valid_activity = await validate_activity(activity)
                    if is_valid_activity:
                        return activity
                except Exception as error:
                    raise error
            else:
                raise TypeError(
                    "BotFrameworkAdapter.parse_request(): received invalid request"
                )
        else:
            # The `req` has already been deserialized to an Activity, so verify the Activity.type and return it.
            is_valid_activity = await validate_activity(req)
            if is_valid_activity:
                return req

    async def update_activity(self, context: TurnContext, activity: Activity):
        """
        Replaces an activity that was previously sent to a channel. It should be noted that not all
        channels support this feature.

        :param context: The context object for the turn
        :type context: :class:`TurnContext'
        :param activity: New replacement activity
        :type activity: :class:`botbuilder.schema.Activity`

        :raises: A generic exception error

        :return: A task that represents the work queued to execute

        .. remarks::
            If the activity is successfully sent, the task result contains
            a :class:`botbuilder.schema.ResourceResponse` object containing the ID that
            the receiving channel assigned to the activity.
            Before calling this function, set the ID of the replacement activity to the ID
            of the activity to replace.
        """
        try:
            client = context.turn_state[BotAdapter.BOT_CONNECTOR_CLIENT_KEY]
            return await client.conversations.update_activity(
                activity.conversation.id, activity.id, activity
            )
        except Exception as error:
            raise error

    async def delete_activity(
        self, context: TurnContext, reference: ConversationReference
    ):
        """
        Deletes an activity that was previously sent to a channel. It should be noted that not all
        channels support this feature.

        :param context: The context object for the turn
        :type context: :class:`TurnContext'
        :param reference: Conversation reference for the activity to delete
        :type reference: :class:`botbuilder.schema.ConversationReference`

        :raises: A exception error

        :return: A task that represents the work queued to execute

        .. note::

            The activity_id of the :class:`botbuilder.schema.ConversationReference` identifies the activity to delete.
        """
        try:
            client = context.turn_state[BotAdapter.BOT_CONNECTOR_CLIENT_KEY]
            await client.conversations.delete_activity(
                reference.conversation.id, reference.activity_id
            )
        except Exception as error:
            raise error

    async def send_activities(
        self, context: TurnContext, activities: List[Activity]
    ) -> List[ResourceResponse]:
        try:
            responses: List[ResourceResponse] = []
            for activity in activities:
                response: ResourceResponse = None
                if activity.type == "delay":
                    try:
                        delay_in_ms = float(activity.value) / 1000
                    except TypeError:
                        raise TypeError(
                            "Unexpected delay value passed. Expected number or str type."
                        )
                    except AttributeError:
                        raise Exception("activity.value was not found.")
                    else:
                        await asyncio.sleep(delay_in_ms)
                elif activity.type == "invokeResponse":
                    context.turn_state[self._INVOKE_RESPONSE_KEY] = activity
                else:
                    if not getattr(activity, "service_url", None):
                        raise TypeError(
                            "BotFrameworkAdapter.send_activity(): service_url can not be None."
                        )
                    if (
                        not hasattr(activity, "conversation")
                        or not activity.conversation
                        or not getattr(activity.conversation, "id", None)
                    ):
                        raise TypeError(
                            "BotFrameworkAdapter.send_activity(): conversation.id can not be None."
                        )

                    if activity.type == "trace" and activity.channel_id != "emulator":
                        pass
                    elif activity.reply_to_id:
                        client = context.turn_state[BotAdapter.BOT_CONNECTOR_CLIENT_KEY]
                        response = await client.conversations.reply_to_activity(
                            activity.conversation.id, activity.reply_to_id, activity
                        )
                    else:
                        client = context.turn_state[BotAdapter.BOT_CONNECTOR_CLIENT_KEY]
                        response = await client.conversations.send_to_conversation(
                            activity.conversation.id, activity
                        )

                if not response:
                    response = ResourceResponse(id=activity.id or "")

                responses.append(response)
            return responses
        except Exception as error:
            raise error

    async def delete_conversation_member(
        self, context: TurnContext, member_id: str
    ) -> None:
        """
        Deletes a member from the current conversation.

        :param context: The context object for the turn
        :type context: :class:`botbuilder.core.TurnContext`
        :param member_id: The ID of the member to remove from the conversation
        :type member_id: str

        :raises: A exception error

        :return: A task that represents the work queued to execute.</returns
        """
        try:
            if not context.activity.service_url:
                raise TypeError(
                    "BotFrameworkAdapter.delete_conversation_member(): missing service_url"
                )
            if (
                not context.activity.conversation
                or not context.activity.conversation.id
            ):
                raise TypeError(
                    "BotFrameworkAdapter.delete_conversation_member(): missing conversation or "
                    "conversation.id"
                )

            client = context.turn_state[BotAdapter.BOT_CONNECTOR_CLIENT_KEY]
            return await client.conversations.delete_conversation_member(
                context.activity.conversation.id, member_id
            )
        except AttributeError as attr_e:
            raise attr_e
        except Exception as error:
            raise error

    async def get_activity_members(self, context: TurnContext, activity_id: str):
        """
        Lists the members of a given activity.

        :param context: The context object for the turn
        :type context: :class:`botbuilder.core.TurnContext`
        :param activity_id: (Optional) Activity ID to enumerate.
        If not specified the current activities ID will be used.

        :raises: An exception error

        :return: List of Members of the activity
        """
        try:
            if not activity_id:
                activity_id = context.activity.id
            if not context.activity.service_url:
                raise TypeError(
                    "BotFrameworkAdapter.get_activity_member(): missing service_url"
                )
            if (
                not context.activity.conversation
                or not context.activity.conversation.id
            ):
                raise TypeError(
                    "BotFrameworkAdapter.get_activity_member(): missing conversation or conversation.id"
                )
            if not activity_id:
                raise TypeError(
                    "BotFrameworkAdapter.get_activity_member(): missing both activity_id and "
                    "context.activity.id"
                )

            client = context.turn_state[BotAdapter.BOT_CONNECTOR_CLIENT_KEY]
            return await client.conversations.get_activity_members(
                context.activity.conversation.id, activity_id
            )
        except Exception as error:
            raise error

    async def get_conversation_members(self, context: TurnContext):
        """
        Lists the members of a current conversation.

        :param context: The context object for the turn
        :type context: :class:`botbuilder.core.TurnContext`

        :raises: TypeError if missing service_url or conversation.id

        :return: List of members of the current conversation
        """

        if not context.activity.service_url:
            raise TypeError(
                "BotFrameworkAdapter.get_conversation_members(): missing service_url"
            )
        if not context.activity.conversation or not context.activity.conversation.id:
            raise TypeError(
                "BotFrameworkAdapter.get_conversation_members(): missing conversation or "
                "conversation.id"
            )

        client = context.turn_state[BotAdapter.BOT_CONNECTOR_CLIENT_KEY]
        return await client.conversations.get_conversation_members(
            context.activity.conversation.id
        )

    async def get_conversation_member(
        self, context: TurnContext, member_id: str
    ) -> ChannelAccount:
        """
        Retrieve a member of a current conversation.

        :param context: The context object for the turn
        :type context: :class:`botbuilder.core.TurnContext`
        :param member_id: The member Id
        :type member_id: str

        :raises: A TypeError if missing member_id, service_url, or conversation.id

        :return: A member of the current conversation
        """
        if not context.activity.service_url:
            raise TypeError(
                "BotFrameworkAdapter.get_conversation_member(): missing service_url"
            )
        if not context.activity.conversation or not context.activity.conversation.id:
            raise TypeError(
                "BotFrameworkAdapter.get_conversation_member(): missing conversation or "
                "conversation.id"
            )
        if not member_id:
            raise TypeError(
                "BotFrameworkAdapter.get_conversation_member(): missing memberId"
            )

        client = context.turn_state[BotAdapter.BOT_CONNECTOR_CLIENT_KEY]
        return await client.conversations.get_conversation_member(
            context.activity.conversation.id, member_id
        )

    async def get_conversations(
        self,
        service_url: str,
        credentials: AppCredentials,
        continuation_token: str = None,
    ):
        """
        Lists the Conversations in which this bot has participated for a given channel server.

        :param service_url: The URL of the channel server to query. This can be retrieved from
        `context.activity.serviceUrl`
        :type service_url: str

        :param continuation_token: The continuation token from the previous page of results
        :type continuation_token: str

        :raises: A generic exception error

        :return: A task that represents the work queued to execute

        .. remarks::
            The channel server returns results in pages and each page will include a `continuationToken` that
            can be used to fetch the next page of results from the server.
            If the task completes successfully, the result contains a page of the members of the current conversation.
            This overload may be called from outside the context of a conversation, as only the bot's service URL and
            credentials are required.
        """
        client = self._get_or_create_connector_client(service_url, credentials)
        return await client.conversations.get_conversations(continuation_token)

    async def get_user_token(
        self,
        context: TurnContext,
        connection_name: str,
        magic_code: str = None,
        oauth_app_credentials: AppCredentials = None,  # pylint: disable=unused-argument
    ) -> TokenResponse:
        """
        Attempts to retrieve the token for a user that's in a login flow.

        :param context: Context for the current turn of conversation with the user
        :type context: :class:`botbuilder.core.TurnContext`
        :param connection_name: Name of the auth connection to use
        :type connection_name: str
        :param magic_code" (Optional) user entered code to validate
        :str magic_code" str
        :param oauth_app_credentials: (Optional) AppCredentials for OAuth.
        :type oauth_app_credentials: :class:`botframework.connector.auth.AppCredential`

        :raises: An exception error

        :returns: Token Response
        :rtype: :class:'botbuilder.schema.TokenResponse`

        """

        if (
            context.activity.from_property is None
            or not context.activity.from_property.id
        ):
            raise Exception(
                "BotFrameworkAdapter.get_user_token(): missing from or from.id"
            )
        if not connection_name:
            raise Exception(
                "get_user_token() requires a connection_name but none was provided."
            )

        client = await self._create_token_api_client(context, oauth_app_credentials)

        result = client.user_token.get_token(
            context.activity.from_property.id,
            connection_name,
            context.activity.channel_id,
            magic_code,
        )

        if result is None or result.token is None:
            return None

        return result

    async def sign_out_user(
        self,
        context: TurnContext,
        connection_name: str = None,  # pylint: disable=unused-argument
        user_id: str = None,
        oauth_app_credentials: AppCredentials = None,
    ):
        """
        Signs the user out with the token server.

        :param context: Context for the current turn of conversation with the user
        :type context: :class:`botbuilder.core.TurnContext`
        :param connection_name: Name of the auth connection to use
        :type connection_name: str
        :param user_id: User id of user to sign out
        :type user_id: str
        :param oauth_app_credentials: (Optional) AppCredentials for OAuth.
        :type oauth_app_credentials: :class:`botframework.connector.auth.AppCredential`
        """
        if not context.activity.from_property or not context.activity.from_property.id:
            raise Exception(
                "BotFrameworkAdapter.sign_out_user(): missing from_property or from_property.id"
            )
        if not user_id:
            user_id = context.activity.from_property.id

        client = await self._create_token_api_client(context, oauth_app_credentials)
        client.user_token.sign_out(
            user_id, connection_name, context.activity.channel_id
        )

    async def get_oauth_sign_in_link(
        self,
        context: TurnContext,
        connection_name: str,
        final_redirect: str = None,  # pylint: disable=unused-argument
        oauth_app_credentials: AppCredentials = None,
    ) -> str:
        """
        Gets the raw sign-in link to be sent to the user for sign-in for a connection name.

        :param context: Context for the current turn of conversation with the user
        :type context: :class:`botbuilder.core.TurnContext`
        :param connection_name: Name of the auth connection to use
        :type connection_name: str
        :param final_redirect: The final URL that the OAuth flow will redirect to.
        :param oauth_app_credentials: (Optional) AppCredentials for OAuth.
        :type oauth_app_credentials: :class:`botframework.connector.auth.AppCredential`

        :return: If the task completes successfully, the result contains the raw sign-in link
        """

        client = await self._create_token_api_client(context, oauth_app_credentials)

        conversation = TurnContext.get_conversation_reference(context.activity)
        state = TokenExchangeState(
            connection_name=connection_name,
            conversation=conversation,
            ms_app_id=client.config.credentials.microsoft_app_id,
            relates_to=context.activity.relates_to,
        )

        final_state = base64.b64encode(
            json.dumps(state.serialize()).encode(encoding="UTF-8", errors="strict")
        ).decode()

        return client.bot_sign_in.get_sign_in_url(final_state)

    async def get_token_status(
        self,
        context: TurnContext,
        connection_name: str = None,
        user_id: str = None,
        include_filter: str = None,
        oauth_app_credentials: AppCredentials = None,
    ) -> List[TokenStatus]:
        """
        Retrieves the token status for each configured connection for the given user.

        :param context: Context for the current turn of conversation with the user
        :type context: :class:`botbuilder.core.TurnContext`
        :param connection_name: Name of the auth connection to use
        :type connection_name: str
        :param user_id: The user Id for which tokens are retrieved. If passing in None the userId is taken
        :type user_id: str
        :param include_filter: (Optional) Comma separated list of connection's to include.
        Blank will return token status for all configured connections.
        :type include_filter: str
        :param oauth_app_credentials: (Optional) AppCredentials for OAuth.
        :type oauth_app_credentials: :class:`botframework.connector.auth.AppCredential`

        :returns: Array of :class:`botframework.connector.token_api.modelsTokenStatus`
        """

        if not user_id and (
            not context.activity.from_property or not context.activity.from_property.id
        ):
            raise Exception(
                "BotFrameworkAdapter.get_token_status(): missing from_property or from_property.id"
            )

        client = await self._create_token_api_client(context, oauth_app_credentials)

        user_id = user_id or context.activity.from_property.id
        return client.user_token.get_token_status(
            user_id, context.activity.channel_id, include_filter
        )

    async def get_aad_tokens(
        self,
        context: TurnContext,
        connection_name: str,
        resource_urls: List[str],
        user_id: str = None,  # pylint: disable=unused-argument
        oauth_app_credentials: AppCredentials = None,
    ) -> Dict[str, TokenResponse]:
        """
        Retrieves Azure Active Directory tokens for particular resources on a configured connection.

        :param context: Context for the current turn of conversation with the user
        :type context: :class:`botbuilder.core.TurnContext`
        :param connection_name: The name of the Azure Active Directory connection configured with this bot
        :type connection_name: str
        :param resource_urls: The list of resource URLs to retrieve tokens for
        :type resource_urls: :class:`typing.List`
        :param user_id: The user Id for which tokens are retrieved. If passing in null the userId is taken
        from the Activity in the TurnContext.
        :type user_id: str
        :param oauth_app_credentials: (Optional) AppCredentials for OAuth.
        :type oauth_app_credentials: :class:`botframework.connector.auth.AppCredential`

        :returns: Dictionary of resource Urls to the corresponding :class:'botbuilder.schema.TokenResponse`
        :rtype: :class:`typing.Dict`
        """
        if not context.activity.from_property or not context.activity.from_property.id:
            raise Exception(
                "BotFrameworkAdapter.get_aad_tokens(): missing from_property or from_property.id"
            )

        client = await self._create_token_api_client(context, oauth_app_credentials)
        return client.user_token.get_aad_tokens(
            context.activity.from_property.id,
            connection_name,
            context.activity.channel_id,
            resource_urls,
        )

    async def create_connector_client(
        self, service_url: str, identity: ClaimsIdentity = None, audience: str = None
    ) -> ConnectorClient:
        """
        Implementation of ConnectorClientProvider.create_connector_client.

        :param service_url: The service URL
        :param identity: The claims identity
        :param audience:

        :return: An instance of the :class:`ConnectorClient` class
        """

        if not identity:
            # This is different from C# where an exception is raised.  In this case
            # we are creating a ClaimsIdentity to retain compatibility with this
            # method.
            identity = ClaimsIdentity(
                claims={
                    AuthenticationConstants.AUDIENCE_CLAIM: self.settings.app_id,
                    AuthenticationConstants.APP_ID_CLAIM: self.settings.app_id,
                },
                is_authenticated=True,
            )

        # For requests from channel App Id is in Audience claim of JWT token. For emulator it is in AppId claim.
        # For unauthenticated requests we have anonymous claimsIdentity provided auth is disabled.
        # For Activities coming from Emulator AppId claim contains the Bot's AAD AppId.
        bot_app_id = identity.claims.get(
            AuthenticationConstants.AUDIENCE_CLAIM
        ) or identity.claims.get(AuthenticationConstants.APP_ID_CLAIM)

        # Anonymous claims and non-skill claims should fall through without modifying the scope.
        credentials = None
        if bot_app_id:
            scope = audience
            if not scope:
                scope = (
                    JwtTokenValidation.get_app_id_from_claims(identity.claims)
                    if SkillValidation.is_skill_claim(identity.claims)
                    else self.__get_botframework_oauth_scope()
                )

            credentials = await self.__get_app_credentials(bot_app_id, scope)

        return self._get_or_create_connector_client(service_url, credentials)

    def _get_or_create_connector_client(
        self, service_url: str, credentials: AppCredentials
    ) -> ConnectorClient:
        if not credentials:
            credentials = MicrosoftAppCredentials.empty()

        # Get ConnectorClient from cache or create.
        client_key = BotFrameworkAdapter.key_for_connector_client(
            service_url, credentials.microsoft_app_id, credentials.oauth_scope
        )
        client = self._connector_client_cache.get(client_key)
        if not client:
            client = ConnectorClient(credentials, base_url=service_url)
            client.config.add_user_agent(USER_AGENT)
            self._connector_client_cache[client_key] = client

        return client

    async def get_sign_in_resource_from_user(
        self,
        turn_context: TurnContext,
        connection_name: str,
        user_id: str,
        final_redirect: str = None,
    ) -> SignInUrlResponse:
        return await self.get_sign_in_resource_from_user_and_credentials(
            turn_context, None, connection_name, user_id, final_redirect
        )

    async def get_sign_in_resource_from_user_and_credentials(
        self,
        turn_context: TurnContext,
        oauth_app_credentials: AppCredentials,
        connection_name: str,
        user_id: str,
        final_redirect: str = None,
    ) -> SignInUrlResponse:
        if not connection_name:
            raise TypeError(
                "BotFrameworkAdapter.get_sign_in_resource_from_user_and_credentials(): missing connection_name"
            )
        if not user_id:
            raise TypeError(
                "BotFrameworkAdapter.get_sign_in_resource_from_user_and_credentials(): missing user_id"
            )

        activity = turn_context.activity

        app_id = self.__get_app_id(turn_context)
        token_exchange_state = TokenExchangeState(
            connection_name=connection_name,
            conversation=ConversationReference(
                activity_id=activity.id,
                bot=activity.recipient,
                channel_id=activity.channel_id,
                conversation=activity.conversation,
                locale=activity.locale,
                service_url=activity.service_url,
                user=activity.from_property,
            ),
            relates_to=activity.relates_to,
            ms_app_id=app_id,
        )

        state = base64.b64encode(
            json.dumps(token_exchange_state.serialize()).encode(
                encoding="UTF-8", errors="strict"
            )
        ).decode()

        client = await self._create_token_api_client(
            turn_context, oauth_app_credentials
        )

        return client.bot_sign_in.get_sign_in_resource(
            state, final_redirect=final_redirect
        )

    async def exchange_token(
        self,
        turn_context: TurnContext,
        connection_name: str,
        user_id: str,
        exchange_request: TokenExchangeRequest,
    ) -> TokenResponse:
        return await self.exchange_token_from_credentials(
            turn_context, None, connection_name, user_id, exchange_request
        )

    async def exchange_token_from_credentials(
        self,
        turn_context: TurnContext,
        oauth_app_credentials: AppCredentials,
        connection_name: str,
        user_id: str,
        exchange_request: TokenExchangeRequest,
    ) -> TokenResponse:
        # pylint: disable=no-member

        if not connection_name:
            raise TypeError(
                "BotFrameworkAdapter.exchange_token(): missing connection_name"
            )
        if not user_id:
            raise TypeError("BotFrameworkAdapter.exchange_token(): missing user_id")
        if exchange_request and not exchange_request.token and not exchange_request.uri:
            raise TypeError(
                "BotFrameworkAdapter.exchange_token(): Either a Token or Uri property is required"
                " on the TokenExchangeRequest"
            )

        client = await self._create_token_api_client(
            turn_context, oauth_app_credentials
        )

        result = client.user_token.exchange_async(
            user_id,
            connection_name,
            turn_context.activity.channel_id,
            exchange_request.uri,
            exchange_request.token,
        )

        if isinstance(result, ConnectorTokenResponse):
            return TokenResponse(
                channel_id=result.channel_id,
                connection_name=result.connection_name,
                token=result.token,
                expiration=result.expiration,
            )
        raise TypeError(f"exchange token returned improper result: {type(result)}")

    def can_process_outgoing_activity(
        self, activity: Activity  # pylint: disable=unused-argument
    ) -> bool:
        return False

    async def process_outgoing_activity(
        self, turn_context: TurnContext, activity: Activity
    ) -> ResourceResponse:
        raise Exception("NotImplemented")

    @staticmethod
    def key_for_connector_client(service_url: str, app_id: str, scope: str):
        return f"{service_url if service_url else ''}:{app_id if app_id else ''}:{scope if scope else ''}"

    async def _create_token_api_client(
        self,
        context: TurnContext,
        oauth_app_credentials: AppCredentials = None,
    ) -> TokenApiClient:
        if (
            not self._is_emulating_oauth_cards
            and context.activity.channel_id == "emulator"
            and await self._credential_provider.is_authentication_disabled()
        ):
            self._is_emulating_oauth_cards = True

        app_id = self.__get_app_id(context)
        scope = self.__get_botframework_oauth_scope()
        app_credentials = oauth_app_credentials or await self.__get_app_credentials(
            app_id, scope
        )

        if (
            not self._is_emulating_oauth_cards
            and context.activity.channel_id == "emulator"
            and await self._credential_provider.is_authentication_disabled()
        ):
            self._is_emulating_oauth_cards = True

        # TODO: token_api_client cache

        url = self.__oauth_api_url(context)
        client = TokenApiClient(app_credentials, url)
        client.config.add_user_agent(USER_AGENT)

        if self._is_emulating_oauth_cards:
            # intentionally not awaiting this call
            EmulatorApiClient.emulate_oauth_cards(app_credentials, url, True)

        return client

    def __oauth_api_url(self, context_or_service_url: Union[TurnContext, str]) -> str:
        url = None
        if self._is_emulating_oauth_cards:
            url = (
                context_or_service_url.activity.service_url
                if isinstance(context_or_service_url, object)
                else context_or_service_url
            )
        else:
            if self.settings.oauth_endpoint:
                url = self.settings.oauth_endpoint
            else:
                url = (
                    US_GOV_OAUTH_ENDPOINT
                    if self.settings.channel_provider.is_government()
                    else OAUTH_ENDPOINT
                )

        return url

    @staticmethod
    def key_for_app_credentials(app_id: str, scope: str):
        return f"{app_id}:{scope}"

    async def __get_app_credentials(
        self, app_id: str, oauth_scope: str
    ) -> AppCredentials:
        if not app_id:
            return MicrosoftAppCredentials.empty()

        # get from the cache if it's there
        cache_key = BotFrameworkAdapter.key_for_app_credentials(app_id, oauth_scope)
        app_credentials = self._app_credential_map.get(cache_key)
        if app_credentials:
            return app_credentials

        # If app credentials were provided, use them as they are the preferred choice moving forward
        if self._credentials:
            self._app_credential_map[cache_key] = self._credentials
            return self._credentials

        # Credentials not found in cache, build them
        app_credentials = await self.__build_credentials(app_id, oauth_scope)

        # Cache the credentials for later use
        self._app_credential_map[cache_key] = app_credentials

        return app_credentials

    async def __build_credentials(
        self, app_id: str, oauth_scope: str = None
    ) -> AppCredentials:
        app_password = await self._credential_provider.get_app_password(app_id)

        if self._channel_provider.is_government():
            return MicrosoftGovernmentAppCredentials(
                app_id,
                app_password,
                self.settings.channel_auth_tenant,
                scope=oauth_scope,
            )

        return MicrosoftAppCredentials(
            app_id,
            app_password,
            self.settings.channel_auth_tenant,
            oauth_scope=oauth_scope,
        )

    def __get_botframework_oauth_scope(self) -> str:
        if (
            self.settings.channel_provider
            and self.settings.channel_provider.is_government()
        ):
            return GovernmentConstants.TO_CHANNEL_FROM_BOT_OAUTH_SCOPE
        return AuthenticationConstants.TO_CHANNEL_FROM_BOT_OAUTH_SCOPE

    def __get_app_id(self, context: TurnContext) -> str:
        identity = context.turn_state[BotAdapter.BOT_IDENTITY_KEY]
        if not identity:
            raise Exception("An IIdentity is required in TurnState for this operation.")

        app_id = identity.claims.get(AuthenticationConstants.AUDIENCE_CLAIM)
        if not app_id:
            raise Exception("Unable to get the bot AppId from the audience claim.")

        return app_id
