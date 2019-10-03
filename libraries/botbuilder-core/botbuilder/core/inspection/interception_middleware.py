# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from abc import abstractmethod
from typing import Any, Awaitable, Callable, List

from botbuilder.core import Middleware, TurnContext
from botbuilder.schema import Activity, ConversationReference

from .trace_activity import from_activity, from_conversation_reference, from_error


class InterceptionMiddleware(Middleware):
    async def on_turn(
        self, context: TurnContext, logic: Callable[[TurnContext], Awaitable]
    ):
        should_forward_to_application, should_intercept = await self._invoke_inbound(
            context,
            from_activity(context.activity, "ReceivedActivity", "Received Activity"),
        )

        if should_intercept:

            async def aux_on_send(
                ctx: TurnContext, activities: List[Activity], next_send: Callable
            ):
                trace_activities = [
                    from_activity(activity, "SentActivity", "Sent Activity")
                    for activity in activities
                ]
                await self._invoke_outbound(ctx, trace_activities)
                return await next_send()

            async def aux_on_update(
                ctx: TurnContext, activity: Activity, next_update: Callable
            ):
                trace_activity = from_activity(
                    activity, "MessageUpdate", "Updated Message"
                )
                await self._invoke_outbound(ctx, [trace_activity])
                return await next_update()

            async def aux_on_delete(
                ctx: TurnContext,
                reference: ConversationReference,
                next_delete: Callable,
            ):
                trace_activity = from_conversation_reference(reference)
                await self._invoke_outbound(ctx, [trace_activity])
                return await next_delete()

            context.on_send_activities(aux_on_send)
            context.on_update_activity(aux_on_update)
            context.on_delete_activity(aux_on_delete)

        if should_forward_to_application:
            try:
                await logic()
            except Exception as err:
                trace_activity = from_error(str(err))
                await self._invoke_outbound(context, [trace_activity])
                raise err

        if should_intercept:
            await self._invoke_trace_state(context)

    @abstractmethod
    async def _inbound(self, context: TurnContext, trace_activity: Activity) -> Any:
        raise NotImplementedError()

    @abstractmethod
    async def _outbound(
        self, context: TurnContext, trace_activities: List[Activity]
    ) -> Any:
        raise NotImplementedError()

    @abstractmethod
    async def _trace_state(self, context: TurnContext) -> Any:
        raise NotImplementedError()

    async def _invoke_inbound(
        self, context: TurnContext, trace_activity: Activity
    ) -> Any:
        try:
            return await self._inbound(context, trace_activity)
        except Exception as err:
            print(f"Exception in inbound interception {str(err)}")
            return True, False

    async def _invoke_outbound(
        self, context: TurnContext, trace_activities: List[Activity]
    ) -> Any:
        try:
            return await self._outbound(context, trace_activities)
        except Exception as err:
            print(f"Exception in outbound interception {str(err)}")

    async def _invoke_trace_state(self, context: TurnContext) -> Any:
        try:
            return await self._trace_state(context)
        except Exception as err:
            print(f"Exception in state interception {str(err)}")
