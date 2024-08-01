from dataclasses import dataclass, field
from typing import List
from .on_behalf_of import OnBehalfOf


@dataclass
class MeetingNotificationChannelData:
    """
    Specify Teams Bot meeting notification channel data.
    """

    on_behalf_of_list: List[OnBehalfOf] = field(
        default_factory=list, metadata={"json": "OnBehalfOf"}
    )
