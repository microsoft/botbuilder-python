# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import asyncio
from typing import List, Callable
from botbuilder.schema import Activity, ConversationReference
from botframework.connector import ConnectorClient
from botframework.connector.auth import (MicrosoftAppCredentials,
                                         JwtTokenValidation, SimpleCredentialProvider)

from .bot_adapter import BotAdapter
from .bot_context import BotContext


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
                except BaseException as e:
                    raise e
            elif 'body' in req:
                try:
                    activity = Activity().deserialize(req['body'])
                    is_valid_activity = await validate_activity(activity)
                    if is_valid_activity:
                        return activity
                except BaseException as e:
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
            return connector_client.conversations.update_activity(
                activity.conversation.id,
                activity.conversation.activity_id,
                activity)
        except BaseException as e:
            raise e

    async def delete_activity(self, conversation_reference: ConversationReference):
        try:
            connector_client = ConnectorClient(self._credentials, conversation_reference.service_url)
            connector_client.conversations.delete_activity(conversation_reference.conversation.id,
                                                           conversation_reference.activity_id)
        except BaseException as e:
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
                    connector_client.conversations.send_to_conversation(activity.conversation.id, activity)
        except BaseException as e:
            raise e

    # Legacy code.
    async def send(self, activities: List[Activity]):
        for activity in activities:
            connector = ConnectorClient(self._credentials, base_url=activity.service_url)
            await connector.conversations.send_to_conversation_async(activity.conversation.id, activity)

    async def receive(self, auth_header: str, activity: Activity):
        try:
            await JwtTokenValidation.assert_valid_activity(activity, auth_header, self._credential_provider)
        except BaseException as e:
            raise e
        else:
            if self.on_receive is not None:
                await self.on_receive(activity)
