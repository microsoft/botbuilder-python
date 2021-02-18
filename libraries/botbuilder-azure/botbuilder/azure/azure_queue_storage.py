# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from azure.core.exceptions import ResourceExistsError
from azure.storage.queue.aio import QueueClient
from jsonpickle import encode

from botbuilder.core import QueueStorage
from botbuilder.schema import Activity


class AzureQueueStorage(QueueStorage):
    def __init__(self, queues_storage_connection_string: str, queue_name: str):
        if not queues_storage_connection_string:
            raise Exception("queues_storage_connection_string cannot be empty.")
        if not queue_name:
            raise Exception("queue_name cannot be empty.")

        self.__queue_client = QueueClient.from_connection_string(
            queues_storage_connection_string, queue_name
        )

        self.__initialized = False

    async def _initialize(self):
        if self.__initialized is False:
            # This should only happen once - assuming this is a singleton.
            # There is no `create_queue_if_exists` or `exists` method, so we need to catch the ResourceExistsError.
            try:
                await self.__queue_client.create_queue()
            except ResourceExistsError:
                pass
            self.__initialized = True
        return self.__initialized

    async def queue_activity(
        self,
        activity: Activity,
        visibility_timeout: int = None,
        time_to_live: int = None,
    ) -> str:
        """
        Enqueues an Activity for later processing. The visibility timeout specifies how long the message should be
        visible to Dequeue and Peek operations.

        :param activity: The activity to be queued for later processing.
        :type activity: :class:`botbuilder.schema.Activity`
        :param visibility_timeout: Visibility timeout in seconds. Optional with a default value of 0.
            Cannot be larger than 7 days.
        :type visibility_timeout: int
        :param time_to_live: Specifies the time-to-live interval for the message in seconds.
        :type time_to_live: int

        :returns: QueueMessage as a JSON string.
        :rtype: :class:`azure.storage.queue.QueueMessage`
        """
        await self._initialize()

        # Encode the activity as a JSON string.
        message = encode(activity)

        receipt = await self.__queue_client.send_message(
            message, visibility_timeout=visibility_timeout, time_to_live=time_to_live
        )

        # Encode the QueueMessage receipt as a JSON string.
        return encode(receipt)
