# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from abc import ABC, abstractmethod
from botbuilder.schema import Activity


class QueueStorage(ABC):
    """
    A base class for enqueueing an Activity for later processing.
    """

    @abstractmethod
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

        :returns: String representing the read receipt.
        """
        raise NotImplementedError()
