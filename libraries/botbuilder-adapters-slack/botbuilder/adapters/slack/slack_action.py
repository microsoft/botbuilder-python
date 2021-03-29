from botbuilder.adapters.slack.slack_text import SlackText
from typing import Optional


# Slack action block (https://api.slack.com/reference/block-kit/block-elements)
class SlackAction:
    def __init__(self, **kwargs):
        self.action_id: str = kwargs.get("action_id")
        self.block_id: str = kwargs.get("block_id")
        self.value: str = kwargs.get("value")
        self.type: str = kwargs.get("type")
        self.action_ts: str = kwargs.get("action_ts")
        self.text: Optional[SlackText] = (
            None if "text" not in kwargs else SlackText(**(kwargs.get("text")))
        )
