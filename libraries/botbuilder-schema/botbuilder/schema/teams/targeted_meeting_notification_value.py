from typing import List, Optional
import json
from .surface import Surface


class TargetedMeetingNotificationValue:
    """
    Specifies the targeted meeting notification value, including recipients and surfaces.
    """

    def __init__(
        self,
        recipients: Optional[List[str]] = None,
        surfaces: Optional[List[Surface]] = None,
    ):
        self.recipients = recipients if recipients is not None else []
        self.surfaces = surfaces if surfaces is not None else []

    def to_json(self) -> str:
        """
        Converts the TargetedMeetingNotificationValue object to JSON.
        :return: JSON representation of the TargetedMeetingNotificationValue object.
        """
        return json.dumps(
            {
                "recipients": self.recipients,
                "surfaces": [surface.to_dict() for surface in self.surfaces],
            },
            sort_keys=True,
            indent=4,
        )
