from typing import Optional
import json
from .meeting_notification import MeetingNotification
from .targeted_meeting_notification_value import TargetedMeetingNotificationValue
from .meeting_notification_channel_data import MeetingNotificationChannelData


class TargetedMeetingNotification(
    MeetingNotification[TargetedMeetingNotificationValue]
):
    """
    Specifies Teams targeted meeting notification.
    """

    def __init__(
        self,
        value: Optional[TargetedMeetingNotificationValue] = None,
        channel_data: Optional[MeetingNotificationChannelData] = None,
        type: Optional[str] = None
    ):
        super().__init__(value=value, type=type)
        self.channel_data = channel_data

    def to_json(self) -> str:
        """
        Converts the TargetedMeetingNotification object to JSON.
        :return: JSON representation of the TargetedMeetingNotification object.
        """
        return json.dumps(
            {
                "type": self.type,
                "value": self.value.to_dict() if self.value else None,
                "channelData": (
                    self.channel_data.to_dict() if self.channel_data else None
                ),
            },
            sort_keys=True,
            indent=4,
        )
