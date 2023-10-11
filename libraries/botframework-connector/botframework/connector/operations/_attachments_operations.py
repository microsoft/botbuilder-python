# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

from msrest.pipeline import ClientRawResponse

from .. import models


class AttachmentsOperations:
    """AttachmentsOperations operations.

    You should not instantiate directly this class, but create a Client instance that will create it for you and attach
     it as attribute.

    :param client: Client for service requests.
    :param config: Configuration of service client.
    :param serializer: An object model serializer.
    :param deserializer: An object model deserializer.
    :ivar api_version: The API version to use for the request. Constant value: "v3".
    """

    models = models

    def __init__(self, client, config, serializer, deserializer):
        self._client = client
        self._serialize = serializer
        self._deserialize = deserializer

        self.config = config
        self.api_version = "v3"

    def get_attachment_info(
        self, attachment_id, custom_headers=None, raw=False, **operation_config
    ):
        """GetAttachmentInfo.

        Get AttachmentInfo structure describing the attachment views.

        :param attachment_id: attachment id
        :type attachment_id: str
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: AttachmentInfo or ClientRawResponse if raw=true
        :rtype: ~botframework.connector.models.AttachmentInfo or
         ~msrest.pipeline.ClientRawResponse
        :raises:
         :class:`ErrorResponseException<botframework.connector.models.ErrorResponseException>`
        """
        # Construct URL
        url = self.get_attachment_info.metadata["url"]
        path_format_arguments = {
            "attachmentId": self._serialize.url("attachment_id", attachment_id, "str")
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}

        # Construct headers
        header_parameters = {}
        header_parameters["Accept"] = "application/json"
        if custom_headers:
            header_parameters.update(custom_headers)

        # Construct and send request
        request = self._client.get(url, query_parameters, header_parameters)
        response = self._client.send(request, stream=False, **operation_config)

        if response.status_code not in [200]:
            raise models.ErrorResponseException(self._deserialize, response)

        deserialized = None
        if response.status_code == 200:
            deserialized = self._deserialize("AttachmentInfo", response)

        if raw:
            client_raw_response = ClientRawResponse(deserialized, response)
            return client_raw_response

        return deserialized

    get_attachment_info.metadata = {"url": "/v3/attachments/{attachmentId}"}

    def get_attachment(
        self,
        attachment_id,
        view_id,
        custom_headers=None,
        raw=False,
        callback=None,
        **operation_config
    ):
        """GetAttachment.

        Get the named view as binary content.

        :param attachment_id: attachment id
        :type attachment_id: str
        :param view_id: View id from attachmentInfo
        :type view_id: str
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param callback: When specified, will be called with each chunk of
         data that is streamed. The callback should take two arguments, the
         bytes of the current chunk of data and the response object. If the
         data is uploading, response will be None.
        :type callback: Callable[Bytes, response=None]
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: object or ClientRawResponse if raw=true
        :rtype: Generator or ~msrest.pipeline.ClientRawResponse
        :raises:
         :class:`ErrorResponseException<botframework.connector.models.ErrorResponseException>`
        """
        # Construct URL
        url = self.get_attachment.metadata["url"]
        path_format_arguments = {
            "attachmentId": self._serialize.url("attachment_id", attachment_id, "str"),
            "viewId": self._serialize.url("view_id", view_id, "str"),
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}

        # Construct headers
        header_parameters = {}
        header_parameters["Accept"] = "application/json"
        if custom_headers:
            header_parameters.update(custom_headers)

        # Construct and send request
        request = self._client.get(url, query_parameters, header_parameters)
        response = self._client.send(request, stream=True, **operation_config)

        if response.status_code not in [200, 301, 302]:
            raise models.ErrorResponseException(self._deserialize, response)

        deserialized = self._client.stream_download(response, callback)

        if raw:
            client_raw_response = ClientRawResponse(deserialized, response)
            return client_raw_response

        return deserialized

    get_attachment.metadata = {"url": "/v3/attachments/{attachmentId}/views/{viewId}"}
