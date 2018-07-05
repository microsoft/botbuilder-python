# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import asyncio
from copy import copy
from uuid import uuid4
from typing import List, Callable, Union
from botbuilder.schema import Activity, ConversationReference, ResourceResponse


class TurnContext(object):
    def __init__(self, adapter_or_context, request: Activity=None):
        """
        Creates a new TurnContext instance.
        :param adapter_or_context:
        :param request:
        """
        if isinstance(adapter_or_context, TurnContext):
            adapter_or_context.copy_to(self)
        else:
            self.adapter = adapter_or_context
            self._activity = request
            self.responses: List[Activity] = []
            self._services: dict = {}
            self._on_send_activities: Callable[[]] = []
            self._on_update_activity: Callable[[]] = []
            self._on_delete_activity: Callable[[]] = []
            self._responded = {'responded': False}

        if self.adapter is None:
            raise TypeError('TurnContext must be instantiated with an adapter.')
        if self.activity is None:
            raise TypeError('TurnContext must be instantiated with a request parameter of type Activity.')

    def copy_to(self, context: 'TurnContext') -> None:
        """
        Called when this TurnContext instance is passed into the constructor of a new TurnContext
        instance. Can be overridden in derived classes.
        :param context:
        :return:
        """
        for attribute in ['adapter', 'activity', '_responded', '_services',
                          '_on_send_activities', '_on_update_activity', '_on_delete_activity']:
            setattr(context, attribute, getattr(self, attribute))

    @property
    def activity(self):
        """
        The received activity.
        :return:
        """
        return self._activity

    @activity.setter
    def activity(self, value):
        """
        Used to set TurnContext._activity when a context object is created. Only takes instances of Activities.
        :param value:
        :return:
        """
        if not isinstance(value, Activity):
            raise TypeError('TurnContext: cannot set `activity` to a type other than Activity.')
        else:
            self._activity = value

    @property
    def responded(self):
        """
        If `true` at least one response has been sent for the current turn of conversation.
        :return:
        """
        return self._responded['responded']

    @responded.setter
    def responded(self, value):
        if not value:
            raise ValueError('TurnContext: cannot set TurnContext.responded to False.')
        else:
            self._responded['responded'] = True

    @property
    def services(self):
        """
        Map of services and other values cached for the lifetime of the turn.
        :return:
        """
        return self._services

    def get(self, key: str) -> object:
        if not key or not isinstance(key, str):
            raise TypeError('"key" must be a valid string.')
        try:
            return self._services[key]
        except KeyError:
            raise KeyError('%s not found in TurnContext._services.' % key)

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

    async def send_activity(self, *activity_or_text: Union[Activity, str]) -> ResourceResponse:
        """
        Sends a single activity or message to the user.
        :param activity_or_text:
        :return:
        """
        reference = TurnContext.get_conversation_reference(self.activity)
        output = [TurnContext.apply_conversation_reference(
            Activity(text=a, type='message') if isinstance(a, str) else a, reference)
            for a in activity_or_text]
        for activity in output:
            activity.input_hint = 'acceptingInput'

        async def callback(context: 'TurnContext', output):
            responses = await context.adapter.send_activities(context, output)
            context._responded = True
            return responses

        await self._emit(self._on_send_activities, output, callback(self, output))

    async def update_activity(self, activity: Activity):
        """
        Replaces an existing activity.
        :param activity:
        :return:
        """
        return await self._emit(self._on_update_activity, activity, self.adapter.update_activity(self, activity))

    async def delete_activity(self, id_or_reference: Union[str, ConversationReference]):
        """
        Deletes an existing activity.
        :param id_or_reference:
        :return:
        """
        if type(id_or_reference) == str:
            reference = TurnContext.get_conversation_reference(self.activity)
            reference.activity_id = id_or_reference
        else:
            reference = id_or_reference
        return await self._emit(self._on_delete_activity, reference, self.adapter.delete_activity(self, reference))

    def on_send_activities(self, handler) -> 'TurnContext':
        """
        Registers a handler to be notified of and potentially intercept the sending of activities.
        :param handler:
        :return:
        """
        self._on_send_activities.append(handler)
        return self

    def on_update_activity(self, handler) -> 'TurnContext':
        """
        Registers a handler to be notified of and potentially intercept an activity being updated.
        :param handler:
        :return:
        """
        self._on_update_activity.append(handler)
        return self

    def on_delete_activity(self, handler) -> 'TurnContext':
        """
        Registers a handler to be notified of and potentially intercept an activity being deleted.
        :param handler:
        :return:
        """
        self._on_delete_activity.append(handler)
        return self

    async def _emit(self, plugins, arg, logic):
        handlers = copy(plugins)

        async def emit_next(i: int):
            context = self
            try:
                if i < len(handlers):
                    async def next_handler():
                        await emit_next(i + 1)
                    await handlers[i](context, arg, next_handler)

            except Exception as e:
                raise e
        await emit_next(0)
        # This should be changed to `return await logic()`
        return await logic

    @staticmethod
    def get_conversation_reference(activity: Activity) -> ConversationReference:
        """
        Returns the conversation reference for an activity. This can be saved as a plain old JSON
        object and then later used to message the user proactively.

        Usage Example:
        reference = TurnContext.get_conversation_reference(context.request)
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
        activity.channel_id = reference.channel_id
        activity.service_url = reference.service_url
        activity.conversation = reference.conversation
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
