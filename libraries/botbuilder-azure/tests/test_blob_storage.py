# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import pytest
from botbuilder.core import StoreItem
from botbuilder.azure import BlobStorage, BlobStorageSettings
from botbuilder.testing import StorageBaseTests

# local blob emulator instance blob

BLOB_STORAGE_SETTINGS = BlobStorageSettings(
    account_name="",
    account_key="",
    container_name="test",
    # Default Azure Storage Emulator Connection String
    connection_string="AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq"
    + "2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;DefaultEndpointsProtocol=http;BlobEndpoint="
    + "http://127.0.0.1:10000/devstoreaccount1;QueueEndpoint=http://127.0.0.1:10001/devstoreaccount1;"
    + "TableEndpoint=http://127.0.0.1:10002/devstoreaccount1;",
)
EMULATOR_RUNNING = False


def get_storage():
    return BlobStorage(BLOB_STORAGE_SETTINGS)


async def reset():
    storage = get_storage()
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


class TestBlobStorageConstructor:
    @pytest.mark.asyncio
    async def test_blob_storage_init_should_error_without_cosmos_db_config(self):
        try:
            BlobStorage(BlobStorageSettings())  # pylint: disable=no-value-for-parameter
        except Exception as error:
            assert error


class TestBlobStorageBaseTests:
    @pytest.mark.skipif(not EMULATOR_RUNNING, reason="Needs the emulator to run.")
    @pytest.mark.asyncio
    async def test_return_empty_object_when_reading_unknown_key(self):
        await reset()

        test_ran = await StorageBaseTests.return_empty_object_when_reading_unknown_key(
            get_storage()
        )

        assert test_ran

    @pytest.mark.skipif(not EMULATOR_RUNNING, reason="Needs the emulator to run.")
    @pytest.mark.asyncio
    async def test_handle_null_keys_when_reading(self):
        await reset()

        test_ran = await StorageBaseTests.handle_null_keys_when_reading(get_storage())

        assert test_ran

    @pytest.mark.skipif(not EMULATOR_RUNNING, reason="Needs the emulator to run.")
    @pytest.mark.asyncio
    async def test_handle_null_keys_when_writing(self):
        await reset()

        test_ran = await StorageBaseTests.handle_null_keys_when_writing(get_storage())

        assert test_ran

    @pytest.mark.skipif(not EMULATOR_RUNNING, reason="Needs the emulator to run.")
    @pytest.mark.asyncio
    async def test_does_not_raise_when_writing_no_items(self):
        await reset()

        test_ran = await StorageBaseTests.does_not_raise_when_writing_no_items(
            get_storage()
        )

        assert test_ran

    @pytest.mark.skipif(not EMULATOR_RUNNING, reason="Needs the emulator to run.")
    @pytest.mark.asyncio
    async def test_create_object(self):
        await reset()

        test_ran = await StorageBaseTests.create_object(get_storage())

        assert test_ran

    @pytest.mark.skipif(not EMULATOR_RUNNING, reason="Needs the emulator to run.")
    @pytest.mark.asyncio
    async def test_handle_crazy_keys(self):
        await reset()

        test_ran = await StorageBaseTests.handle_crazy_keys(get_storage())

        assert test_ran

    @pytest.mark.skipif(not EMULATOR_RUNNING, reason="Needs the emulator to run.")
    @pytest.mark.asyncio
    async def test_update_object(self):
        await reset()

        test_ran = await StorageBaseTests.update_object(get_storage())

        assert test_ran

    @pytest.mark.skipif(not EMULATOR_RUNNING, reason="Needs the emulator to run.")
    @pytest.mark.asyncio
    async def test_delete_object(self):
        await reset()

        test_ran = await StorageBaseTests.delete_object(get_storage())

        assert test_ran

    @pytest.mark.skipif(not EMULATOR_RUNNING, reason="Needs the emulator to run.")
    @pytest.mark.asyncio
    async def test_perform_batch_operations(self):
        await reset()

        test_ran = await StorageBaseTests.perform_batch_operations(get_storage())

        assert test_ran

    @pytest.mark.skipif(not EMULATOR_RUNNING, reason="Needs the emulator to run.")
    @pytest.mark.asyncio
    async def test_proceeds_through_waterfall(self):
        await reset()

        test_ran = await StorageBaseTests.proceeds_through_waterfall(get_storage())

        assert test_ran


class TestBlobStorage:
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
