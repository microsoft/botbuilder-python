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

from .task_module_response_base_py3 import TaskModuleResponseBase


class TaskModuleContinueResponse(TaskModuleResponseBase):
    """Task Module Response with continue action.

    :param type: Choice of action options when responding to the task/submit
     message. Possible values include: 'message', 'continue'
    :type type: str or ~botframework.connector.teams.models.enum
    :param value: The JSON for the Adaptive card to appear in the task module.
    :type value: ~botframework.connector.teams.models.TaskModuleTaskInfo
    """

    _attribute_map = {
        'type': {'key': 'type', 'type': 'str'},
        'value': {'key': 'value', 'type': 'TaskModuleTaskInfo'},
    }

    def __init__(self, *, type=None, value=None, **kwargs) -> None:
        super(TaskModuleContinueResponse, self).__init__(type=type, **kwargs)
        self.value = value
