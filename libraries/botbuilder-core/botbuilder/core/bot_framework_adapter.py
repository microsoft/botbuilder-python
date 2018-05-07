# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import asyncio
from typing import List, Callable
from botbuilder.schema import Activity, ChannelAccount, ConversationReference, ConversationsResult
from botframework.connector import ConnectorClient
from botframework.connector.auth import (MicrosoftAppCredentials,
                                         JwtTokenValidation, SimpleCredentialProvider)

from . import __version__
from .bot_adapter import BotAdapter
from .bot_context import BotContext

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

    async def process_request(self, req, auth_header: str, logic: Callable):
        request = await self.parse_request(req)
        auth_header = auth_header or ''

        await self.authenticate_request(request, auth_header)
        context = self.create_context(request)

        return await self.run_middleware(context, logic)

    async def authenticate_request(self, request: Activity, auth_header: str):
        await JwtTokenValidation.assert_valid_activity(request, auth_header, self._credential_provider)

    def create_context(self, activity):
        return BotContext(self, activity)

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

    async def update_activity(self, activity: Activity):
        try:
            connector_client = ConnectorClient(self._credentials, activity.service_url)
            connector_client.config.add_user_agent(USER_AGENT)
            return await connector_client.conversations.update_activity_async(
                activity.conversation.id,
                activity.conversation.activity_id,
                activity)
        except Exception as e:
            raise e

    async def delete_activity(self, conversation_reference: ConversationReference):
        try:
            connector_client = ConnectorClient(self._credentials, conversation_reference.service_url)
            connector_client.config.add_user_agent(USER_AGENT)
            await connector_client.conversations.delete_activity_async(conversation_reference.conversation.id,
                                                           conversation_reference.activity_id)
        except Exception as e:
            raise e

    async def send_activity(self, activities: List[Activity]):
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
                    connector_client = ConnectorClient(self._credentials, activity.service_url)
                    connector_client.config.add_user_agent(USER_AGENT)
                    await connector_client.conversations.send_to_conversation_async(activity.conversation.id, activity)
        except Exception as e:
            raise e

    async def delete_conversation_member(self, context: BotContext, member_id: str) -> None:
        """
        Deletes a member from the current conversation.
        :param context:
        :param member_id:
        :return:
        """
        try:
            if not context.request.service_url:
                raise TypeError('BotFrameworkAdapter.delete_conversation_member(): missing service_url')
            if not context.request.conversation or not context.request.conversation.id:
                raise TypeError('BotFrameworkAdapter.delete_conversation_member(): missing conversation or '
                                'conversation.id')
            service_url = context.request.service_url
            conversation_id = context.request.conversation.id
            client = ConnectorClient(self._credentials, service_url)
            client.config.add_user_agent(USER_AGENT)
            return await client.conversations.delete_conversation_member_async(conversation_id, member_id)
        except AttributeError as attr_e:
            raise attr_e
        except Exception as e:
            raise e

    async def get_activity_members(self, context: BotContext, activity_id: str):
        """
        Lists the members of a given activity.
        :param context:
        :param activity_id:
        :return:
        """
        try:
            if not activity_id:
                activity_id = context.request.id
            if not context.request.service_url:
                raise TypeError('BotFrameworkAdapter.get_activity_member(): missing service_url')
            if not context.request.conversation or not context.request.conversation.id:
                raise TypeError('BotFrameworkAdapter.get_activity_member(): missing conversation or conversation.id')
            if not activity_id:
                raise TypeError('BotFrameworkAdapter.get_activity_member(): missing both activity_id and '
                                'context.activity.id')
            service_url = context.request.service_url
            conversation_id = context.request.conversation.id
            client = ConnectorClient(self._credentials, service_url)
            client.config.add_user_agent(USER_AGENT)
            return await client.conversations.get_activity_members_async(conversation_id, activity_id)
        except Exception as e:
            raise e

    async def get_conversation_members(self, context: BotContext):
        """
        Lists the members of a current conversation.
        :param context:
        :return:
        """
        try:
            if not context.request.service_url:
                raise TypeError('BotFrameworkAdapter.get_conversation_members(): missing service_url')
            if not context.request.conversation or not context.request.conversation.id:
                raise TypeError('BotFrameworkAdapter.get_conversation_members(): missing conversation or '
                                'conversation.id')
            service_url = context.request.service_url
            conversation_id = context.request.conversation.id
            client = ConnectorClient(self._credentials, service_url)
            client.config.add_user_agent(USER_AGENT)
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
        client = ConnectorClient(self._credentials, service_url)
        client.config.add_user_agent(USER_AGENT)
        return await client.conversations.get_conversations_async(continuation_token)
