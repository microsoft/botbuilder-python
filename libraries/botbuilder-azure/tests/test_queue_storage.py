# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import unittest
import aiounittest
from jsonpickle import decode

from botbuilder.azure import AzureQueueStorage

EMULATOR_RUNNING = False

# This connection string is to connect to local Azure Storage Emulator.
CONNECTION_STRING = (
    "AccountName=devstoreaccount1;"
    "AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr"
    "/KBHBeksoGMGw==;DefaultEndpointsProtocol=http;"
    "BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;"
    "QueueEndpoint=http://127.0.0.1:10001/devstoreaccount1;"
    "TableEndpoint=http://127.0.0.1:10002/devstoreaccount1;"
)
QUEUE_NAME = "queue"


class TestAzureQueueStorageConstructor:
    def test_queue_storage_init_should_error_without_connection_string(self):
        try:
            # pylint: disable=no-value-for-parameter
            AzureQueueStorage()
        except Exception as error:
            assert error

    def test_queue_storage_init_should_error_without_queue_name(self):
        try:
            # pylint: disable=no-value-for-parameter
            AzureQueueStorage(queues_storage_connection_string="somestring")
        except Exception as error:
            assert error


class TestAzureQueueStorage(aiounittest.AsyncTestCase):
    @unittest.skipIf(not EMULATOR_RUNNING, reason="Needs the emulator to run.")
    async def test_returns_read_receipt(self):
        message = {"string": "test", "object": {"string2": "test2"}, "number": 99}
        queue = AzureQueueStorage(CONNECTION_STRING, QUEUE_NAME)

        receipt = await queue.queue_activity(message)
        decoded = decode(receipt)

        assert decoded.id is not None
        assert decode(decoded.content) == message
