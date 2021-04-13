# Slack text object (https://api.slack.com/reference/block-kit/composition-objects#text)
class SlackText:
    def __init__(self, **kwargs):
        self.text: str = kwargs.get("text")
        self.type: str = kwargs.get("type")
        self.emoji: bool = kwargs.get("emoji")
        self.verbatim: bool = kwargs.get("varbatim")
