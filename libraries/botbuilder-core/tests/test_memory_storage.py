# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import pytest

from botbuilder.core import MemoryStorage, StoreItem
from botbuilder.testing import StorageBaseTests


def get_storage():
    return MemoryStorage()


class SimpleStoreItem(StoreItem):
    def __init__(self, counter=1, e_tag="*"):
        super(SimpleStoreItem, self).__init__()
        self.counter = counter
        self.e_tag = e_tag


class TestMemoryStorageConstructor:
    def test_initializing_memory_storage_without_data_should_still_have_memory(self):
        storage = MemoryStorage()
        assert storage.memory is not None
        assert isinstance(storage.memory, dict)

    def test_memory_storage__e_tag_should_start_at_0(self):
        storage = MemoryStorage()
        assert storage._e_tag == 0  # pylint: disable=protected-access

    @pytest.mark.asyncio
    async def test_memory_storage_initialized_with_memory_should_have_accessible_data(
        self,
    ):
        storage = MemoryStorage({"test": SimpleStoreItem()})
        data = await storage.read(["test"])
        assert "test" in data
        assert data["test"].counter == 1
        assert len(data.keys()) == 1


class TestMemoryStorageBaseTests:
    @pytest.mark.asyncio
    async def test_return_empty_object_when_reading_unknown_key(self):
        test_ran = await StorageBaseTests.return_empty_object_when_reading_unknown_key(
            get_storage()
        )

        assert test_ran

    @pytest.mark.asyncio
    async def test_handle_null_keys_when_reading(self):
        test_ran = await StorageBaseTests.handle_null_keys_when_reading(get_storage())

        assert test_ran

    @pytest.mark.asyncio
    async def test_handle_null_keys_when_writing(self):
        test_ran = await StorageBaseTests.handle_null_keys_when_writing(get_storage())

        assert test_ran

    @pytest.mark.asyncio
    async def test_does_not_raise_when_writing_no_items(self):
        test_ran = await StorageBaseTests.does_not_raise_when_writing_no_items(
            get_storage()
        )

        assert test_ran

    @pytest.mark.asyncio
    async def test_create_object(self):
        test_ran = await StorageBaseTests.create_object(get_storage())

        assert test_ran

    @pytest.mark.asyncio
    async def test_handle_crazy_keys(self):
        test_ran = await StorageBaseTests.handle_crazy_keys(get_storage())

        assert test_ran

    @pytest.mark.asyncio
    async def test_update_object(self):
        test_ran = await StorageBaseTests.update_object(get_storage())

        assert test_ran

    @pytest.mark.asyncio
    async def test_delete_object(self):
        test_ran = await StorageBaseTests.delete_object(get_storage())

        assert test_ran

    @pytest.mark.asyncio
    async def test_perform_batch_operations(self):
        test_ran = await StorageBaseTests.perform_batch_operations(get_storage())

        assert test_ran

    @pytest.mark.asyncio
    async def test_proceeds_through_waterfall(self):
        test_ran = await StorageBaseTests.proceeds_through_waterfall(get_storage())

        assert test_ran


class TestMemoryStorage:
    @pytest.mark.asyncio
    async def test_memory_storage_write_should_overwrite_when_new_e_tag_is_an_asterisk_1(
        self,
    ):
        storage = MemoryStorage()
        await storage.write({"user": SimpleStoreItem(e_tag="1")})

        await storage.write({"user": SimpleStoreItem(counter=10, e_tag="*")})
        data = await storage.read(["user"])
        assert data["user"].counter == 10

    @pytest.mark.asyncio
    async def test_memory_storage_write_should_overwrite_when_new_e_tag_is_an_asterisk_2(
        self,
    ):
        storage = MemoryStorage()
        await storage.write({"user": SimpleStoreItem(e_tag="1")})

        await storage.write({"user": SimpleStoreItem(counter=5, e_tag="1")})
        data = await storage.read(["user"])
        assert data["user"].counter == 5

    @pytest.mark.asyncio
    async def test_memory_storage_read_with_invalid_key_should_return_empty_dict(self):
        storage = MemoryStorage()
        data = await storage.read(["test"])

        assert isinstance(data, dict)
        assert not data.keys()

    @pytest.mark.asyncio
    async def test_memory_storage_delete_should_delete_according_cached_data(self):
        storage = MemoryStorage({"test": "test"})
        try:
            await storage.delete(["test"])
        except Exception as error:
            raise error
        else:
            data = await storage.read(["test"])

            assert isinstance(data, dict)
            assert not data.keys()

    @pytest.mark.asyncio
    async def test_memory_storage_delete_should_delete_multiple_values_when_given_multiple_valid_keys(
        self,
    ):
        storage = MemoryStorage(
            {"test": SimpleStoreItem(), "test2": SimpleStoreItem(2, "2")}
        )

        await storage.delete(["test", "test2"])
        data = await storage.read(["test", "test2"])
        assert not data.keys()

    @pytest.mark.asyncio
    async def test_memory_storage_delete_should_delete_values_when_given_multiple_valid_keys_and_ignore_other_data(
        self,
    ):
        storage = MemoryStorage(
            {
                "test": SimpleStoreItem(),
                "test2": SimpleStoreItem(2, "2"),
                "test3": SimpleStoreItem(3, "3"),
            }
        )

        await storage.delete(["test", "test2"])
        data = await storage.read(["test", "test2", "test3"])
        assert len(data.keys()) == 1

    @pytest.mark.asyncio
    async def test_memory_storage_delete_invalid_key_should_do_nothing_and_not_affect_cached_data(
        self,
    ):
        storage = MemoryStorage({"test": "test"})

        await storage.delete(["foo"])
        data = await storage.read(["test"])
        assert len(data.keys()) == 1
        data = await storage.read(["foo"])
        assert not data.keys()

    @pytest.mark.asyncio
    async def test_memory_storage_delete_invalid_keys_should_do_nothing_and_not_affect_cached_data(
        self,
    ):
        storage = MemoryStorage({"test": "test"})

        await storage.delete(["foo", "bar"])
        data = await storage.read(["test"])
        assert len(data.keys()) == 1
