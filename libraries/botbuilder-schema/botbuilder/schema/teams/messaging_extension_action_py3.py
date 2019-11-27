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

from .task_module_request_py3 import TaskModuleRequest


class MessagingExtensionAction(TaskModuleRequest):
    """Messaging extension action.

    :param data: User input data. Free payload with key-value pairs.
    :type data: object
    :param context: Current user context, i.e., the current theme
    :type context:
     ~botframework.connector.teams.models.TaskModuleRequestContext
    :param command_id: Id of the command assigned by Bot
    :type command_id: str
    :param command_context: The context from which the command originates.
     Possible values include: 'message', 'compose', 'commandbox'
    :type command_context: str or ~botframework.connector.teams.models.enum
    :param bot_message_preview_action: Bot message preview action taken by
     user. Possible values include: 'edit', 'send'
    :type bot_message_preview_action: str or
     ~botframework.connector.teams.models.enum
    :param bot_activity_preview:
    :type bot_activity_preview:
     list[~botframework.connector.teams.models.Activity]
    :param message_payload: Message content sent as part of the command
     request.
    :type message_payload:
     ~botframework.connector.teams.models.MessageActionsPayload
    """

    _attribute_map = {
        'data': {'key': 'data', 'type': 'object'},
        'context': {'key': 'context', 'type': 'TaskModuleRequestContext'},
        'command_id': {'key': 'commandId', 'type': 'str'},
        'command_context': {'key': 'commandContext', 'type': 'str'},
        'bot_message_preview_action': {'key': 'botMessagePreviewAction', 'type': 'str'},
        'bot_activity_preview': {'key': 'botActivityPreview', 'type': '[Activity]'},
        'message_payload': {'key': 'messagePayload', 'type': 'MessageActionsPayload'},
    }

    def __init__(self, *, data=None, context=None, command_id: str=None, command_context=None, bot_message_preview_action=None, bot_activity_preview=None, message_payload=None, **kwargs) -> None:
        super(MessagingExtensionAction, self).__init__(data=data, context=context, **kwargs)
        self.command_id = command_id
        self.command_context = command_context
        self.bot_message_preview_action = bot_message_preview_action
        self.bot_activity_preview = bot_activity_preview
        self.message_payload = message_payload
