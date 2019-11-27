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


class FileUploadInfo(Model):
    """Information about the file to be uploaded.

    :param name: Name of the file.
    :type name: str
    :param upload_url: URL to an upload session that the bot can use to set
     the file contents.
    :type upload_url: str
    :param content_url: URL to file.
    :type content_url: str
    :param unique_id: ID that uniquely identifies the file.
    :type unique_id: str
    :param file_type: Type of the file.
    :type file_type: str
    """

    _attribute_map = {
        'name': {'key': 'name', 'type': 'str'},
        'upload_url': {'key': 'uploadUrl', 'type': 'str'},
        'content_url': {'key': 'contentUrl', 'type': 'str'},
        'unique_id': {'key': 'uniqueId', 'type': 'str'},
        'file_type': {'key': 'fileType', 'type': 'str'},
    }

    def __init__(self, *, name: str=None, upload_url: str=None, content_url: str=None, unique_id: str=None, file_type: str=None, **kwargs) -> None:
        super(FileUploadInfo, self).__init__(**kwargs)
        self.name = name
        self.upload_url = upload_url
        self.content_url = content_url
        self.unique_id = unique_id
        self.file_type = file_type
