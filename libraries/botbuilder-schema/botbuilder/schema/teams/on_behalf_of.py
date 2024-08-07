import json
from typing import Optional


class OnBehalfOf:
    """
    Specifies attribution for notifications.
    """

    def __init__(
        self,
        item_id: int = 0,
        mention_type: str = "person",
        mri: Optional[str] = None,
        display_name: Optional[str] = None,
    ):
        self.item_id = item_id
        self.mention_type = mention_type
        self.mri = mri
        self.display_name = display_name

    def to_json(self) -> str:
        """
        Converts the OnBehalfOf object to JSON.

        :return: JSON representation of the OnBehalfOf object.
        """
        return json.dumps(
            {
                "itemid": self.item_id,
                "mentionType": self.mention_type,
                "mri": self.mri,
                "displayName": self.display_name,
            },
            sort_keys=True,
            indent=4,
        )
