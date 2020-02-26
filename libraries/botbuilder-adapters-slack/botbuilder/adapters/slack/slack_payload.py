# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import Optional, List

from botbuilder.adapters.slack.slack_message import SlackMessage

from slack.web.classes.actions import Action


class SlackPayload:
    def __init__(self, **kwargs):
        self.type: [str] = kwargs.get("type")
        self.token: str = kwargs.get("token")
        self.channel: str = kwargs.get("channel")
        self.thread_ts: str = kwargs.get("thread_ts")
        self.team: str = kwargs.get("team")
        self.user: str = kwargs.get("user")
        self.actions: Optional[List[Action]] = None

        if "message" in kwargs:
            message = kwargs.get("message")
            self.message = (
                message
                if isinstance(message) is SlackMessage
                else SlackMessage(**message)
            )
