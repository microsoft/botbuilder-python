from dataclasses import dataclass, field
from typing import Optional
import json
from .meeting_notification import MeetingNotification
from .targeted_meeting_notification_value import TargetedMeetingNotificationValue
from .meeting_notification_channel_data import MeetingNotificationChannelData


@dataclass
class TargetedMeetingNotification(
    MeetingNotification[TargetedMeetingNotificationValue]
):
    """
    Specifies Teams targeted meeting notification.
    """
    value: Optional[TargetedMeetingNotificationValue] = field(
        default=None, metadata={"json": "value"}
    )
    channel_data: Optional[MeetingNotificationChannelData] = field(
        default=None, metadata={"json": "channelData"}
    )

    def to_json(self) -> str:
        """
        Converts the TargetedMeetingNotification object to JSON.
        :return: JSON representation of the TargetedMeetingNotification object.
        """
        return json.dumps(
            self,
            default=lambda o: {k: v for k, v in o.__dict__.items() if v is not None},
            sort_keys=True,
            indent=4,
        )
    