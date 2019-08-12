import json
from typing import List

from azure.storage.blob import BlockBlobService, Blob
from botbuilder.core import Storage, StoreItem

# TODO: sanitize_blob_name


class BlobStorageSettings:
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


class BlobStorage(Storage):
    def __init__(self, settings: BlobStorageSettings):
        if settings.connection_string:
            client = BlockBlobService(connection_string=settings.connection_string)
        elif settings.account_name and settings.account_key:
            client = BlockBlobService(
                account_name=settings.account_name, account_key=settings.account_key
            )
        else:
            raise Exception(
                "Connection string should be provided if there are no account name and key"
            )

        self.client = client
        self.settings = settings

    async def read(self, keys: List[str]):
        if not keys:
            raise Exception("Please provide at least one key to read from storage.")

        self.client.create_container(self.settings.container_name)
        items = {}

        for key in keys:
            if self.client.exists(
                container_name=self.settings.container_name, blob_name=key
            ):
                items[key] = self.client.get_blob_to_text(
                    container_name=self.settings.container_name, blob_name=key
                )

        return items

    async def write(self, changes):
        pass

    async def delete(self, keys: List[str]):
        pass

    def _blob_to_store_item(self, blob: Blob) -> StoreItem:
        item = json.loads(blob.content)
        item["e_tag"] = blob.properties.etag
        item["id"] = blob.name
        return StoreItem(**item)

    def _store_item_to_str(self, item: StoreItem) -> str:
        if hasattr(item, "e_tag"):
            delattr(item, "e_tag")
        if hasattr(item, "id"):
            delattr(item, "id")
        return str(item)
