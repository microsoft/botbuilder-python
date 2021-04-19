# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
import json
from typing import List
from botbuilder.adapters.slack.slack_message import SlackMessage


class SlackPayload:
    def __init__(self, **kwargs):
        payload = json.loads(kwargs.get("payload"))

        self.type: List[str] = payload.get("type")
        self.token: str = payload.get("token")
        self.channel: str = payload.get("channel")
        self.thread_ts: str = payload.get("thread_ts")
        self.team: str = payload.get("team")
        self.user: str = payload.get("user")
        self.actions = payload.get("actions")
        self.trigger_id: str = payload.get("trigger_id")
        self.action_ts: str = payload.get("action_ts")
        self.submission: str = payload.get("submission")
        self.callback_id: str = payload.get("callback_id")
        self.state: str = payload.get("state")
        self.response_url: str = payload.get("response_url")

        if "message" in payload:
            message = payload.get("message")
            self.message = (
                message
                if isinstance(message, SlackMessage)
                else SlackMessage(**message)
            )
