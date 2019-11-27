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


class MessagingExtensionSuggestedAction(Model):
    """Messaging extension Actions (Only when type is auth or config).

    :param actions: Actions
    :type actions: list[~botframework.connector.teams.models.CardAction]
    """

    _attribute_map = {
        'actions': {'key': 'actions', 'type': '[CardAction]'},
    }

    def __init__(self, **kwargs):
        super(MessagingExtensionSuggestedAction, self).__init__(**kwargs)
        self.actions = kwargs.get('actions', None)
