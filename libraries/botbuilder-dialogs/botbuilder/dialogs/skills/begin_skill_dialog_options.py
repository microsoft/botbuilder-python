# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.schema import Activity


class BeginSkillDialogOptions:
    def __init__(
        self, activity: Activity, connection_name: str = None
    ):  # pylint: disable=unused-argument
        self.activity = activity
        self.connection_name = connection_name

    @staticmethod
    def from_object(obj: object) -> "BeginSkillDialogOptions":
        if isinstance(obj, dict) and "activity" in obj:
            return BeginSkillDialogOptions(obj["activity"], obj.get("connection_name"))
        if hasattr(obj, "activity"):
            return BeginSkillDialogOptions(
                obj.activity,
                obj.connection_name if hasattr(obj, "connection_name") else None,
            )
        return None
