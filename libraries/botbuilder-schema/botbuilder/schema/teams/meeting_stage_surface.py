from typing import Generic, TypeVar, Optional
from botbuilder.schema.teams.content_type import ContentType
from botbuilder.schema.teams.surface import Surface
from botbuilder.schema.teams.surface_type import SurfaceType

T = TypeVar("T")


class MeetingStageSurface(Generic[T], Surface):
    def __init__(self):
        super().__init__(SurfaceType.MEETING_STAGE)
        self.content_type = ContentType.TASK
        self.content: Optional[T] = None
