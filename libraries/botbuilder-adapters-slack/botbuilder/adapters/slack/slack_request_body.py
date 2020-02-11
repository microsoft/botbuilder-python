# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.adapters.slack.slack_event import SlackEvent
from botbuilder.adapters.slack.slack_payload import SlackPayload


class SlackRequestBody:
    def __init__(self, **kwargs):
        self.challenge = kwargs.get("challenge")
        self.token = kwargs.get("token")
        self.team_id = kwargs.get("team_id")
        self.api_app_id = kwargs.get("api_app_id")
        self.type = kwargs.get("type")
        self.event_id = kwargs.get("event_id")
        self.event_time = kwargs.get("event_time")
        self.authed_users: [str] = kwargs.get("authed_users")
        self.trigger_id = kwargs.get("trigger_id")
        self.channel_id = kwargs.get("channel_id")
        self.user_id = kwargs.get("user_id")
        self.text = kwargs.get("text")
        self.command = kwargs.get("command")

        self.payload: SlackPayload = None
        if "payload" in kwargs:
            payload = kwargs.get("payload")
            self.payload = (
                payload
                if isinstance(payload, SlackPayload)
                else SlackPayload(**payload)
            )

        self.event: SlackEvent = None
        if "event" in kwargs:
            event = kwargs.get("event")
            self.event = event if isinstance(event, SlackEvent) else SlackEvent(**event)
