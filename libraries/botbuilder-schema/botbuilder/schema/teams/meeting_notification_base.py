from typing import Optional
import json


class MeetingNotificationBase:
    """
    Specifies Bot meeting notification base including channel data and type.
    """

    def __init__(self, type: Optional[str] = None):
        self.type = type

    def to_json(self) -> str:
        """
        Converts the MeetingNotificationBase object to JSON.
        :return: JSON representation of the MeetingNotificationBase object.
        """
        return json.dumps(
            {
                "type": self.type
            },
            sort_keys=True,
            indent=4
        )
    