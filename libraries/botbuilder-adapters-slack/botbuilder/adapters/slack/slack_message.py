# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from slack.web.classes.attachments import Attachment
from slack.web.classes.blocks import Block


class SlackMessage:
    def __init__(self, **kwargs):
        self.ephemeral = kwargs.get("ephemeral")
        self.as_user = kwargs.get("as_user")
        self.icon_url = kwargs.get("icon_url")
        self.icon_emoji = kwargs.get("icon_emoji")
        self.thread_ts = kwargs.get("thread_ts")
        self.user = kwargs.get("user")
        self.channel = kwargs.get("channel")
        self.text = kwargs.get("text")
        self.team = kwargs.get("team")
        self.ts = kwargs.get("ts")  # pylint: disable=invalid-name
        self.username = kwargs.get("username")
        self.bot_id = kwargs.get("bot_id")
        self.icons = kwargs.get("icons")
        self.blocks: [Block] = kwargs.get("blocks")

        # Create proper Attachment objects
        # It would appear that we can get dict fields from the wire that aren't defined
        # in the Attachment class.  So only pass in known fields.
        attachments = kwargs.get("attachments")
        if attachments is not None:
            self.attachments = [
                Attachment(**{x: att[x] for x in att if x in Attachment.attributes})
                for att in kwargs.get("attachments")
            ]
