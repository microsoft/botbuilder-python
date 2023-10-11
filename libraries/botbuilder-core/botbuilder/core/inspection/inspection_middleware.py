# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from uuid import uuid4
from typing import Any, List

from jsonpickle import Pickler
from botbuilder.core import BotState, ConversationState, TurnContext, UserState
from botbuilder.schema import Activity, ActivityTypes, ConversationReference
from botframework.connector.auth import MicrosoftAppCredentials

from .inspection_session import InspectionSession
from .inspection_sessions_by_status import (
    InspectionSessionsByStatus,
    DEFAULT_INSPECTION_SESSIONS_BY_STATUS,
)
from .inspection_state import InspectionState
from .interception_middleware import InterceptionMiddleware
from .trace_activity import from_state, make_command_activity


class InspectionMiddleware(InterceptionMiddleware):
    _COMMAND = "/INSPECT"

    def __init__(  # pylint: disable=super-init-not-called
        self,
        inspection_state: InspectionState,
        user_state: UserState = None,
        conversation_state: ConversationState = None,
        credentials: MicrosoftAppCredentials = None,
    ):
        self.inspection_state = inspection_state
        self.inspection_state_accessor = inspection_state.create_property(
            "InspectionSessionByStatus"
        )
        self.user_state = user_state
        self.conversation_state = conversation_state
        self.credentials = MicrosoftAppCredentials(
            credentials.microsoft_app_id if credentials else "",
            credentials.microsoft_app_password if credentials else "",
        )

    async def process_command(self, context: TurnContext) -> Any:
        if context.activity.type == ActivityTypes.message and context.activity.text:
            original_text = context.activity.text
            TurnContext.remove_recipient_mention(context.activity)

            command = context.activity.text.strip().split(" ")
            if len(command) > 1 and command[0] == InspectionMiddleware._COMMAND:
                if len(command) == 2 and command[1] == "open":
                    await self._process_open_command(context)
                    return True

                if len(command) == 3 and command[1] == "attach":
                    await self.process_attach_command(context, command[2])
                    return True

            context.activity.text = original_text

        return False

    async def _inbound(self, context: TurnContext, trace_activity: Activity) -> Any:
        if await self.process_command(context):
            return False, False

        session = await self._find_session(context)
        if session:
            if await self._invoke_send(context, session, trace_activity):
                return True, True
        return True, False

    async def _outbound(
        self, context: TurnContext, trace_activities: List[Activity]
    ) -> Any:
        session = await self._find_session(context)
        if session:
            for trace_activity in trace_activities:
                if not await self._invoke_send(context, session, trace_activity):
                    break

    async def _trace_state(self, context: TurnContext) -> Any:
        session = await self._find_session(context)
        if session:
            if self.user_state:
                await self.user_state.load(context, False)

            if self.conversation_state:
                await self.conversation_state.load(context, False)

            bot_state = {}

            if self.user_state:
                bot_state["user_state"] = InspectionMiddleware._get_serialized_context(
                    self.user_state, context
                )

            if self.conversation_state:
                bot_state[
                    "conversation_state"
                ] = InspectionMiddleware._get_serialized_context(
                    self.conversation_state, context
                )

            await self._invoke_send(context, session, from_state(bot_state))

    async def _process_open_command(self, context: TurnContext) -> Any:
        sessions = await self.inspection_state_accessor.get(
            context, DEFAULT_INSPECTION_SESSIONS_BY_STATUS
        )
        session_id = self._open_command(
            sessions, TurnContext.get_conversation_reference(context.activity)
        )
        await context.send_activity(
            make_command_activity(
                f"{InspectionMiddleware._COMMAND} attach {session_id}"
            )
        )
        await self.inspection_state.save_changes(context, False)

    async def process_attach_command(
        self, context: TurnContext, session_id: str
    ) -> None:
        sessions = await self.inspection_state_accessor.get(
            context, DEFAULT_INSPECTION_SESSIONS_BY_STATUS
        )

        if self._attach_comamnd(context.activity.conversation.id, sessions, session_id):
            await context.send_activity(
                "Attached to session, all traffic is being replicated for inspection."
            )
        else:
            await context.send_activity(
                f"Open session with id {session_id} does not exist."
            )

        await self.inspection_state.save_changes(context, False)

    def _open_command(
        self,
        sessions: InspectionSessionsByStatus,
        conversation_reference: ConversationReference,
    ) -> str:
        session_id = str(uuid4())
        sessions.opened_sessions[session_id] = conversation_reference
        return session_id

    def _attach_comamnd(
        self,
        conversation_id: str,
        sessions: InspectionSessionsByStatus,
        session_id: str,
    ) -> bool:
        inspection_session_state = sessions.opened_sessions.get(session_id)
        if inspection_session_state:
            sessions.attached_sessions[conversation_id] = inspection_session_state
            del sessions.opened_sessions[session_id]
            return True

        return False

    @staticmethod
    def _get_serialized_context(state: BotState, context: TurnContext):
        ctx = state.get(context)
        return Pickler(unpicklable=False).flatten(ctx)

    async def _find_session(self, context: TurnContext) -> Any:
        sessions = await self.inspection_state_accessor.get(
            context, DEFAULT_INSPECTION_SESSIONS_BY_STATUS
        )

        conversation_reference = sessions.attached_sessions.get(
            context.activity.conversation.id
        )
        if conversation_reference:
            return InspectionSession(conversation_reference, self.credentials)

        return None

    async def _invoke_send(
        self, context: TurnContext, session: InspectionSession, activity: Activity
    ) -> bool:
        if await session.send(activity):
            return True

        await self._clean_up_session(context)
        return False

    async def _clean_up_session(self, context: TurnContext) -> None:
        sessions = await self.inspection_state_accessor.get(
            context, DEFAULT_INSPECTION_SESSIONS_BY_STATUS
        )

        del sessions.attached_sessions[context.activity.conversation.id]
        await self.inspection_state.save_changes(context, False)
