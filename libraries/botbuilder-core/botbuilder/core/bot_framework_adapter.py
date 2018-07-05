# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import asyncio
from typing import List, Callable
from botbuilder.schema import (Activity, ChannelAccount,
                               ConversationAccount,
                               ConversationParameters, ConversationReference,
                               ConversationsResult, ConversationResourceResponse)
from botframework.connector import ConnectorClient
from botframework.connector.auth import (MicrosoftAppCredentials,
                                         JwtTokenValidation, SimpleCredentialProvider)

from . import __version__
from .bot_adapter import BotAdapter
from .turn_context import TurnContext

USER_AGENT = f"Microsoft-BotFramework/3.1 (BotBuilder Python/{__version__})"


class BotFrameworkAdapterSettings(object):
    def __init__(self, app_id: str, app_password: str):
        self.app_id = app_id
        self.app_password = app_password


class BotFrameworkAdapter(BotAdapter):

    def __init__(self, settings: BotFrameworkAdapterSettings):
        super(BotFrameworkAdapter, self).__init__()
        self.settings = settings or BotFrameworkAdapterSettings('', '')
        self._credentials = MicrosoftAppCredentials(self.settings.app_id, self.settings.app_password)
        self._credential_provider = SimpleCredentialProvider(self.settings.app_id, self.settings.app_password)

    async def continue_conversation(self, reference: ConversationReference, logic):
        """
        Continues a conversation with a user. This is often referred to as the bots "Proactive Messaging"
        flow as its lets the bot proactively send messages to a conversation or user that its already
        communicated with. Scenarios like sending notifications or coupons to a user are enabled by this
        method.
        :param reference:
        :param logic:
        :return:
        """
        request = TurnContext.apply_conversation_reference(Activity(), reference, is_incoming=True)
        context = self.create_context(request)
        return await self.run_middleware(context, logic)

    async def create_conversation(self, reference: ConversationReference, logic):
        """
        Starts a new conversation with a user. This is typically used to Direct Message (DM) a member
        of a group.
        :param reference:
        :param logic:
        :return:
        """
        try:
            if reference.service_url is None:
                raise TypeError('BotFrameworkAdapter.create_conversation(): reference.service_url cannot be None.')

            # Create conversation
            parameters = ConversationParameters(bot=reference.bot)
            client = self.create_connector_client(reference.service_url)

            resource_response = await client.conversations.create_conversation_async(parameters)
            request = TurnContext.apply_conversation_reference(Activity(), reference, is_incoming=True)
            request.conversation = ConversationAccount(id=resource_response.id)
            if resource_response.service_url:
                request.service_url = resource_response.service_url

            context = self.create_context(request)
            return await self.run_middleware(context, logic)

        except Exception as e:
            raise e

    async def process_activity(self, req, auth_header: str, logic: Callable):
        """
        Processes an activity received by the bots web server. This includes any messages sent from a
        user and is the method that drives what's often referred to as the bots "Reactive Messaging"
        flow.
        :param req:
        :param auth_header:
        :param logic:
        :return:
        """
        activity = await self.parse_request(req)
        auth_header = auth_header or ''

        await self.authenticate_request(activity, auth_header)
        context = self.create_context(activity)

        return await self.run_middleware(context, logic)

    async def authenticate_request(self, request: Activity, auth_header: str):
        """
        Allows for the overriding of authentication in unit tests.
        :param request:
        :param auth_header:
        :return:
        """
        await JwtTokenValidation.authenticate_request(request, auth_header, self._credential_provider)

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
                raise TypeError('BotFrameworkAdapter.parse_request(): invalid or missing activity type.')
            return True

        if not isinstance(req, Activity):
            # If the req is a raw HTTP Request, try to deserialize it into an Activity and return the Activity.
            if hasattr(req, 'body'):
                try:
                    activity = Activity().deserialize(req.body)
                    is_valid_activity = await validate_activity(activity)
                    if is_valid_activity:
                        return activity
                except Exception as e:
                    raise e
            elif 'body' in req:
                try:
                    activity = Activity().deserialize(req['body'])
                    is_valid_activity = await validate_activity(activity)
                    if is_valid_activity:
                        return activity
                except Exception as e:
                    raise e
            else:
                raise TypeError('BotFrameworkAdapter.parse_request(): received invalid request')
        else:
            # The `req` has already been deserialized to an Activity, so verify the Activity.type and return it.
            is_valid_activity = await validate_activity(req)
            if is_valid_activity:
                return req

    async def update_activity(self, context: TurnContext, activity: Activity):
        """
        Replaces an activity that was previously sent to a channel. It should be noted that not all
        channels support this feature.
        :param context:
        :param activity:
        :return:
        """
        try:
            client = self.create_connector_client(activity.service_url)
            return await client.conversations.update_activity_async(
                activity.conversation.id,
                activity.conversation.activity_id,
                activity)
        except Exception as e:
            raise e

    async def delete_activity(self, context: TurnContext, conversation_reference: ConversationReference):
        """
        Deletes an activity that was previously sent to a channel. It should be noted that not all
        channels support this feature.
        :param context:
        :param conversation_reference:
        :return:
        """
        try:
            client = self.create_connector_client(conversation_reference.service_url)
            await client.conversations.delete_activity_async(conversation_reference.conversation.id,
                                                             conversation_reference.activity_id)
        except Exception as e:
            raise e

    async def send_activities(self, context: TurnContext, activities: List[Activity]):
        try:
            for activity in activities:
                if activity.type == 'delay':
                    try:
                        delay_in_ms = float(activity.value) / 1000
                    except TypeError:
                        raise TypeError('Unexpected delay value passed. Expected number or str type.')
                    except AttributeError:
                        raise Exception('activity.value was not found.')
                    else:
                        await asyncio.sleep(delay_in_ms)
                else:
                    client = self.create_connector_client(activity.service_url)
                    await client.conversations.send_to_conversation_async(activity.conversation.id, activity)
        except Exception as e:
            raise e

    async def delete_conversation_member(self, context: TurnContext, member_id: str) -> None:
        """
        Deletes a member from the current conversation.
        :param context:
        :param member_id:
        :return:
        """
        try:
            if not context.activity.service_url:
                raise TypeError('BotFrameworkAdapter.delete_conversation_member(): missing service_url')
            if not context.activity.conversation or not context.activity.conversation.id:
                raise TypeError('BotFrameworkAdapter.delete_conversation_member(): missing conversation or '
                                'conversation.id')
            service_url = context.activity.service_url
            conversation_id = context.activity.conversation.id
            client = self.create_connector_client(service_url)
            return await client.conversations.delete_conversation_member_async(conversation_id, member_id)
        except AttributeError as attr_e:
            raise attr_e
        except Exception as e:
            raise e

    async def get_activity_members(self, context: TurnContext, activity_id: str):
        """
        Lists the members of a given activity.
        :param context:
        :param activity_id:
        :return:
        """
        try:
            if not activity_id:
                activity_id = context.activity.id
            if not context.activity.service_url:
                raise TypeError('BotFrameworkAdapter.get_activity_member(): missing service_url')
            if not context.activity.conversation or not context.activity.conversation.id:
                raise TypeError('BotFrameworkAdapter.get_activity_member(): missing conversation or conversation.id')
            if not activity_id:
                raise TypeError('BotFrameworkAdapter.get_activity_member(): missing both activity_id and '
                                'context.activity.id')
            service_url = context.activity.service_url
            conversation_id = context.activity.conversation.id
            client = self.create_connector_client(service_url)
            return await client.conversations.get_activity_members_async(conversation_id, activity_id)
        except Exception as e:
            raise e

    async def get_conversation_members(self, context: TurnContext):
        """
        Lists the members of a current conversation.
        :param context:
        :return:
        """
        try:
            if not context.activity.service_url:
                raise TypeError('BotFrameworkAdapter.get_conversation_members(): missing service_url')
            if not context.activity.conversation or not context.activity.conversation.id:
                raise TypeError('BotFrameworkAdapter.get_conversation_members(): missing conversation or '
                                'conversation.id')
            service_url = context.activity.service_url
            conversation_id = context.activity.conversation.id
            client = self.create_connector_client(service_url)
            return await client.conversations.get_conversation_members_async(conversation_id)
        except Exception as e:
            raise e

    async def get_conversations(self, service_url: str, continuation_token: str=None):
        """
        Lists the Conversations in which this bot has participated for a given channel server. The channel server
        returns results in pages and each page will include a `continuationToken` that can be used to fetch the next
        page of results from the server.
        :param service_url:
        :param continuation_token:
        :return:
        """
        client = self.create_connector_client(service_url)
        return await client.conversations.get_conversations_async(continuation_token)

    def create_connector_client(self, service_url: str) -> ConnectorClient:
        """
        Allows for mocking of the connector client in unit tests.
        :param service_url:
        :return:
        """
        client = ConnectorClient(self._credentials, base_url=service_url)
        client.config.add_user_agent(USER_AGENT)
        return client
