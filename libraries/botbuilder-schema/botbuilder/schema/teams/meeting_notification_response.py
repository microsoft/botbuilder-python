import json
from typing import List

from botbuilder.schema.teams.meeting_notification_recipient_failure_info import (
    MeetingNotificationRecipientFailureInfo,
)


class MeetingNotificationResponse:
    def __init__(self):
        self.recipients_failure_info: List[MeetingNotificationRecipientFailureInfo] = []

    @property
    def recipients_failure_info(self) -> List[MeetingNotificationRecipientFailureInfo]:
        return self._recipients_failure_info

    @recipients_failure_info.setter
    def recipients_failure_info(
        self, value: List[MeetingNotificationRecipientFailureInfo]
    ):
        self._recipients_failure_info = value
