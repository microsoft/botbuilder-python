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


class FileInfoCard(Model):
    """File info card.

    :param unique_id: Unique Id for the file.
    :type unique_id: str
    :param file_type: Type of file.
    :type file_type: str
    :param etag: ETag for the file.
    :type etag: object
    """

    _attribute_map = {
        "unique_id": {"key": "uniqueId", "type": "str"},
        "file_type": {"key": "fileType", "type": "str"},
        "etag": {"key": "etag", "type": "object"},
    }

    def __init__(
        self, *, unique_id: str = None, file_type: str = None, etag=None, **kwargs
    ) -> None:
        super(FileInfoCard, self).__init__(**kwargs)
        self.unique_id = unique_id
        self.file_type = file_type
        self.etag = etag
