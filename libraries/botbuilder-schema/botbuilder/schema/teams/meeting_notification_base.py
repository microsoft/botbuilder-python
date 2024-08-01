from dataclasses import dataclass, field
from typing import Optional
import json


@dataclass
class MeetingNotificationBase:
    """
    Specifies Bot meeting notification base including channel data and type.
    """

    type: Optional[str] = field(default=None)

    def to_json(self) -> str:
        """
        Converts the MeetingNotificationBase object to JSON.
        :return: JSON representation of the MeetingNotificationBase object.
        """
        return json.dumps(
            self,
            default=lambda o: {k: v for k, v in o.__dict__.items() if v is not None},
            sort_keys=True,
            indent=4,
        )
