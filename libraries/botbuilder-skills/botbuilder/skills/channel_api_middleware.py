# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import uuid
from typing import Callable, Awaitable

from botbuilder.core import BotFrameworkAdapter, Middleware, TurnContext
from botbuilder.schema import Activity, ActivityTypes, ResourceResponse
from .channel_api_args import ChannelApiArgs
from .channel_api_methods import ChannelApiMethods
from .skill_host_adapter import SkillHostAdapter


class ChannelApiMiddleware(Middleware):
    def __init__(self, skill_adapter: SkillHostAdapter):
        self._skill_adapter = skill_adapter

    async def on_turn(
        self, context: TurnContext, logic: Callable[[TurnContext], Awaitable]
    ):
        # register the  skill adapter
        context.turn_state[self._skill_adapter.__class__.__name__] = self._skill_adapter

        if (
            context.activity.type == ActivityTypes.invoke
            and context.activity.name == SkillHostAdapter.INVOKE_ACTIVITY_NAME
        ):
            # process invoke activity TODO: (implement next 2 lines)
            invoke_activity = context.activity.as_invoke_activity()
            invoke_args: ChannelApiArgs = invoke_activity.value

            await self.call_channel_api(context, logic, invoke_args)
        else:
            await logic()

    @staticmethod
    async def _process_end_of_conversation(
        context: TurnContext,
        logic: Callable[[TurnContext], Awaitable],
        activity_payload: Activity,
    ):
        end_of_conversation = activity_payload.as_end_of_conversation_activity()
        context.activity.type = end_of_conversation.type
        context.activity.text = end_of_conversation.text
        context.activity.code = end_of_conversation.code
        context.activity.entities = end_of_conversation.entities
        context.activity.local_timestamp = end_of_conversation.local_timestamp
        context.activity.timestamp = end_of_conversation.timestamp
        context.activity.value = activity_payload.value
        context.activity.channel_data = end_of_conversation.channel_data
        # TODO: these properties are in extensions so currently they doesnt exist
        context.activity.properties = end_of_conversation.properties

        await logic()

    async def _call_chanel_api(
        self,
        context: TurnContext,
        logic: Callable[[TurnContext], Awaitable],
        invoke_args: ChannelApiArgs,
    ):
        try:
            adapter: BotFrameworkAdapter = context.adapter

            if invoke_args.method == ChannelApiMethods.SEND_TO_CONVERSATION:
                activity_payload: Activity = invoke_args.args[0]
                if activity_payload.type == ActivityTypes.end_of_conversation:
                    await ChannelApiMiddleware._process_end_of_conversation(
                        context, logic, activity_payload
                    )
                    invoke_args.result = ResourceResponse(id=uuid.uuid4().hex)
                    return

                invoke_args.result = await context.send_activity(activity_payload)
                return

            elif invoke_args.method == ChannelApiMethods.REPLY_TO_ACTIVITY:
                activity_payload: Activity = invoke_args.args[1]
                activity_payload.reply_to_id = invoke_args[0]

                if activity_payload.type == ActivityTypes.end_of_conversation:
                    await ChannelApiMiddleware._process_end_of_conversation(
                        context, logic, activity_payload
                    )
                    invoke_args.result = ResourceResponse(id=uuid.uuid4().hex)
                    return

                invoke_args.result = await context.send_activity(activity_payload)
                return

            elif invoke_args.method == ChannelApiMethods.UPDATE_ACTIVITY:
                invoke_args.result = await context.update_activity(invoke_args.args[0])
                return

            elif invoke_args.method == ChannelApiMethods.DELETE_ACTIVITY:
                invoke_args.result = await context.delete_activity(invoke_args[0])

            elif invoke_args == ChannelApiMethods.SEND_CONVERSATION_HISTORY:
                raise NotImplementedError(
                    f"{ChannelApiMethods.SEND_CONVERSATION_HISTORY} is not supported"
                )

            elif invoke_args == ChannelApiMethods.GET_CONVERSATION_MEMBERS:
                if adapter:
                    invoke_args.result = await adapter.get_conversation_members(context)

            elif invoke_args == ChannelApiMethods.GET_CONVERSATION_PAGED_MEMBERS:
                raise NotImplementedError(
                    f"{ChannelApiMethods.GET_CONVERSATION_PAGED_MEMBERS} is not supported"
                )

            elif invoke_args == ChannelApiMethods.DELETE_CONVERSATION_MEMBER:
                if adapter:
                    invoke_args.result = await adapter.delete_conversation_member(
                        context, invoke_args[0]
                    )

            elif invoke_args == ChannelApiMethods.GET_ACTIVITY_MEMBERS:
                if adapter:
                    invoke_args.result = await adapter.get_activity_members(
                        context, invoke_args[0]
                    )

            elif invoke_args == ChannelApiMethods.UPLOAD_ATTACHMENT:
                raise NotImplementedError(
                    f"{ChannelApiMethods.UPLOAD_ATTACHMENT} is not supported"
                )

        except Exception as exp:
            invoke_args.exception = exp
