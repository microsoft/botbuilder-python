import json


class MeetingNotificationRecipientFailureInfo:
    recipient_mri: str
    error_code: str
    failure_reason: str

    def to_json(self):
        return json.dumps(
            {
                "recipientMri": self.recipient_mri,
                "errorcode": self.error_code,
                "failureReason": self.failure_reason,
            }
        )

    @staticmethod
    def from_json(json_str):
        data = json.loads(json_str)
        return MeetingNotificationRecipientFailureInfo(
            recipient_mri=data.get("recipientMri"),
            error_code=data.get("errorcode"),
            failure_reason=data.get("failureReason"),
        )
