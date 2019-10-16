# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import json
import logging
import time
import uuid
from datetime import datetime
from typing import Awaitable, Callable, List

from botbuilder.core import Middleware, TurnContext
from botbuilder.schema import Activity, ActivityTypes, ResourceResponse


class DialogTestLogger(Middleware):
    """
    A middleware to output incoming and outgoing activities as json strings to the console during
    unit tests.
    """

    def __init__(
        self,
        log_func: Callable[..., None] = None,
        json_indent: int = 4,
        time_func: Callable[[], float] = None,
    ):
        """
        Initialize a new instance of the dialog test logger.

        :param log_func: A callable method or object that can log a message,
        default to `logging.getLogger(__name__).info`.
        :type log_func: Callable[..., None]
        :param json_indent: An indent for json output, default indent is 4.
        :type json_indent: int
        :param time_func: A time function to record time spans, default to `time.monotonic`.
        :type time_func: Callable[[], float]
        """
        self._log = logging.getLogger(__name__).info if log_func is None else log_func
        self._stopwatch_state_key = f"stopwatch.{uuid.uuid4()}"
        self._json_indent = json_indent
        self._time_func = time.monotonic if time_func is None else time_func

    async def on_turn(
        self, context: TurnContext, logic: Callable[[TurnContext], Awaitable]
    ):
        context.turn_state[self._stopwatch_state_key] = self._time_func()
        await self._log_incoming_activity(context, context.activity)
        context.on_send_activities(self._send_activities_handler)
        await logic()

    async def _log_incoming_activity(
        self, context: TurnContext, activity: Activity
    ) -> None:
        self._log("")
        if context.activity.type == ActivityTypes.message:
            self._log("User: Text = %s", context.activity.text)
        else:
            self._log_activity_as_json(actor="User", activity=activity)

        timestamp = self._get_timestamp()
        self._log("-> ts: %s", timestamp)

    async def _send_activities_handler(
        self,
        context: TurnContext,
        activities: List[Activity],
        next_send: Callable[[], Awaitable[None]],
    ) -> List[ResourceResponse]:
        for activity in activities:
            await self._log_outgoing_activity(context, activity)
        responses = await next_send()
        return responses

    async def _log_outgoing_activity(
        self, context: TurnContext, activity: Activity
    ) -> None:
        self._log("")
        start_time = context.turn_state[self._stopwatch_state_key]
        if activity.type == ActivityTypes.message:
            message = (
                f"Bot: Text      = {activity.text}\r\n"
                f"     Speak     = {activity.speak}\r\n"
                f"     InputHint = {activity.input_hint}"
            )
            self._log(message)
        else:
            self._log_activity_as_json(actor="Bot", activity=activity)

        now = self._time_func()
        mms = int(round((now - start_time) * 1000))
        timestamp = self._get_timestamp()
        self._log("-> ts: %s elapsed %d ms", timestamp, mms)

    def _log_activity_as_json(self, actor: str, activity: Activity) -> None:
        activity_dict = activity.serialize()
        activity_json = json.dumps(activity_dict, indent=self._json_indent)
        message = f"{actor}: Activity = {activity.type}\r\n" f"{activity_json}"
        self._log(message)

    @staticmethod
    def _get_timestamp() -> str:
        timestamp = datetime.now().strftime("%H:%M:%S")
        return timestamp
