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


class TaskModuleRequest(Model):
    """Task module invoke request value payload.

    :param data: User input data. Free payload with key-value pairs.
    :type data: object
    :param context: Current user context, i.e., the current theme
    :type context:
     ~botframework.connector.teams.models.TaskModuleRequestContext
    """

    _attribute_map = {
        'data': {'key': 'data', 'type': 'object'},
        'context': {'key': 'context', 'type': 'TaskModuleRequestContext'},
    }

    def __init__(self, *, data=None, context=None, **kwargs) -> None:
        super(TaskModuleRequest, self).__init__(**kwargs)
        self.data = data
        self.context = context
