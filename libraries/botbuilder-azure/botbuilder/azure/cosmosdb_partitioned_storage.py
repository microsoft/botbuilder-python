"""Implements a CosmosDB based storage provider using partitioning for a bot.
"""

# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
from typing import Dict, List
from threading import Lock
import json
from hashlib import sha256
from azure.core import MatchConditions
from azure.cosmos import documents, http_constants
from jsonpickle.pickler import Pickler
from jsonpickle.unpickler import Unpickler
import azure.cosmos.cosmos_client as cosmos_client  # pylint: disable=no-name-in-module,import-error
import azure.cosmos.exceptions as cosmos_exceptions
from botbuilder.core.storage import Storage


class CosmosDbPartitionedConfig:
    """The class for partitioned CosmosDB configuration for the Azure Bot Framework."""

    def __init__(
        self,
        cosmos_db_endpoint: str = None,
        auth_key: str = None,
        database_id: str = None,
        container_id: str = None,
        cosmos_client_options: dict = None,
        container_throughput: int = 400,
        key_suffix: str = "",
        compatibility_mode: bool = False,
        **kwargs,
    ):
        """Create the Config object.

        :param cosmos_db_endpoint: The CosmosDB endpoint.
        :param auth_key: The authentication key for Cosmos DB.
        :param database_id: The database identifier for Cosmos DB instance.
        :param container_id: The container identifier.
        :param cosmos_client_options: The options for the CosmosClient. Currently only supports connection_policy and
            consistency_level
        :param container_throughput: The throughput set when creating the Container. Defaults to 400.
        :param key_suffix: The suffix to be added to every key. The keySuffix must contain only valid ComosDb
            key characters. (e.g. not: '\\', '?', '/', '#', '*')
        :param compatibility_mode: True if keys should be truncated in order to support previous CosmosDb
            max key length of 255.
        :return CosmosDbPartitionedConfig:
        """
        self.__config_file = kwargs.get("filename")
        if self.__config_file:
            kwargs = json.load(open(self.__config_file))
        self.cosmos_db_endpoint = cosmos_db_endpoint or kwargs.get("cosmos_db_endpoint")
        self.auth_key = auth_key or kwargs.get("auth_key")
        self.database_id = database_id or kwargs.get("database_id")
        self.container_id = container_id or kwargs.get("container_id")
        self.cosmos_client_options = cosmos_client_options or kwargs.get(
            "cosmos_client_options", {}
        )
        self.container_throughput = container_throughput or kwargs.get(
            "container_throughput"
        )
        self.key_suffix = key_suffix or kwargs.get("key_suffix")
        self.compatibility_mode = compatibility_mode or kwargs.get("compatibility_mode")


class CosmosDbKeyEscape:
    @staticmethod
    def sanitize_key(
        key: str, key_suffix: str = "", compatibility_mode: bool = True
    ) -> str:
        """Return the sanitized key.

        Replace characters that are not allowed in keys in Cosmos.

        :param key: The provided key to be escaped.
        :param key_suffix: The string to add a the end of all RowKeys.
        :param compatibility_mode: True if keys should be truncated in order to support previous CosmosDb
            max key length of 255.  This behavior can be overridden by setting
            cosmosdb_partitioned_config.compatibility_mode to False.
        :return str:
        """
        # forbidden characters
        bad_chars = ["\\", "?", "/", "#", "\t", "\n", "\r", "*"]
        # replace those with with '*' and the
        # Unicode code point of the character and return the new string
        key = "".join(map(lambda x: "*" + str(ord(x)) if x in bad_chars else x, key))

        if key_suffix is None:
            key_suffix = ""

        return CosmosDbKeyEscape.truncate_key(f"{key}{key_suffix}", compatibility_mode)

    @staticmethod
    def truncate_key(key: str, compatibility_mode: bool = True) -> str:
        max_key_len = 255

        if not compatibility_mode:
            return key

        if len(key) > max_key_len:
            aux_hash = sha256(key.encode("utf-8"))
            aux_hex = aux_hash.hexdigest()

            key = key[0 : max_key_len - len(aux_hex)] + aux_hex

        return key


class CosmosDbPartitionedStorage(Storage):
    """A CosmosDB based storage provider using partitioning for a bot."""

    def __init__(self, config: CosmosDbPartitionedConfig):
        """Create the storage object.

        :param config:
        """
        super(CosmosDbPartitionedStorage, self).__init__()
        self.config = config
        self.client = None
        self.database = None
        self.container = None
        self.compatability_mode_partition_key = False
        # Lock used for synchronizing container creation
        self.__lock = Lock()
        if config.key_suffix is None:
            config.key_suffix = ""
        if not config.key_suffix.__eq__(""):
            if config.compatibility_mode:
                raise Exception(
                    "compatibilityMode cannot be true while using a keySuffix."
                )
            suffix_escaped = CosmosDbKeyEscape.sanitize_key(config.key_suffix)
            if not suffix_escaped.__eq__(config.key_suffix):
                raise Exception(
                    f"Cannot use invalid Row Key characters: {config.key_suffix} in keySuffix."
                )

    async def read(self, keys: List[str]) -> Dict[str, object]:
        """Read storeitems from storage.

        :param keys:
        :return dict:
        """
        if not keys:
            # No keys passed in, no result to return. Back-compat with original CosmosDBStorage.
            return {}

        await self.initialize()

        store_items = {}

        for key in keys:
            try:
                escaped_key = CosmosDbKeyEscape.sanitize_key(
                    key, self.config.key_suffix, self.config.compatibility_mode
                )

                read_item_response = self.container.read_item(
                    escaped_key, self.__get_partition_key(escaped_key)
                )
                document_store_item = read_item_response
                if document_store_item:
                    store_items[document_store_item["realId"]] = self.__create_si(
                        document_store_item
                    )
            # When an item is not found a CosmosException is thrown, but we want to
            # return an empty collection so in this instance we catch and do not rethrow.
            # Throw for any other exception.
            except cosmos_exceptions.CosmosResourceNotFoundError:
                continue
            except Exception as err:
                raise err
        return store_items

    async def write(self, changes: Dict[str, object]):
        """Save storeitems to storage.

        :param changes:
        :return:
        """
        if changes is None:
            raise Exception("Changes are required when writing")
        if not changes:
            return

        await self.initialize()

        for key, change in changes.items():
            e_tag = None
            if isinstance(change, dict):
                e_tag = change.get("e_tag", None)
            elif hasattr(change, "e_tag"):
                e_tag = change.e_tag
            doc = {
                "id": CosmosDbKeyEscape.sanitize_key(
                    key, self.config.key_suffix, self.config.compatibility_mode
                ),
                "realId": key,
                "document": self.__create_dict(change),
            }
            if e_tag == "":
                raise Exception("cosmosdb_storage.write(): etag missing")

            access_condition = e_tag != "*" and e_tag and e_tag != ""

            try:
                self.container.upsert_item(
                    body=doc,
                    etag=e_tag if access_condition else None,
                    match_condition=(
                        MatchConditions.IfNotModified if access_condition else None
                    ),
                )
            except Exception as err:
                raise err

    async def delete(self, keys: List[str]):
        """Remove storeitems from storage.

        :param keys:
        :return:
        """
        await self.initialize()

        for key in keys:
            escaped_key = CosmosDbKeyEscape.sanitize_key(
                key, self.config.key_suffix, self.config.compatibility_mode
            )
            try:
                self.container.delete_item(
                    escaped_key,
                    self.__get_partition_key(escaped_key),
                )
            except cosmos_exceptions.CosmosResourceNotFoundError:
                continue
            except Exception as err:
                raise err

    async def initialize(self):
        if not self.container:
            if not self.client:
                connection_policy = self.config.cosmos_client_options.get(
                    "connection_policy", documents.ConnectionPolicy()
                )

                # kwargs 'connection_verify' is to handle CosmosClient overwriting the
                # ConnectionPolicy.DisableSSLVerification value.
                self.client = cosmos_client.CosmosClient(
                    self.config.cosmos_db_endpoint,
                    self.config.auth_key,
                    self.config.cosmos_client_options.get("consistency_level", None),
                    **{
                        "connection_policy": connection_policy,
                        "connection_verify": not connection_policy.DisableSSLVerification,
                    },
                )

            if not self.database:
                with self.__lock:
                    if not self.database:
                        self.database = self.client.create_database_if_not_exists(
                            self.config.database_id
                        )

            self.__get_or_create_container()

    def __get_or_create_container(self):
        with self.__lock:
            partition_key = {
                "paths": ["/id"],
                "kind": documents.PartitionKind.Hash,
            }
            try:
                if not self.container:
                    self.container = self.database.create_container(
                        self.config.container_id,
                        partition_key,
                        offer_throughput=self.config.container_throughput,
                    )
            except cosmos_exceptions.CosmosHttpResponseError as err:
                if err.status_code == http_constants.StatusCodes.CONFLICT:
                    self.container = self.database.get_container_client(
                        self.config.container_id
                    )
                    properties = self.container.read()
                    if "partitionKey" not in properties:
                        self.compatability_mode_partition_key = True
                    else:
                        paths = properties["partitionKey"]["paths"]
                        if "/partitionKey" in paths:
                            self.compatability_mode_partition_key = True
                        elif "/id" not in paths:
                            raise Exception(
                                f"Custom Partition Key Paths are not supported. {self.config.container_id} "
                                "has a custom Partition Key Path of {paths[0]}."
                            )

                else:
                    raise err

    def __get_partition_key(self, key: str) -> str:
        return None if self.compatability_mode_partition_key else key

    @staticmethod
    def __create_si(result) -> object:
        """Create an object from a result out of CosmosDB.

        :param result:
        :return object:
        """
        # get the document item from the result and turn into a dict
        doc = result.get("document")
        # read the e_tag from Cosmos
        if result.get("_etag"):
            doc["e_tag"] = result["_etag"]

        result_obj = Unpickler().restore(doc)

        # create and return the object
        return result_obj

    @staticmethod
    def __create_dict(store_item: object) -> Dict:
        """Return the dict of an object.

        This eliminates non_magic attributes and the e_tag.

        :param store_item:
        :return dict:
        """
        # read the content
        json_dict = Pickler().flatten(store_item)
        if "e_tag" in json_dict:
            del json_dict["e_tag"]

        # loop through attributes and write and return a dict
        return json_dict
