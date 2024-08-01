from dataclasses import dataclass, field
from typing import List
import json
from .surface import Surface


@dataclass
class TargetedMeetingNotificationValue:
    """
    Specifies the targeted meeting notification value, including recipients and surfaces.
    """

    recipients: List[str] = field(default_factory=list, metadata={"json": "recipients"})
    surfaces: List[Surface] = field(default_factory=list, metadata={"json": "surfaces"})

    def to_json(self) -> str:
        """
        Converts the TargetedMeetingNotificationValue object to JSON.
        :return: JSON representation of the TargetedMeetingNotificationValue object.
        """
        return json.dumps(
            self,
            default=lambda o: {k: v for k, v in o.__dict__.items() if v is not None},
            sort_keys=True,
            indent=4,
        )
