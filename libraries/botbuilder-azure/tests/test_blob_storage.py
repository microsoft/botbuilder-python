# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import pytest
from botbuilder.core import StoreItem
from botbuilder.azure import BlobStorage, BlobStorageSettings

# local blob emulator instance blob
BLOB_STORAGE_SETTINGS = BlobStorageSettings(
    account_name="", account_key="", container_name="test"
)
EMULATOR_RUNNING = False


async def reset():
    storage = BlobStorage(BLOB_STORAGE_SETTINGS)
    try:
        await storage.client.delete_container(
            container_name=BLOB_STORAGE_SETTINGS.container_name
        )
    except Exception:
        pass


class SimpleStoreItem(StoreItem):
    def __init__(self, counter=1, e_tag="*"):
        super(SimpleStoreItem, self).__init__()
        self.counter = counter
        self.e_tag = e_tag


class TestBlobStorage:
    @pytest.mark.asyncio
    async def test_blob_storage_init_should_error_without_cosmos_db_config(self):
        try:
            BlobStorage(BlobStorageSettings())  # pylint: disable=no-value-for-parameter
        except Exception as error:
            assert error

    @pytest.mark.skipif(not EMULATOR_RUNNING, reason="Needs the emulator to run.")
    @pytest.mark.asyncio
    async def test_blob_storage_read_should_return_data_with_valid_key(self):
        storage = BlobStorage(BLOB_STORAGE_SETTINGS)
        await storage.write({"user": SimpleStoreItem()})

        data = await storage.read(["user"])
        assert "user" in data
        assert data["user"].counter == 1
        assert len(data.keys()) == 1

    @pytest.mark.skipif(not EMULATOR_RUNNING, reason="Needs the emulator to run.")
    @pytest.mark.asyncio
    async def test_blob_storage_read_update_should_return_new_etag(self):
        storage = BlobStorage(BLOB_STORAGE_SETTINGS)
        await storage.write({"test": SimpleStoreItem(counter=1)})
        data_result = await storage.read(["test"])
        data_result["test"].counter = 2
        await storage.write(data_result)
        data_updated = await storage.read(["test"])
        assert data_updated["test"].counter == 2
        assert data_updated["test"].e_tag != data_result["test"].e_tag

    @pytest.mark.skipif(not EMULATOR_RUNNING, reason="Needs the emulator to run.")
    @pytest.mark.asyncio
    async def test_blob_storage_read_no_key_should_throw(self):
        try:
            storage = BlobStorage(BLOB_STORAGE_SETTINGS)
            await storage.read([])
        except Exception as error:
            assert error

    @pytest.mark.skipif(not EMULATOR_RUNNING, reason="Needs the emulator to run.")
    @pytest.mark.asyncio
    async def test_blob_storage_write_should_add_new_value(self):
        storage = BlobStorage(BLOB_STORAGE_SETTINGS)
        await storage.write({"user": SimpleStoreItem(counter=1)})

        data = await storage.read(["user"])
        assert "user" in data
        assert data["user"].counter == 1

    @pytest.mark.skipif(not EMULATOR_RUNNING, reason="Needs the emulator to run.")
    @pytest.mark.asyncio
    async def test_blob_storage_write_should_overwrite_when_new_e_tag_is_an_asterisk(
        self,
    ):
        storage = BlobStorage(BLOB_STORAGE_SETTINGS)
        await storage.write({"user": SimpleStoreItem()})

        await storage.write({"user": SimpleStoreItem(counter=10, e_tag="*")})
        data = await storage.read(["user"])
        assert data["user"].counter == 10

    @pytest.mark.skipif(not EMULATOR_RUNNING, reason="Needs the emulator to run.")
    @pytest.mark.asyncio
    async def test_blob_storage_write_batch_operation(self):
        storage = BlobStorage(BLOB_STORAGE_SETTINGS)
        await storage.write(
            {
                "batch1": SimpleStoreItem(counter=1),
                "batch2": SimpleStoreItem(counter=1),
                "batch3": SimpleStoreItem(counter=1),
            }
        )
        data = await storage.read(["batch1", "batch2", "batch3"])
        assert len(data.keys()) == 3
        assert data["batch1"]
        assert data["batch2"]
        assert data["batch3"]
        assert data["batch1"].counter == 1
        assert data["batch2"].counter == 1
        assert data["batch3"].counter == 1
        assert data["batch1"].e_tag
        assert data["batch2"].e_tag
        assert data["batch3"].e_tag
        await storage.delete(["batch1", "batch2", "batch3"])
        data = await storage.read(["batch1", "batch2", "batch3"])
        assert not data.keys()

    @pytest.mark.skipif(not EMULATOR_RUNNING, reason="Needs the emulator to run.")
    @pytest.mark.asyncio
    async def test_blob_storage_delete_should_delete_according_cached_data(self):
        storage = BlobStorage(BLOB_STORAGE_SETTINGS)
        await storage.write({"test": SimpleStoreItem()})
        try:
            await storage.delete(["test"])
        except Exception as error:
            raise error
        else:
            data = await storage.read(["test"])

            assert isinstance(data, dict)
            assert not data.keys()

    @pytest.mark.skipif(not EMULATOR_RUNNING, reason="Needs the emulator to run.")
    @pytest.mark.asyncio
    async def test_blob_storage_delete_should_delete_multiple_values_when_given_multiple_valid_keys(
        self,
    ):
        storage = BlobStorage(BLOB_STORAGE_SETTINGS)
        await storage.write({"test": SimpleStoreItem(), "test2": SimpleStoreItem(2)})

        await storage.delete(["test", "test2"])
        data = await storage.read(["test", "test2"])
        assert not data.keys()

    @pytest.mark.skipif(not EMULATOR_RUNNING, reason="Needs the emulator to run.")
    @pytest.mark.asyncio
    async def test_blob_storage_delete_should_delete_values_when_given_multiple_valid_keys_and_ignore_other_data(
        self,
    ):
        storage = BlobStorage(BLOB_STORAGE_SETTINGS)
        await storage.write(
            {
                "test": SimpleStoreItem(),
                "test2": SimpleStoreItem(counter=2),
                "test3": SimpleStoreItem(counter=3),
            }
        )

        await storage.delete(["test", "test2"])
        data = await storage.read(["test", "test2", "test3"])
        assert len(data.keys()) == 1

    @pytest.mark.skipif(not EMULATOR_RUNNING, reason="Needs the emulator to run.")
    @pytest.mark.asyncio
    async def test_blob_storage_delete_invalid_key_should_do_nothing_and_not_affect_cached_data(
        self,
    ):
        storage = BlobStorage(BLOB_STORAGE_SETTINGS)
        await storage.write({"test": SimpleStoreItem()})

        await storage.delete(["foo"])
        data = await storage.read(["test"])
        assert len(data.keys()) == 1
        data = await storage.read(["foo"])
        assert not data.keys()

    @pytest.mark.skipif(not EMULATOR_RUNNING, reason="Needs the emulator to run.")
    @pytest.mark.asyncio
    async def test_blob_storage_delete_invalid_keys_should_do_nothing_and_not_affect_cached_data(
        self,
    ):
        storage = BlobStorage(BLOB_STORAGE_SETTINGS)
        await storage.write({"test": SimpleStoreItem()})

        await storage.delete(["foo", "bar"])
        data = await storage.read(["test"])
        assert len(data.keys()) == 1
