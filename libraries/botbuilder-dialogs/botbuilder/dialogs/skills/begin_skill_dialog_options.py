# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.schema import Activity


class BeginSkillDialogOptions:
    def __init__(self, activity: Activity):
        self.activity = activity

    @staticmethod
    def from_object(obj: object) -> "BeginSkillDialogOptions":
        if isinstance(obj, dict) and "activity" in obj:
            return BeginSkillDialogOptions(obj["activity"])
        if hasattr(obj, "activity"):
            return BeginSkillDialogOptions(obj.activity)
        return None
