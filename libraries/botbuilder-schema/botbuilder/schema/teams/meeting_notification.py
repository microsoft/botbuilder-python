from dataclasses import dataclass, field
from typing import Optional, TypeVar, Generic
import json
from .meeting_notification_base import MeetingNotificationBase

T = TypeVar("T")


@dataclass
class MeetingNotification(Generic[T], MeetingNotificationBase):
    """
    Specifies Bot meeting notification including meeting notification value.
    """

    value: Optional[T] = field(default=None, metadata={"json": "value"})

    def to_json(self) -> str:
        """
        Converts the MeetingNotification object to JSON.
        :return: JSON representation of the MeetingNotification object.
        """
        return json.dumps(
            self,
            default=lambda o: {k: v for k, v in o.__dict__.items() if v is not None},
            sort_keys=True,
            indent=4,
        )
