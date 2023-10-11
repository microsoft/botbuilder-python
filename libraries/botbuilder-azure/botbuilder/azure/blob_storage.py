# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import json
from typing import Dict, List

from jsonpickle import encode
from jsonpickle.unpickler import Unpickler
from azure.core import MatchConditions
from azure.core.exceptions import (
    HttpResponseError,
    ResourceExistsError,
    ResourceNotFoundError,
)
from azure.storage.blob.aio import (
    BlobServiceClient,
    BlobClient,
    StorageStreamDownloader,
)
from botbuilder.core import Storage


class BlobStorageSettings:
    """The class for Azure Blob configuration for the Azure Bot Framework.

    :param container_name: Name of the Blob container.
    :type container_name: str
    :param account_name: Name of the Blob Storage account. Required if not using connection_string.
    :type account_name: str
    :param account_key: Key of the Blob Storage account. Required if not using connection_string.
    :type account_key: str
    :param connection_string: Connection string of the Blob Storage account.
        Required if not using account_name and account_key.
    :type connection_string: str
    """

    def __init__(
        self,
        container_name: str,
        account_name: str = "",
        account_key: str = "",
        connection_string: str = "",
    ):
        self.container_name = container_name
        self.account_name = account_name
        self.account_key = account_key
        self.connection_string = connection_string


# New Azure Blob SDK only allows connection strings, but our SDK allows key+name.
# This is here for backwards compatibility.
def convert_account_name_and_key_to_connection_string(settings: BlobStorageSettings):
    if not settings.account_name or not settings.account_key:
        raise Exception(
            "account_name and account_key are both required for BlobStorageSettings if not using a connections string."
        )
    return (
        f"DefaultEndpointsProtocol=https;AccountName={settings.account_name};"
        f"AccountKey={settings.account_key};EndpointSuffix=core.windows.net"
    )


class BlobStorage(Storage):
    """An Azure Blob based storage provider for a bot.

    This class uses a single Azure Storage Blob Container.
    Each entity or StoreItem is serialized into a JSON string and stored in an individual text blob.
    Each blob is named after the store item key,  which is encoded so that it conforms a valid blob name.
    If an entity is an StoreItem, the storage object will set the entity's e_tag
    property value to the blob's e_tag upon read. Afterward, an match_condition with the ETag value
    will be generated during Write. New entities start with a null e_tag.

    :param settings: Settings used to instantiate the Blob service.
    :type settings: :class:`botbuilder.azure.BlobStorageSettings`
    """

    def __init__(self, settings: BlobStorageSettings):
        if not settings.container_name:
            raise Exception("Container name is required.")

        if settings.connection_string:
            blob_service_client = BlobServiceClient.from_connection_string(
                settings.connection_string
            )
        else:
            blob_service_client = BlobServiceClient.from_connection_string(
                convert_account_name_and_key_to_connection_string(settings)
            )

        self.__container_client = blob_service_client.get_container_client(
            settings.container_name
        )

        self.__initialized = False

    async def _initialize(self):
        if self.__initialized is False:
            # This should only happen once - assuming this is a singleton.
            # ContainerClient.exists() method is available in an unreleased version of the SDK. Until then, we use:
            try:
                await self.__container_client.create_container()
            except ResourceExistsError:
                pass
            self.__initialized = True
        return self.__initialized

    async def read(self, keys: List[str]) -> Dict[str, object]:
        """Retrieve entities from the configured blob container.

        :param keys: An array of entity keys.
        :type keys: Dict[str, object]
        :return dict:
        """
        if not keys:
            raise Exception("Keys are required when reading")

        await self._initialize()

        items = {}

        for key in keys:
            blob_client = self.__container_client.get_blob_client(key)

            try:
                items[key] = await self._inner_read_blob(blob_client)
            except HttpResponseError as err:
                if err.status_code == 404:
                    continue

        return items

    async def write(self, changes: Dict[str, object]):
        """Stores a new entity in the configured blob container.

        :param changes: The changes to write to storage.
        :type changes: Dict[str, object]
        :return:
        """
        if changes is None:
            raise Exception("Changes are required when writing")
        if not changes:
            return

        await self._initialize()

        for name, item in changes.items():
            blob_reference = self.__container_client.get_blob_client(name)

            e_tag = None
            if isinstance(item, dict):
                e_tag = item.get("e_tag", None)
            elif hasattr(item, "e_tag"):
                e_tag = item.e_tag
            e_tag = None if e_tag == "*" else e_tag
            if e_tag == "":
                raise Exception("blob_storage.write(): etag missing")

            item_str = self._store_item_to_str(item)

            if e_tag:
                await blob_reference.upload_blob(
                    item_str, match_condition=MatchConditions.IfNotModified, etag=e_tag
                )
            else:
                await blob_reference.upload_blob(item_str, overwrite=True)

    async def delete(self, keys: List[str]):
        """Deletes entity blobs from the configured container.

        :param keys: An array of entity keys.
        :type keys: Dict[str, object]
        """
        if keys is None:
            raise Exception("BlobStorage.delete: keys parameter can't be null")

        await self._initialize()

        for key in keys:
            blob_client = self.__container_client.get_blob_client(key)
            try:
                await blob_client.delete_blob()
            # We can't delete what's already gone.
            except ResourceNotFoundError:
                pass

    def _store_item_to_str(self, item: object) -> str:
        return encode(item)

    async def _inner_read_blob(self, blob_client: BlobClient):
        blob = await blob_client.download_blob()

        return await self._blob_to_store_item(blob)

    @staticmethod
    async def _blob_to_store_item(blob: StorageStreamDownloader) -> object:
        item = json.loads(await blob.content_as_text())
        item["e_tag"] = blob.properties.etag.replace('"', "")
        result = Unpickler().restore(item)
        return result
