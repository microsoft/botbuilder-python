import json
from typing import List, Optional
from .on_behalf_of import OnBehalfOf


class MeetingNotificationChannelData:
    """
    Specify Teams Bot meeting notification channel data.
    """

    def __init__(self, on_behalf_of_list: Optional[List[OnBehalfOf]] = None):
        self.on_behalf_of_list = (
            on_behalf_of_list if on_behalf_of_list is not None else []
        )

    def to_json(self) -> str:
        """
        Converts the MeetingNotificationChannelData object to JSON.

        :return: JSON representation of the MeetingNotificationChannelData object.
        """
        return json.dumps(
            {"OnBehalfOf": [item.to_dict() for item in self.on_behalf_of_list]},
            sort_keys=True,
            indent=4,
        )
