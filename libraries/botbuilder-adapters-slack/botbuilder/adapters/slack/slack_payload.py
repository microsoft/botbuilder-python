# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import Optional, List
from slack.web.classes.actions import Action
from botbuilder.adapters.slack.slack_message import SlackMessage


class SlackPayload:
    def __init__(self, **kwargs):
        self.type: List[str] = kwargs.get("type")
        self.token: str = kwargs.get("token")
        self.channel: str = kwargs.get("channel")
        self.thread_ts: str = kwargs.get("thread_ts")
        self.team: str = kwargs.get("team")
        self.user: str = kwargs.get("user")
        self.actions: Optional[List[Action]] = None
        self.trigger_id: str = kwargs.get("trigger_id")
        self.action_ts: str = kwargs.get("action_ts")
        self.submission: str = kwargs.get("submission")
        self.callback_id: str = kwargs.get("callback_id")
        self.state: str = kwargs.get("state")
        self.response_url: str = kwargs.get("response_url")

        if "message" in kwargs:
            message = kwargs.get("message")
            self.message = (
                message
                if isinstance(message) is SlackMessage
                else SlackMessage(**message)
            )
