from dataclasses import dataclass, field
import json


@dataclass
class OnBehalfOf:
    """
    Specifies attribution for notifications.
    """

    item_id: int = field(default=0, metadata={"json": "itemid"})
    mention_type: str = field(default="person", metadata={"json": "mentionType"})
    mri: str = field(default=None, metadata={"json": "mri"})
    display_name: str = field(default=None, metadata={"json": "displayName"})

    def to_json(self) -> str:
        """
        Converts the OnBehalfOf object to JSON.

        :return: JSON representation of the OnBehalfOf object.
        """
        return json.dumps(
            self,
            default=lambda o: {k: v for k, v in o.__dict__.items() if v is not None},
            sort_keys=True,
            indent=4,
        )
