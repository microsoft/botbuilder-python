# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from enum import Enum


class SurfaceType(str, Enum):
    """
    Defines Teams Surface type for use with a Surface object.
    """

    UNKNOWN = "Unknown"
    MEETING_STAGE = "MeetingStage"
    MEETING_TAB_ICON = "MeetingTabIcon"
