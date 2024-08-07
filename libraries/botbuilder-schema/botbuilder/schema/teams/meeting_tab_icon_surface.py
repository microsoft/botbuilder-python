from .surface import Surface
from .surface_type import SurfaceType


class MeetingTabIconSurface(Surface):
    """
    Specifies meeting tab icon surface.
    """

    tab_entity_id: str = None

    def __init__(self):
        super().__init__(SurfaceType.MEETING_TAB_ICON)

    def to_dict(self):
        """
        Converts the MeetingTabIconSurface object to a dictionary.
        :return: Dictionary representation of the MeetingTabIconSurface object.
        """
        return {"type": self.type.value, "tabEntityId": self.tab_entity_id}
