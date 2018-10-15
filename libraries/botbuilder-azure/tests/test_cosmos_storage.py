# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import pytest
from botbuilder.core import StoreItem
from botbuilder.azure import (CosmosDbStorage, CosmosDbConfig)

# local cosmosdb emulator instance cosmos_db_config
cosmos_db_config = CosmosDbConfig(
    endpoint='https://localhost:8081',
    masterkey='C2y6yDjf5/R+ob0N8A7Cgv30VRDJIWEHLM+4QDU5DE2nQ9nDuVTqobD4b8mGGyPMbIZnqyMsEcaGQy67XIw/Jw==',
    database='test-db',
    container='bot-storage'
)
emulator_running = False

async def reset():
    storage = CosmosDbStorage(cosmos_db_config)
    storage.client.DeleteDatabase(
        database_link='dbs/' + cosmos_db_config.database,
        ignore_errors=True)


class SimpleStoreItem(StoreItem):
    def __init__(self, counter=1, e_tag='*'):
        super(SimpleStoreItem, self).__init__()
        self.counter = counter
        self.e_tag = e_tag


class TestCosmosDbStorage:

    @pytest.mark.asyncio
    async def test_cosmos_storage_init_should_error_without_cosmos_db_config(self):
        try:
            CosmosDbStorage(CosmosDbConfig())
        except Exception as e:
            assert e

    @pytest.mark.skipif(not emulator_running, reason='Needs the emulator to run.')
    async def test_cosmos_storage_init_should_work_with_just_endpoint_and_key(self):
        storage = CosmosDbStorage(CosmosDbConfig(endpoint=cosmos_db_config.endpoint, masterkey=cosmos_db_config.masterkey))
        await storage.write({'user': SimpleStoreItem()})
        data = await storage.read(['user'])
        assert 'user' in data
        assert data['user'].counter == 1
        assert len(data.keys()) == 1

    @pytest.mark.skipif(not emulator_running, reason='Needs the emulator to run.')
    async def test_cosmos_storage_read_should_return_data_with_valid_key(self):
        await reset()
        storage = CosmosDbStorage(cosmos_db_config)
        await storage.write({'user': SimpleStoreItem()})

        data = await storage.read(['user'])
        assert 'user' in data
        assert data['user'].counter == 1
        assert len(data.keys()) == 1

    @pytest.mark.skipif(not emulator_running, reason='Needs the emulator to run.')
    async def test_cosmos_storage_read_update_should_return_new_etag(self):
        await reset()
        storage = CosmosDbStorage(cosmos_db_config)
        await storage.write({'test': SimpleStoreItem(counter=1)})
        data_result = await storage.read(['test'])
        data_result['test'].counter = 2
        await storage.write(data_result)
        data_updated = await storage.read(['test'])
        assert data_updated['test'].counter == 2
        assert data_updated['test'].e_tag != data_result['test'].e_tag

    @pytest.mark.skipif(not emulator_running, reason='Needs the emulator to run.')
    async def test_cosmos_storage_read_with_invalid_key_should_return_empty_dict(self):
        await reset()
        storage = CosmosDbStorage(cosmos_db_config)
        data = await storage.read(['test'])

        assert type(data) == dict
        assert len(data.keys()) == 0

    @pytest.mark.skipif(not emulator_running, reason='Needs the emulator to run.')
    async def test_cosmos_storage_read_no_key_should_throw(self):
        try:
            await reset()
            storage = CosmosDbStorage(cosmos_db_config)
            await storage.read([])
        except Exception as e:
            assert e

    @pytest.mark.skipif(not emulator_running, reason='Needs the emulator to run.')
    async def test_cosmos_storage_write_should_add_new_value(self):
        await reset()
        storage = CosmosDbStorage(cosmos_db_config)
        await storage.write({'user': SimpleStoreItem(counter=1)})

        data = await storage.read(['user'])
        assert 'user' in data
        assert data['user'].counter == 1

    @pytest.mark.skipif(not emulator_running, reason='Needs the emulator to run.')
    async def test_cosmos_storage_write_should_overwrite_when_new_e_tag_is_an_asterisk(self):
        await reset()
        storage = CosmosDbStorage(cosmos_db_config)
        await storage.write({'user': SimpleStoreItem()})

        await storage.write({'user': SimpleStoreItem(counter=10, e_tag='*')})
        data = await storage.read(['user'])
        assert data['user'].counter == 10

    @pytest.mark.skipif(not emulator_running, reason='Needs the emulator to run.')
    async def test_cosmos_storage_write_batch_operation(self):
        await reset()
        storage = CosmosDbStorage(cosmos_db_config)
        await storage.write(
            {'batch1': SimpleStoreItem(counter=1),
            'batch2': SimpleStoreItem(counter=1),
            'batch3': SimpleStoreItem(counter=1)}
            )
        data = await storage.read(['batch1', 'batch2', 'batch3'])
        assert len(data.keys()) == 3
        assert data['batch1']
        assert data['batch2']
        assert data['batch3']
        assert data['batch1'].counter == 1
        assert data['batch2'].counter == 1
        assert data['batch3'].counter == 1
        assert data['batch1'].e_tag
        assert data['batch2'].e_tag
        assert data['batch3'].e_tag
        await storage.delete(['batch1', 'batch2', 'batch3'])
        data = await storage.read(['batch1', 'batch2', 'batch3'])
        assert len(data.keys()) == 0

    @pytest.mark.skipif(not emulator_running, reason='Needs the emulator to run.')
    async def test_cosmos_storage_write_crazy_keys_work(self):
        await reset()
        storage = CosmosDbStorage(cosmos_db_config)
        crazy_key = '!@#$%^&*()_+??><":QASD~`'
        await storage.write({crazy_key: SimpleStoreItem(counter=1)})
        data = await storage.read([crazy_key])
        assert len(data.keys()) == 1
        assert data[crazy_key]
        assert data[crazy_key].counter == 1
        assert data[crazy_key].e_tag

    @pytest.mark.skipif(not emulator_running, reason='Needs the emulator to run.')
    async def test_cosmos_storage_delete_should_delete_according_cached_data(self):
        await reset()
        storage = CosmosDbStorage(cosmos_db_config)
        await storage.write({'test': SimpleStoreItem()})
        try:
            await storage.delete(['test'])
        except Exception as e:
            raise e
        else:
            data = await storage.read(['test'])

            assert type(data) == dict
            assert len(data.keys()) == 0

    @pytest.mark.skipif(not emulator_running, reason='Needs the emulator to run.')
    async def test_cosmos_storage_delete_should_delete_multiple_values_when_given_multiple_valid_keys(self):
        await reset()
        storage = CosmosDbStorage(cosmos_db_config)
        await storage.write({'test': SimpleStoreItem(), 'test2': SimpleStoreItem(2)})

        await storage.delete(['test', 'test2'])
        data = await storage.read(['test', 'test2'])
        assert len(data.keys()) == 0

    @pytest.mark.skipif(not emulator_running, reason='Needs the emulator to run.')
    async def test_cosmos_storage_delete_should_delete_values_when_given_multiple_valid_keys_and_ignore_other_data(self):
        await reset()
        storage = CosmosDbStorage(cosmos_db_config)
        await storage.write({'test': SimpleStoreItem(),
                                 'test2': SimpleStoreItem(counter=2),
                                 'test3': SimpleStoreItem(counter=3)})

        await storage.delete(['test', 'test2'])
        data = await storage.read(['test', 'test2', 'test3'])
        assert len(data.keys()) == 1

    @pytest.mark.skipif(not emulator_running, reason='Needs the emulator to run.')
    async def test_cosmos_storage_delete_invalid_key_should_do_nothing_and_not_affect_cached_data(self):
        await reset()
        storage = CosmosDbStorage(cosmos_db_config)
        await storage.write({'test': SimpleStoreItem()})

        await storage.delete(['foo'])
        data = await storage.read(['test'])
        assert len(data.keys()) == 1
        data = await storage.read(['foo'])
        assert len(data.keys()) == 0

    @pytest.mark.skipif(not emulator_running, reason='Needs the emulator to run.')
    async def test_cosmos_storage_delete_invalid_keys_should_do_nothing_and_not_affect_cached_data(self):
        await reset()
        storage = CosmosDbStorage(cosmos_db_config)
        await storage.write({'test': SimpleStoreItem()})

        await storage.delete(['foo', 'bar'])
        data = await storage.read(['test'])
        assert len(data.keys()) == 1
