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


class MessageActionsPayloadAttachment(Model):
    """Represents the attachment in a message.

    :param id: The id of the attachment.
    :type id: str
    :param content_type: The type of the attachment.
    :type content_type: str
    :param content_url: The url of the attachment, in case of a external link.
    :type content_url: str
    :param content: The content of the attachment, in case of a code snippet,
     email, or file.
    :type content: object
    :param name: The plaintext display name of the attachment.
    :type name: str
    :param thumbnail_url: The url of a thumbnail image that might be embedded
     in the attachment, in case of a card.
    :type thumbnail_url: str
    """

    _attribute_map = {
        'id': {'key': 'id', 'type': 'str'},
        'content_type': {'key': 'contentType', 'type': 'str'},
        'content_url': {'key': 'contentUrl', 'type': 'str'},
        'content': {'key': 'content', 'type': 'object'},
        'name': {'key': 'name', 'type': 'str'},
        'thumbnail_url': {'key': 'thumbnailUrl', 'type': 'str'},
    }

    def __init__(self, **kwargs):
        super(MessageActionsPayloadAttachment, self).__init__(**kwargs)
        self.id = kwargs.get('id', None)
        self.content_type = kwargs.get('content_type', None)
        self.content_url = kwargs.get('content_url', None)
        self.content = kwargs.get('content', None)
        self.name = kwargs.get('name', None)
        self.thumbnail_url = kwargs.get('thumbnail_url', None)
