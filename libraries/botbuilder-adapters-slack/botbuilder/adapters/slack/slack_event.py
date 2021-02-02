# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import List
from botbuilder.adapters.slack.slack_message import SlackMessage


class SlackEvent:
    """
    Wrapper class for an incoming slack event.
    """

    def __init__(self, **kwargs):
        self.client_msg_id = kwargs.get("client_msg_id")
        self.type = kwargs.get("type")
        self.subtype = kwargs.get("subtype")
        self.text = kwargs.get("text")
        self.ts = kwargs.get("ts")  # pylint: disable=invalid-name
        self.team = kwargs.get("team")
        self.channel = kwargs.get("channel")
        self.channel_id = kwargs.get("channel_id")
        self.event_ts = kwargs.get("event_ts")
        self.channel_type = kwargs.get("channel_type")
        self.thread_ts = kwargs.get("thread_ts")
        self.user = kwargs.get("user")
        self.user_id = kwargs.get("user_id")
        self.bot_id = kwargs.get("bot_id")
        self.actions: List[str] = kwargs.get("actions")
        self.item = kwargs.get("item")
        self.item_channel = kwargs.get("item_channel")
        self.files: [] = kwargs.get("files")
        self.message = (
            None if "message" not in kwargs else SlackMessage(**kwargs.get("message"))
        )
