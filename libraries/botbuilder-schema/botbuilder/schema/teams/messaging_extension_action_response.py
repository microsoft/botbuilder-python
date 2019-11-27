# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class MessagingExtensionActionResponse(Model):
    """Response of messaging extension action.

    :param task: The JSON for the Adaptive card to appear in the task module.
    :type task: ~botframework.connector.teams.models.TaskModuleResponseBase
    :param compose_extension:
    :type compose_extension:
     ~botframework.connector.teams.models.MessagingExtensionResult
    """

    _attribute_map = {
        "task": {"key": "task", "type": "TaskModuleResponseBase"},
        "compose_extension": {
            "key": "composeExtension",
            "type": "MessagingExtensionResult",
        },
    }

    def __init__(self, **kwargs):
        super(MessagingExtensionActionResponse, self).__init__(**kwargs)
        self.task = kwargs.get("task", None)
        self.compose_extension = kwargs.get("compose_extension", None)
