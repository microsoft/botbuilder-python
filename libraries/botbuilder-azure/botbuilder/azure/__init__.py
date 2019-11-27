# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

from .about import __version__
from .cosmosdb_storage import CosmosDbStorage, CosmosDbConfig, CosmosDbKeyEscape
from .cosmosdb_partitioned_storage import (
    CosmosDbPartitionedStorage,
    CosmosDbPartitionedConfig,
)
from .blob_storage import BlobStorage, BlobStorageSettings

__all__ = [
    "BlobStorage",
    "BlobStorageSettings",
    "CosmosDbStorage",
    "CosmosDbConfig",
    "CosmosDbKeyEscape",
    "CosmosDbPartitionedStorage",
    "CosmosDbPartitionedConfig",
    "__version__",
]
