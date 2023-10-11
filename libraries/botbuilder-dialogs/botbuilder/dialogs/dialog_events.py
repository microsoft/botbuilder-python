# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from enum import Enum


class DialogEvents(str, Enum):
    begin_dialog = "beginDialog"
    reprompt_dialog = "repromptDialog"
    cancel_dialog = "cancelDialog"
    activity_received = "activityReceived"
    version_changed = "versionChanged"
    error = "error"
    custom = "custom"
