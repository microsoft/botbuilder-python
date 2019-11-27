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


class FileConsentCard(Model):
    """File consent card attachment.

    :param description: File description.
    :type description: str
    :param size_in_bytes: Size of the file to be uploaded in Bytes.
    :type size_in_bytes: long
    :param accept_context: Context sent back to the Bot if user consented to
     upload. This is free flow schema and is sent back in Value field of
     Activity.
    :type accept_context: object
    :param decline_context: Context sent back to the Bot if user declined.
     This is free flow schema and is sent back in Value field of Activity.
    :type decline_context: object
    """

    _attribute_map = {
        'description': {'key': 'description', 'type': 'str'},
        'size_in_bytes': {'key': 'sizeInBytes', 'type': 'long'},
        'accept_context': {'key': 'acceptContext', 'type': 'object'},
        'decline_context': {'key': 'declineContext', 'type': 'object'},
    }

    def __init__(self, *, description: str=None, size_in_bytes: int=None, accept_context=None, decline_context=None, **kwargs) -> None:
        super(FileConsentCard, self).__init__(**kwargs)
        self.description = description
        self.size_in_bytes = size_in_bytes
        self.accept_context = accept_context
        self.decline_context = decline_context
