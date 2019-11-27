# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import azure.cosmos.errors as cosmos_errors
from azure.cosmos import documents
import pytest
from botbuilder.azure import CosmosDbPartitionedStorage, CosmosDbPartitionedConfig
from botbuilder.testing import StorageBaseTests

EMULATOR_RUNNING = False


def get_settings() -> CosmosDbPartitionedConfig:
    return CosmosDbPartitionedConfig(
        cosmos_db_endpoint="https://localhost:8081",
        auth_key="C2y6yDjf5/R+ob0N8A7Cgv30VRDJIWEHLM+4QDU5DE2nQ9nDuVTqobD4b8mGGyPMbIZnqyMsEcaGQy67XIw/Jw==",
        database_id="test-db",
        container_id="bot-storage",
    )


def get_storage():
    return CosmosDbPartitionedStorage(get_settings())


async def reset():
    storage = CosmosDbPartitionedStorage(get_settings())
    await storage.initialize()
    try:
        storage.client.DeleteDatabase(database_link="dbs/" + get_settings().database_id)
    except cosmos_errors.HTTPFailure:
        pass


class TestCosmosDbPartitionedStorageConstructor:
    @pytest.mark.skipif(not EMULATOR_RUNNING, reason="Needs the emulator to run.")
    @pytest.mark.asyncio
    async def test_raises_error_when_instantiated_with_no_arguments(self):
        try:
            # noinspection PyArgumentList
            # pylint: disable=no-value-for-parameter
            CosmosDbPartitionedStorage()
        except Exception as error:
            assert error

    @pytest.mark.skipif(not EMULATOR_RUNNING, reason="Needs the emulator to run.")
    @pytest.mark.asyncio
    async def test_raises_error_when_no_endpoint_provided(self):
        no_endpoint = get_settings()
        no_endpoint.cosmos_db_endpoint = None
        try:
            CosmosDbPartitionedStorage(no_endpoint)
        except Exception as error:
            assert error

    @pytest.mark.skipif(not EMULATOR_RUNNING, reason="Needs the emulator to run.")
    @pytest.mark.asyncio
    async def test_raises_error_when_no_auth_key_provided(self):
        no_auth_key = get_settings()
        no_auth_key.auth_key = None
        try:
            CosmosDbPartitionedStorage(no_auth_key)
        except Exception as error:
            assert error

    @pytest.mark.skipif(not EMULATOR_RUNNING, reason="Needs the emulator to run.")
    @pytest.mark.asyncio
    async def test_raises_error_when_no_database_id_provided(self):
        no_database_id = get_settings()
        no_database_id.database_id = None
        try:
            CosmosDbPartitionedStorage(no_database_id)
        except Exception as error:
            assert error

    @pytest.mark.skipif(not EMULATOR_RUNNING, reason="Needs the emulator to run.")
    @pytest.mark.asyncio
    async def test_raises_error_when_no_container_id_provided(self):
        no_container_id = get_settings()
        no_container_id.container_id = None
        try:
            CosmosDbPartitionedStorage(no_container_id)
        except Exception as error:
            assert error

    @pytest.mark.skipif(not EMULATOR_RUNNING, reason="Needs the emulator to run.")
    @pytest.mark.asyncio
    async def test_passes_cosmos_client_options(self):
        settings_with_options = get_settings()

        connection_policy = documents.ConnectionPolicy()
        connection_policy.DisableSSLVerification = True

        settings_with_options.cosmos_client_options = {
            "connection_policy": connection_policy,
            "consistency_level": documents.ConsistencyLevel.Eventual,
        }

        client = CosmosDbPartitionedStorage(settings_with_options)
        await client.initialize()

        assert client.client.connection_policy.DisableSSLVerification is True
        assert (
            client.client.default_headers["x-ms-consistency-level"]
            == documents.ConsistencyLevel.Eventual
        )


class TestCosmosDbPartitionedStorageBaseStorageTests:
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
