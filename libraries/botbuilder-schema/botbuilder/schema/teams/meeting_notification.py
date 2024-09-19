from typing import Optional, TypeVar, Generic
import json
from .meeting_notification_base import MeetingNotificationBase

T = TypeVar("T")


class MeetingNotification(Generic[T], MeetingNotificationBase):
    """
    Specifies Bot meeting notification including meeting notification value.
    """

    def __init__(self, value: Optional[T] = None, type: Optional[str] = None):
        super().__init__(type=type)
        self.value = value

    def to_json(self) -> str:
        """
        Converts the MeetingNotification object to JSON.
        :return: JSON representation of the MeetingNotification object.
        """
        value_dict = (
            self.value.to_dict()
            if self.value and hasattr(self.value, "to_dict")
            else self.value
        )
        return json.dumps(
            {"type": self.type, "value": value_dict}, sort_keys=True, indent=4
        )
