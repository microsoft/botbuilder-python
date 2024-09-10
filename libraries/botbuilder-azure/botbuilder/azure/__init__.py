# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

from .about import __version__
from .azure_queue_storage import AzureQueueStorage
from .cosmosdb_partitioned_storage import (
    CosmosDbPartitionedStorage,
    CosmosDbPartitionedConfig,
    CosmosDbKeyEscape,
)
from .blob_storage import BlobStorage, BlobStorageSettings

__all__ = [
    "AzureQueueStorage",
    "BlobStorage",
    "BlobStorageSettings",
    "CosmosDbKeyEscape",
    "CosmosDbPartitionedStorage",
    "CosmosDbPartitionedConfig",
    "__version__",
]
