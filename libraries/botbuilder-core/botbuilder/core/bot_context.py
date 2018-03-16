# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import asyncio
import sys
from copy import deepcopy, copy
from uuid import uuid4
from typing import List, Callable, Iterable, Tuple
from botbuilder.schema import Activity, ActivityTypes, ConversationReference, ResourceResponse

# from .bot_adapter import BotAdapter


class BotContext(object):
    def __init__(self, adapter, request: Activity):
        self.adapter = adapter
        self.request: Activity = request
        self.responses: List[Activity] = []
        self._services: dict = {}
        self._responded: bool = False
        self._on_send_activity: Callable[[]] = []
        self._on_update_activity: Callable[[]] = []
        self._on_delete_activity: Callable[[]] = []

        if not self.request:
            raise TypeError('BotContext must be instantiated with a request parameter of type Activity.')

    def get(self, key: str) -> object:
        if not key or not isinstance(key, str):
            raise TypeError('"key" must be a valid string.')
        try:
            return self._services[key]
        except KeyError:
            raise KeyError('%s not found in BotContext._services.' % key)

    def has(self, key: str) -> bool:
        """
        Returns True is set() has been called for a key. The cached value may be of type 'None'.
        :param key:
        :return:
        """
        if key in self._services:
            return True
        return False

    def set(self, key: str, value: object) -> None:
        """
        Caches a value for the lifetime of the current turn.
        :param key:
        :param value:
        :return:
        """
        if not key or not isinstance(key, str):
            raise KeyError('"key" must be a valid string.')

        self._services[key] = value

    async def send_activity(self, *activity_or_text: Tuple[Activity, str]):
        reference = BotContext.get_conversation_reference(self.request)
        output = [BotContext.apply_conversation_reference(
            Activity(text=a, type='message') if isinstance(a, str) else a, reference)
            for a in activity_or_text]

        async def callback(context: 'BotContext', output):
            responses = await context.adapter.send_activity(output)
            context._responded = True
            return responses

        await self._emit(self._on_send_activity, output, callback(self, output))

    async def update_activity(self, activity: Activity):
        return asyncio.ensure_future(self._emit(self._on_update_activity,
                                                activity,
                                                self.adapter.update_activity(activity)))

    @staticmethod
    async def _emit(plugins, arg, logic):
        handlers = copy(plugins)

        async def emit_next(i: int):
            try:
                if i < len(handlers):
                    await handlers[i](arg, emit_next(i + 1))
                asyncio.ensure_future(logic)
            except BaseException as e:
                raise e
        await emit_next(0)

    @staticmethod
    def get_conversation_reference(activity: Activity) -> ConversationReference:
        """
        Returns the conversation reference for an activity. This can be saved as a plain old JSON
        bject and then later used to message the user proactively.

        Usage Example:
        reference = BotContext.get_conversation_reference(context.request)
        :param activity:
        :return:
        """
        return ConversationReference(activity_id=activity.id,
                                     user=copy(activity.from_property),
                                     bot=copy(activity.recipient),
                                     conversation=copy(activity.conversation),
                                     channel_id=activity.channel_id,
                                     service_url=activity.service_url)

    @staticmethod
    def apply_conversation_reference(activity: Activity,
                                     reference: ConversationReference,
                                     is_incoming: bool=False) -> Activity:
        """
        Updates an activity with the delivery information from a conversation reference. Calling
        this after get_conversation_reference on an incoming activity
        will properly address the reply to a received activity.
        :param activity:
        :param reference:
        :param is_incoming:
        :return:
        """
        activity.channel_id=reference.channel_id
        activity.service_url=reference.service_url
        activity.conversation=reference.conversation
        if is_incoming:
            activity.from_property = reference.user
            activity.recipient = reference.bot
            if reference.activity_id:
                activity.id = reference.activity_id
        else:
            activity.from_property = reference.bot
            activity.recipient = reference.user
            if reference.activity_id:
                activity.reply_to_id = reference.activity_id

        return activity

