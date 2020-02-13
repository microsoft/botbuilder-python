# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

# pylint: disable=too-many-lines

import asyncio
import base64
import json
import os
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
    SimpleCredentialProvider,
    SkillValidation,
    CertificateAppCredentials,
)
from botframework.connector.token_api import TokenApiClient
from botframework.connector.token_api.models import TokenStatus
from botbuilder.schema import (
    Activity,
    ActivityTypes,
    ConversationAccount,
    ConversationParameters,
    ConversationReference,
    TokenResponse,
    ResourceResponse,
)

from . import __version__
from .bot_adapter import BotAdapter
from .turn_context import TurnContext
from .user_token_provider import UserTokenProvider
from .invoke_response import InvokeResponse
from .conversation_reference_extension import get_continuation_activity

USER_AGENT = f"Microsoft-BotFramework/3.1 (BotBuilder Python/{__version__})"
OAUTH_ENDPOINT = "https://api.botframework.com"
US_GOV_OAUTH_ENDPOINT = "https://api.botframework.azure.us"
BOT_IDENTITY_KEY = "BotIdentity"


class TokenExchangeState(Model):
    _attribute_map = {
        "connection_name": {"key": "connectionName", "type": "str"},
        "conversation": {"key": "conversation", "type": "ConversationReference"},
        "bot_url": {"key": "botUrl", "type": "str"},
        "ms_app_id": {"key": "msAppId", "type": "str"},
    }

    def __init__(
        self,
        *,
        connection_name: str = None,
        conversation: ConversationReference = None,
        bot_url: str = None,
        ms_app_id: str = None,
        **kwargs,
    ) -> None:
        super(TokenExchangeState, self).__init__(**kwargs)
        self.connection_name = connection_name
        self.conversation = conversation
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
        channel_service: str = None,
        channel_provider: ChannelProvider = None,
        auth_configuration: AuthenticationConfiguration = None,
        certificate_thumbprint: str = None,
        certificate_private_key: str = None,
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
        :param channel_service:
        :type channel_service: str
        :param channel_provider: The channel provider
        :type channel_provider: :class:`botframework.connector.auth.ChannelProvider`
        :param auth_configuration:
        :type auth_configuration: :class:`botframework.connector.auth.AuthenticationConfiguration`
        :param certificate_thumbprint: X509 thumbprint
        :type certificate_thumbprint: str
        :param certificate_private_key: X509 private key
        :type certificate_private_key: str

        .. remarks::
            For credentials authorization, both app_id and app_password are required.
            For certificate authorization, app_id, certificate_thumbprint, and certificate_private_key are required.

        """
        self.app_id = app_id
        self.app_password = app_password
        self.channel_auth_tenant = channel_auth_tenant
        self.oauth_endpoint = oauth_endpoint
        self.open_id_metadata = open_id_metadata
        self.channel_service = channel_service
        self.channel_provider = channel_provider
        self.auth_configuration = auth_configuration or AuthenticationConfiguration()
        self.certificate_thumbprint = certificate_thumbprint
        self.certificate_private_key = certificate_private_key


class BotFrameworkAdapter(BotAdapter, UserTokenProvider):
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

    _INVOKE_RESPONSE_KEY = "BotFrameworkAdapter.InvokeResponse"

    def __init__(self, settings: BotFrameworkAdapterSettings):
        """
        Initializes a new instance of the :class:`BotFrameworkAdapter` class.

        :param settings: The settings to initialize the adapter
        :type settings: :class:`BotFrameworkAdapterSettings`
        """
        super(BotFrameworkAdapter, self).__init__()
        self.settings = settings or BotFrameworkAdapterSettings("", "")

        # If settings.certificate_thumbprint & settings.certificate_private_key are provided,
        # use CertificateAppCredentials.
        if self.settings.certificate_thumbprint and settings.certificate_private_key:
            self._credentials = CertificateAppCredentials(
                self.settings.app_id,
                self.settings.certificate_thumbprint,
                self.settings.certificate_private_key,
                self.settings.channel_auth_tenant,
            )
            self._credential_provider = SimpleCredentialProvider(
                self.settings.app_id, ""
            )
        else:
            self._credentials = MicrosoftAppCredentials(
                self.settings.app_id,
                self.settings.app_password,
                self.settings.channel_auth_tenant,
            )
            self._credential_provider = SimpleCredentialProvider(
                self.settings.app_id, self.settings.app_password
            )

        self._is_emulating_oauth_cards = False

        # If no channel_service or open_id_metadata values were passed in the settings, check the
        # process' Environment Variables for values.
        # These values may be set when a bot is provisioned on Azure and if so are required for
        # the bot to properly work in Public Azure or a National Cloud.
        self.settings.channel_service = self.settings.channel_service or os.environ.get(
            AuthenticationConstants.CHANNEL_SERVICE
        )
        self.settings.open_id_metadata = (
            self.settings.open_id_metadata
            or os.environ.get(AuthenticationConstants.BOT_OPEN_ID_METADATA_KEY)
        )

        if self.settings.open_id_metadata:
            ChannelValidation.open_id_metadata_endpoint = self.settings.open_id_metadata
            GovernmentChannelValidation.OPEN_ID_METADATA_ENDPOINT = (
                self.settings.open_id_metadata
            )

        if JwtTokenValidation.is_government(self.settings.channel_service):
            self._credentials.oauth_endpoint = (
                GovernmentConstants.TO_CHANNEL_FROM_BOT_LOGIN_URL
            )
            self._credentials.oauth_scope = (
                GovernmentConstants.TO_CHANNEL_FROM_BOT_OAUTH_SCOPE
            )

        self._connector_client_cache: Dict[str, ConnectorClient] = {}

    async def continue_conversation(
        self,
        reference: ConversationReference,
        callback: Callable,
        bot_id: str = None,
        claims_identity: ClaimsIdentity = None,  # pylint: disable=unused-argument
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

        :raises: It raises an argument null exception.

        :return: A task that represents the work queued to execute.

        .. remarks::
            This is often referred to as the bots *proactive messaging* flow as it lets the bot proactively
            send messages to a conversation or user that are already in a communication.
            Scenarios such as sending notifications or coupons to a user are enabled by this function.
        """
        # TODO: proactive messages
        if not claims_identity:
            if not bot_id:
                raise TypeError("Expected bot_id: str but got None instead")

            claims_identity = ClaimsIdentity(
                claims={
                    AuthenticationConstants.AUDIENCE_CLAIM: bot_id,
                    AuthenticationConstants.APP_ID_CLAIM: bot_id,
                },
                is_authenticated=True,
            )

        context = TurnContext(self, get_continuation_activity(reference))
        context.turn_state[BOT_IDENTITY_KEY] = claims_identity
        context.turn_state["BotCallbackHandler"] = callback
        await self._ensure_channel_connector_client_is_created(
            reference.service_url, claims_identity
        )
        return await self.run_pipeline(context, callback)

    async def create_conversation(
        self,
        reference: ConversationReference,
        logic: Callable[[TurnContext], Awaitable] = None,
        conversation_parameters: ConversationParameters = None,
    ):
        """
        Starts a new conversation with a user. Used to direct message to a member of a group.

        :param reference: The conversation reference that contains the tenant
        :type reference: :class:`botbuilder.schema.ConversationReference`
        :param logic: The logic to use for the creation of the conversation
        :type logic: :class:`typing.Callable`
        :param conversation_parameters: The information to use to create the conversation
        :type conversation_parameters:

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
            will contain the ID of the new conversation.</para>
        """
        try:
            if reference.service_url is None:
                raise TypeError(
                    "BotFrameworkAdapter.create_conversation(): reference.service_url cannot be None."
                )

            # Create conversation
            parameters = (
                conversation_parameters
                if conversation_parameters
                else ConversationParameters(
                    bot=reference.bot, members=[reference.user], is_group=False
                )
            )
            client = await self.create_connector_client(reference.service_url)

            # Mix in the tenant ID if specified. This is required for MS Teams.
            if reference.conversation is not None and reference.conversation.tenant_id:
                # Putting tenant_id in channel_data is a temporary while we wait for the Teams API to be updated
                parameters.channel_data = {
                    "tenant": {"id": reference.conversation.tenant_id}
                }

                # Permanent solution is to put tenant_id in parameters.tenant_id
                parameters.tenant_id = reference.conversation.tenant_id

            resource_response = await client.conversations.create_conversation(
                parameters
            )
            request = TurnContext.apply_conversation_reference(
                Activity(type=ActivityTypes.event, name="CreateConversation"),
                reference,
                is_incoming=True,
            )
            request.conversation = ConversationAccount(
                id=resource_response.id, tenant_id=parameters.tenant_id
            )
            request.channel_data = parameters.channel_data
            if resource_response.service_url:
                request.service_url = resource_response.service_url

            context = self.create_context(request)
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

        identity = await self.authenticate_request(activity, auth_header)
        context = self.create_context(activity)
        context.turn_state[BOT_IDENTITY_KEY] = identity

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

        if activity.type == ActivityTypes.invoke:
            invoke_response = context.turn_state.get(
                BotFrameworkAdapter._INVOKE_RESPONSE_KEY  # pylint: disable=protected-access
            )
            if invoke_response is None:
                return InvokeResponse(status=501)
            return invoke_response.value

        return None

    async def authenticate_request(
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
            self.settings.channel_service,
            self.settings.auth_configuration,
        )

        if not claims.is_authenticated:
            raise PermissionError("Unauthorized Access. Request is not authorized")

        return claims

    def create_context(self, activity):
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
            identity: ClaimsIdentity = context.turn_state.get(BOT_IDENTITY_KEY)
            client = await self.create_connector_client(activity.service_url, identity)
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
            identity: ClaimsIdentity = context.turn_state.get(BOT_IDENTITY_KEY)
            client = await self.create_connector_client(reference.service_url, identity)
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

                    identity: ClaimsIdentity = context.turn_state.get(BOT_IDENTITY_KEY)
                    client = await self.create_connector_client(
                        activity.service_url, identity
                    )
                    if activity.type == "trace" and activity.channel_id != "emulator":
                        pass
                    elif activity.reply_to_id:
                        response = await client.conversations.reply_to_activity(
                            activity.conversation.id, activity.reply_to_id, activity
                        )
                    else:
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
            service_url = context.activity.service_url
            conversation_id = context.activity.conversation.id
            identity: ClaimsIdentity = context.turn_state.get(BOT_IDENTITY_KEY)
            client = await self.create_connector_client(service_url, identity)
            return await client.conversations.delete_conversation_member(
                conversation_id, member_id
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
            service_url = context.activity.service_url
            conversation_id = context.activity.conversation.id
            identity: ClaimsIdentity = context.turn_state.get(BOT_IDENTITY_KEY)
            client = await self.create_connector_client(service_url, identity)
            return await client.conversations.get_activity_members(
                conversation_id, activity_id
            )
        except Exception as error:
            raise error

    async def get_conversation_members(self, context: TurnContext):
        """
        Lists the members of a current conversation.

        :param context: The context object for the turn
        :type context: :class:`botbuilder.core.TurnContext`

        :raises: An exception error

        :return: List of members of the current conversation
        """
        try:
            if not context.activity.service_url:
                raise TypeError(
                    "BotFrameworkAdapter.get_conversation_members(): missing service_url"
                )
            if (
                not context.activity.conversation
                or not context.activity.conversation.id
            ):
                raise TypeError(
                    "BotFrameworkAdapter.get_conversation_members(): missing conversation or "
                    "conversation.id"
                )
            service_url = context.activity.service_url
            conversation_id = context.activity.conversation.id
            identity: ClaimsIdentity = context.turn_state.get(BOT_IDENTITY_KEY)
            client = await self.create_connector_client(service_url, identity)
            return await client.conversations.get_conversation_members(conversation_id)
        except Exception as error:
            raise error

    async def get_conversations(self, service_url: str, continuation_token: str = None):
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
        client = await self.create_connector_client(service_url)
        return await client.conversations.get_conversations(continuation_token)

    async def get_user_token(
        self, context: TurnContext, connection_name: str, magic_code: str = None
    ) -> TokenResponse:

        """
        Attempts to retrieve the token for a user that's in a login flow.

        :param context: Context for the current turn of conversation with the user
        :type context: :class:`botbuilder.core.TurnContext`
        :param connection_name: Name of the auth connection to use
        :type connection_name: str
        :param magic_code" (Optional) user entered code to validate
        :str magic_code" str

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

        self.check_emulating_oauth_cards(context)
        user_id = context.activity.from_property.id
        url = self.oauth_api_url(context)
        client = self.create_token_api_client(url)

        result = client.user_token.get_token(
            user_id, connection_name, context.activity.channel_id, magic_code
        )

        # TODO check form of response
        if result is None or result.token is None:
            return None

        return result

    async def sign_out_user(
        self, context: TurnContext, connection_name: str = None, user_id: str = None
    ) -> str:
        """
        Signs the user out with the token server.

        :param context: Context for the current turn of conversation with the user
        :type context: :class:`botbuilder.core.TurnContext`
        :param connection_name: Name of the auth connection to use
        :type connection_name: str
        :param user_id: User id of user to sign out
        :type user_id: str

        :returns: A task that represents the work queued to execute
        """
        if not context.activity.from_property or not context.activity.from_property.id:
            raise Exception(
                "BotFrameworkAdapter.sign_out_user(): missing from_property or from_property.id"
            )
        if not user_id:
            user_id = context.activity.from_property.id

        self.check_emulating_oauth_cards(context)
        url = self.oauth_api_url(context)
        client = self.create_token_api_client(url)
        client.user_token.sign_out(
            user_id, connection_name, context.activity.channel_id
        )

    async def get_oauth_sign_in_link(
        self, context: TurnContext, connection_name: str
    ) -> str:
        """
        Gets the raw sign-in link to be sent to the user for sign-in for a connection name.

        :param context: Context for the current turn of conversation with the user
        :type context: :class:`botbuilder.core.TurnContext`
        :param connection_name: Name of the auth connection to use
        :type connection_name: str

        :returns: A task that represents the work queued to execute

        .. note::

            If the task completes successfully, the result contains the raw sign-in link
        """
        self.check_emulating_oauth_cards(context)
        conversation = TurnContext.get_conversation_reference(context.activity)
        url = self.oauth_api_url(context)
        client = self.create_token_api_client(url)
        state = TokenExchangeState(
            connection_name=connection_name,
            conversation=conversation,
            ms_app_id=client.config.credentials.microsoft_app_id,
        )

        final_state = base64.b64encode(
            json.dumps(state.serialize()).encode(encoding="UTF-8", errors="strict")
        ).decode()

        return client.bot_sign_in.get_sign_in_url(final_state)

    async def get_token_status(
        self, context: TurnContext, user_id: str = None, include_filter: str = None
    ) -> List[TokenStatus]:

        """
        Retrieves the token status for each configured connection for the given user.

        :param context: Context for the current turn of conversation with the user
        :type context: :class:`botbuilder.core.TurnContext`
        :param user_id: The user Id for which token status is retrieved
        :type user_id: str
        :param include_filter: (Optional) Comma separated list of connection's to include.
        Blank will return token status for all configured connections.
        :type include_filter: str

        :returns: Array of :class:`botframework.connector.token_api.modelsTokenStatus`
        """

        if not user_id and (
            not context.activity.from_property or not context.activity.from_property.id
        ):
            raise Exception(
                "BotFrameworkAdapter.get_token_status(): missing from_property or from_property.id"
            )

        self.check_emulating_oauth_cards(context)
        user_id = user_id or context.activity.from_property.id
        url = self.oauth_api_url(context)
        client = self.create_token_api_client(url)

        # TODO check form of response
        return client.user_token.get_token_status(
            user_id, context.activity.channel_id, include_filter
        )

    async def get_aad_tokens(
        self, context: TurnContext, connection_name: str, resource_urls: List[str]
    ) -> Dict[str, TokenResponse]:
        """
        Retrieves Azure Active Directory tokens for particular resources on a configured connection.

        :param context: Context for the current turn of conversation with the user
        :type context: :class:`botbuilder.core.TurnContext`
        :param connection_name: The name of the Azure Active Directory connection configured with this bot
        :type connection_name: str
        :param resource_urls: The list of resource URLs to retrieve tokens for
        :type resource_urls: :class:`typing.List`
        :returns: Dictionary of resource Urls to the corresponding :class:'botbuilder.schema.TokenResponse`
        :rtype: :class:`typing.Dict`
        """
        if not context.activity.from_property or not context.activity.from_property.id:
            raise Exception(
                "BotFrameworkAdapter.get_aad_tokens(): missing from_property or from_property.id"
            )

        self.check_emulating_oauth_cards(context)
        user_id = context.activity.from_property.id
        url = self.oauth_api_url(context)
        client = self.create_token_api_client(url)

        # TODO check form of response
        return client.user_token.get_aad_tokens(
            user_id, connection_name, context.activity.channel_id, resource_urls
        )

    async def create_connector_client(
        self, service_url: str, identity: ClaimsIdentity = None
    ) -> ConnectorClient:
        """Allows for mocking of the connector client in unit tests
        :param service_url: The service URL
        :param identity: The claims identity

        :return: An instance of the :class:`ConnectorClient` class
        """

        # Anonymous claims and non-skill claims should fall through without modifying the scope.
        credentials = self._credentials

        if identity:
            bot_app_id_claim = identity.claims.get(
                AuthenticationConstants.AUDIENCE_CLAIM
            ) or identity.claims.get(AuthenticationConstants.APP_ID_CLAIM)

            if bot_app_id_claim and SkillValidation.is_skill_claim(identity.claims):
                scope = JwtTokenValidation.get_app_id_from_claims(identity.claims)

                # Do nothing, if the current credentials and its scope are valid for the skill.
                # i.e. the adapter instance is pre-configured to talk with one skill.
                # Otherwise we will create a new instance of the AppCredentials
                # so self._credentials.oauth_scope isn't overridden.
                if self._credentials.oauth_scope != scope:
                    password = await self._credential_provider.get_app_password(
                        bot_app_id_claim
                    )
                    credentials = MicrosoftAppCredentials(
                        bot_app_id_claim, password, oauth_scope=scope
                    )
                    if (
                        self.settings.channel_provider
                        and self.settings.channel_provider.is_government()
                    ):
                        credentials.oauth_endpoint = (
                            GovernmentConstants.TO_CHANNEL_FROM_BOT_LOGIN_URL
                        )
                        credentials.oauth_scope = (
                            GovernmentConstants.TO_CHANNEL_FROM_BOT_OAUTH_SCOPE
                        )

        client_key = (
            f"{service_url}{credentials.microsoft_app_id if credentials else ''}"
        )
        client = self._connector_client_cache.get(client_key)

        if not client:
            client = ConnectorClient(credentials, base_url=service_url)
            client.config.add_user_agent(USER_AGENT)
            self._connector_client_cache[client_key] = client

        return client

    def create_token_api_client(self, service_url: str) -> TokenApiClient:
        client = TokenApiClient(self._credentials, service_url)
        client.config.add_user_agent(USER_AGENT)

        return client

    async def emulate_oauth_cards(
        self, context_or_service_url: Union[TurnContext, str], emulate: bool
    ):
        self._is_emulating_oauth_cards = emulate
        url = self.oauth_api_url(context_or_service_url)
        await EmulatorApiClient.emulate_oauth_cards(self._credentials, url, emulate)

    def oauth_api_url(self, context_or_service_url: Union[TurnContext, str]) -> str:
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
                    if JwtTokenValidation.is_government(self.settings.channel_service)
                    else OAUTH_ENDPOINT
                )

        return url

    def check_emulating_oauth_cards(self, context: TurnContext):
        if (
            not self._is_emulating_oauth_cards
            and context.activity.channel_id == "emulator"
            and (
                not self._credentials.microsoft_app_id
                or not self._credentials.microsoft_app_password
            )
        ):
            self._is_emulating_oauth_cards = True

    async def _ensure_channel_connector_client_is_created(
        self, service_url: str, claims_identity: ClaimsIdentity
    ):
        # Ensure we have a default ConnectorClient and MSAppCredentials instance for the audience.
        audience = claims_identity.claims.get(AuthenticationConstants.AUDIENCE_CLAIM)

        if (
            not audience
            or AuthenticationConstants.TO_BOT_FROM_CHANNEL_TOKEN_ISSUER != audience
        ):
            # We create a default connector for audiences that are not coming from
            # the default https://api.botframework.com audience.
            # We create a default claim that contains only the desired audience.
            default_connector_claims = {
                AuthenticationConstants.AUDIENCE_CLAIM: audience
            }
            connector_claims_identity = ClaimsIdentity(
                claims=default_connector_claims, is_authenticated=True
            )

            await self.create_connector_client(service_url, connector_claims_identity)

        if SkillValidation.is_skill_claim(claims_identity.claims):
            # Add the channel service URL to the trusted services list so we can send messages back.
            # the service URL for skills is trusted because it is applied by the
            # SkillHandler based on the original request received by the root bot
            MicrosoftAppCredentials.trust_service_url(service_url)
