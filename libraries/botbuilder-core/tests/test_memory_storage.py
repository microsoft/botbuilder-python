# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import aiounittest

from botbuilder.core import MemoryStorage, StoreItem


class SimpleStoreItem(StoreItem):
    def __init__(self, counter=1, e_tag='*'):
        super(SimpleStoreItem, self).__init__()
        self.counter = counter
        self.e_tag = e_tag


class TestMemoryStorage(aiounittest.AsyncTestCase):
    def test_initializing_memory_storage_without_data_should_still_have_memory(self):
        storage = MemoryStorage()
        assert storage.memory is not None
        assert type(storage.memory) == dict

    def test_memory_storage__e_tag_should_start_at_0(self):
        storage = MemoryStorage()
        assert storage._e_tag == 0

    
    async def test_memory_storage_initialized_with_memory_should_have_accessible_data(self):
        storage = MemoryStorage({'test': SimpleStoreItem()})
        data = await storage.read(['test'])
        assert 'test' in data
        assert data['test'].counter == 1
        assert len(data.keys()) == 1

    
    async def test_memory_storage_read_should_return_data_with_valid_key(self):
        storage = MemoryStorage()
        await storage.write({'user': SimpleStoreItem()})

        data = await storage.read(['user'])
        assert 'user' in data
        assert data['user'].counter == 1
        assert len(data.keys()) == 1
        assert storage._e_tag == 1
        assert int(data['user'].e_tag) == 0

    
    async def test_memory_storage_write_should_add_new_value(self):
        storage = MemoryStorage()
        aux = {'user': SimpleStoreItem(counter=1)}
        await storage.write(aux)

        data = await storage.read(['user'])
        assert 'user' in data
        assert data['user'].counter == 1
        
    
    async def test_memory_storage_write_should_overwrite_when_new_e_tag_is_an_asterisk_1(self):
        storage = MemoryStorage()
        await storage.write({'user': SimpleStoreItem(e_tag='1')})

        await storage.write({'user': SimpleStoreItem(counter=10, e_tag='*')})
        data = await storage.read(['user'])
        assert data['user'].counter == 10

    
    async def test_memory_storage_write_should_overwrite_when_new_e_tag_is_an_asterisk_2(self):
        storage = MemoryStorage()
        await storage.write({'user': SimpleStoreItem(e_tag='1')})

        await storage.write({'user': SimpleStoreItem(counter=5, e_tag='1')})
        data = await storage.read(['user'])
        assert data['user'].counter == 5

    async def test_memory_storage_read_with_invalid_key_should_return_empty_dict(self):
        storage = MemoryStorage()
        data = await storage.read(['test'])

        assert type(data) == dict
        assert len(data.keys()) == 0

    
    async def test_memory_storage_delete_should_delete_according_cached_data(self):
        storage = MemoryStorage({'test': 'test'})
        try:
            await storage.delete(['test'])
        except Exception as e:
            raise e
        else:
            data = await storage.read(['test'])

            assert type(data) == dict
            assert len(data.keys()) == 0

    
    async def test_memory_storage_delete_should_delete_multiple_values_when_given_multiple_valid_keys(self):
        storage = MemoryStorage({'test': SimpleStoreItem(), 'test2': SimpleStoreItem(2, '2')})

        await storage.delete(['test', 'test2'])
        data = await storage.read(['test', 'test2'])
        assert len(data.keys()) == 0

    
    async def test_memory_storage_delete_should_delete_values_when_given_multiple_valid_keys_and_ignore_other_data(self):
        storage = MemoryStorage({'test': SimpleStoreItem(),
                                 'test2': SimpleStoreItem(2, '2'),
                                 'test3': SimpleStoreItem(3, '3')})

        await storage.delete(['test', 'test2'])
        data = await storage.read(['test', 'test2', 'test3'])
        assert len(data.keys()) == 1

    
    async def test_memory_storage_delete_invalid_key_should_do_nothing_and_not_affect_cached_data(self):
        storage = MemoryStorage({'test': 'test'})

        await storage.delete(['foo'])
        data = await storage.read(['test'])
        assert len(data.keys()) == 1
        data = await storage.read(['foo'])
        assert len(data.keys()) == 0

    
    async def test_memory_storage_delete_invalid_keys_should_do_nothing_and_not_affect_cached_data(self):
        storage = MemoryStorage({'test': 'test'})

        await storage.delete(['foo', 'bar'])
        data = await storage.read(['test'])
        assert len(data.keys()) == 1
