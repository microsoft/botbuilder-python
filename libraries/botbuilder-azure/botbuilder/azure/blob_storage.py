import json
from typing import Dict, List

from jsonpickle import encode
from jsonpickle.unpickler import Unpickler
from azure.storage.blob import BlockBlobService, Blob, PublicAccess
from botbuilder.core import Storage

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

    async def read(self, keys: List[str]) -> Dict[str, object]:
        if not keys:
            raise Exception("Keys are required when reading")

        self.client.create_container(self.settings.container_name)
        self.client.set_container_acl(
            self.settings.container_name, public_access=PublicAccess.Container
        )
        items = {}

        for key in keys:
            if self.client.exists(
                container_name=self.settings.container_name, blob_name=key
            ):
                items[key] = self._blob_to_store_item(
                    self.client.get_blob_to_text(
                        container_name=self.settings.container_name, blob_name=key
                    )
                )

        return items

    async def write(self, changes: Dict[str, object]):
        if changes is None:
            raise Exception("Changes are required when writing")
        if not changes:
            return

        self.client.create_container(self.settings.container_name)
        self.client.set_container_acl(
            self.settings.container_name, public_access=PublicAccess.Container
        )

        for (name, item) in changes.items():
            e_tag = None
            if isinstance(item, dict):
                e_tag = item.get("e_tag", None)
            elif hasattr(item, "e_tag"):
                e_tag = item.e_tag
            e_tag = None if e_tag == "*" else e_tag
            if e_tag == "":
                raise Exception("blob_storage.write(): etag missing")
            item_str = self._store_item_to_str(item)
            try:
                self.client.create_blob_from_text(
                    container_name=self.settings.container_name,
                    blob_name=name,
                    text=item_str,
                    if_match=e_tag,
                )
            except Exception as error:
                raise error

    async def delete(self, keys: List[str]):
        if keys is None:
            raise Exception("BlobStorage.delete: keys parameter can't be null")

        self.client.create_container(self.settings.container_name)
        self.client.set_container_acl(
            self.settings.container_name, public_access=PublicAccess.Container
        )

        for key in keys:
            if self.client.exists(
                container_name=self.settings.container_name, blob_name=key
            ):
                self.client.delete_blob(
                    container_name=self.settings.container_name, blob_name=key
                )

    def _blob_to_store_item(self, blob: Blob) -> object:
        item = json.loads(blob.content)
        item["e_tag"] = blob.properties.etag
        result = Unpickler().restore(item)
        return result

    def _store_item_to_str(self, item: object) -> str:
        return encode(item)
