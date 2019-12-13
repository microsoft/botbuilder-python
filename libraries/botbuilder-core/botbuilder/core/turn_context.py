# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import re
from copy import copy, deepcopy
from datetime import datetime
from typing import List, Callable, Union, Dict
from botbuilder.schema import (
    Activity,
    ActivityTypes,
    ConversationReference,
    InputHints,
    Mention,
    ResourceResponse,
)


class TurnContext:
    def __init__(self, adapter_or_context, request: Activity = None):
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
            self._on_send_activities: Callable[
                ["TurnContext", List[Activity], Callable], List[ResourceResponse]
            ] = []
            self._on_update_activity: Callable[
                ["TurnContext", Activity, Callable], ResourceResponse
            ] = []
            self._on_delete_activity: Callable[
                ["TurnContext", ConversationReference, Callable], None
            ] = []
            self._responded: bool = False

        if self.adapter is None:
            raise TypeError("TurnContext must be instantiated with an adapter.")
        if self.activity is None:
            raise TypeError(
                "TurnContext must be instantiated with a request parameter of type Activity."
            )

        self._turn_state = {}

    @property
    def turn_state(self) -> Dict[str, object]:
        return self._turn_state

    def copy_to(self, context: "TurnContext") -> None:
        """
        Called when this TurnContext instance is passed into the constructor of a new TurnContext
        instance. Can be overridden in derived classes.
        :param context:
        :return:
        """
        for attribute in [
            "adapter",
            "activity",
            "_responded",
            "_services",
            "_on_send_activities",
            "_on_update_activity",
            "_on_delete_activity",
        ]:
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
            raise TypeError(
                "TurnContext: cannot set `activity` to a type other than Activity."
            )
        self._activity = value

    @property
    def responded(self) -> bool:
        """
        If `true` at least one response has been sent for the current turn of conversation.
        :return:
        """
        return self._responded

    @responded.setter
    def responded(self, value: bool):
        if not value:
            raise ValueError("TurnContext: cannot set TurnContext.responded to False.")
        self._responded = True

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
            raise KeyError("%s not found in TurnContext._services." % key)

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

    async def send_activity(
        self,
        activity_or_text: Union[Activity, str],
        speak: str = None,
        input_hint: str = None,
    ) -> ResourceResponse:
        """
        Sends a single activity or message to the user.
        :param activity_or_text:
        :return:
        """
        if isinstance(activity_or_text, str):
            activity_or_text = Activity(
                text=activity_or_text,
                input_hint=input_hint or InputHints.accepting_input,
                speak=speak,
            )

        result = await self.send_activities([activity_or_text])
        return result[0] if result else None

    async def send_activities(
        self, activities: List[Activity]
    ) -> List[ResourceResponse]:
        sent_non_trace_activity = False
        ref = TurnContext.get_conversation_reference(self.activity)

        def activity_validator(activity: Activity) -> Activity:
            if not getattr(activity, "type", None):
                activity.type = ActivityTypes.message
            if activity.type != ActivityTypes.trace:
                nonlocal sent_non_trace_activity
                sent_non_trace_activity = True
            if not activity.input_hint:
                activity.input_hint = "acceptingInput"
            activity.id = None
            return activity

        output = [
            activity_validator(
                TurnContext.apply_conversation_reference(deepcopy(act), ref)
            )
            for act in activities
        ]

        async def logic():
            responses = await self.adapter.send_activities(self, output)
            if sent_non_trace_activity:
                self.responded = True
            return responses

        return await self._emit(self._on_send_activities, output, logic())

    async def update_activity(self, activity: Activity):
        """
        Replaces an existing activity.
        :param activity:
        :return:
        """
        reference = TurnContext.get_conversation_reference(self.activity)

        return await self._emit(
            self._on_update_activity,
            TurnContext.apply_conversation_reference(activity, reference),
            self.adapter.update_activity(self, activity),
        )

    async def delete_activity(self, id_or_reference: Union[str, ConversationReference]):
        """
        Deletes an existing activity.
        :param id_or_reference:
        :return:
        """
        if isinstance(id_or_reference, str):
            reference = TurnContext.get_conversation_reference(self.activity)
            reference.activity_id = id_or_reference
        else:
            reference = id_or_reference
        return await self._emit(
            self._on_delete_activity,
            reference,
            self.adapter.delete_activity(self, reference),
        )

    def on_send_activities(self, handler) -> "TurnContext":
        """
        Registers a handler to be notified of and potentially intercept the sending of activities.
        :param handler:
        :return:
        """
        self._on_send_activities.append(handler)
        return self

    def on_update_activity(self, handler) -> "TurnContext":
        """
        Registers a handler to be notified of and potentially intercept an activity being updated.
        :param handler:
        :return:
        """
        self._on_update_activity.append(handler)
        return self

    def on_delete_activity(self, handler) -> "TurnContext":
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

            except Exception as error:
                raise error

        await emit_next(0)
        # logic does not use parentheses because it's a coroutine
        return await logic

    async def send_trace_activity(
        self, name: str, value: object, value_type: str, label: str
    ) -> ResourceResponse:
        trace_activity = Activity(
            type=ActivityTypes.trace,
            timestamp=datetime.utcnow(),
            name=name,
            value=value,
            value_type=value_type,
            label=label,
        )

        return await self.send_activity(trace_activity)

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
        return ConversationReference(
            activity_id=activity.id,
            user=copy(activity.from_property),
            bot=copy(activity.recipient),
            conversation=copy(activity.conversation),
            channel_id=activity.channel_id,
            service_url=activity.service_url,
        )

    @staticmethod
    def apply_conversation_reference(
        activity: Activity, reference: ConversationReference, is_incoming: bool = False
    ) -> Activity:
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

    @staticmethod
    def get_reply_conversation_reference(
        activity: Activity, reply: ResourceResponse
    ) -> ConversationReference:
        reference: ConversationReference = TurnContext.get_conversation_reference(
            activity
        )

        # Update the reference with the new outgoing Activity's id.
        reference.activity_id = reply.id

        return reference

    @staticmethod
    def remove_recipient_mention(activity: Activity) -> str:
        return TurnContext.remove_mention_text(activity, activity.recipient.id)

    @staticmethod
    def remove_mention_text(activity: Activity, identifier: str) -> str:
        mentions = TurnContext.get_mentions(activity)
        for mention in mentions:
            if mention.additional_properties["mentioned"]["id"] == identifier:
                mention_name_match = re.match(
                    r"<at(.*)>(.*?)<\/at>",
                    mention.additional_properties["text"],
                    re.IGNORECASE,
                )
                if mention_name_match:
                    activity.text = re.sub(
                        mention_name_match.groups()[1], "", activity.text
                    )
                    activity.text = re.sub(r"<at><\/at>", "", activity.text)
        return activity.text

    @staticmethod
    def get_mentions(activity: Activity) -> List[Mention]:
        result: List[Mention] = []
        if activity.entities is not None:
            for entity in activity.entities:
                if entity.type.lower() == "mention":
                    result.append(entity)

        return result
