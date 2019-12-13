"""CosmosDB Middleware for Python Bot Framework.

This is middleware to store items in CosmosDB.
Part of the Azure Bot Framework in Python.
"""

# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
from typing import Dict, List
from threading import Lock
import json

from azure.cosmos import documents, http_constants
from jsonpickle.pickler import Pickler
from jsonpickle.unpickler import Unpickler
import azure.cosmos.cosmos_client as cosmos_client  # pylint: disable=no-name-in-module,import-error
import azure.cosmos.errors as cosmos_errors  # pylint: disable=no-name-in-module,import-error
from botbuilder.core.storage import Storage
from botbuilder.azure import CosmosDbKeyEscape


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


class CosmosDbPartitionedStorage(Storage):
    """The class for partitioned CosmosDB middleware for the Azure Bot Framework."""

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
            raise Exception("Keys are required when reading")

        await self.initialize()

        store_items = {}

        for key in keys:
            try:
                escaped_key = CosmosDbKeyEscape.sanitize_key(
                    key, self.config.key_suffix, self.config.compatibility_mode
                )

                read_item_response = self.client.ReadItem(
                    self.__item_link(escaped_key), self.__get_partition_key(escaped_key)
                )
                document_store_item = read_item_response
                if document_store_item:
                    store_items[document_store_item["realId"]] = self.__create_si(
                        document_store_item
                    )
            # When an item is not found a CosmosException is thrown, but we want to
            # return an empty collection so in this instance we catch and do not rethrow.
            # Throw for any other exception.
            except cosmos_errors.HTTPFailure as err:
                if (
                    err.status_code
                    == cosmos_errors.http_constants.StatusCodes.NOT_FOUND
                ):
                    continue
                raise err
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

        for (key, change) in changes.items():
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

            access_condition = {
                "accessCondition": {"type": "IfMatch", "condition": e_tag}
            }
            options = (
                access_condition if e_tag != "*" and e_tag and e_tag != "" else None
            )
            try:
                self.client.UpsertItem(
                    database_or_Container_link=self.__container_link,
                    document=doc,
                    options=options,
                )
            except cosmos_errors.HTTPFailure as err:
                raise err
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
                self.client.DeleteItem(
                    document_link=self.__item_link(escaped_key),
                    options=self.__get_partition_key(escaped_key),
                )
            except cosmos_errors.HTTPFailure as err:
                if (
                    err.status_code
                    == cosmos_errors.http_constants.StatusCodes.NOT_FOUND
                ):
                    continue
                raise err
            except Exception as err:
                raise err

    async def initialize(self):
        if not self.container:
            if not self.client:
                self.client = cosmos_client.CosmosClient(
                    self.config.cosmos_db_endpoint,
                    {"masterKey": self.config.auth_key},
                    self.config.cosmos_client_options.get("connection_policy", None),
                    self.config.cosmos_client_options.get("consistency_level", None),
                )

            if not self.database:
                with self.__lock:
                    try:
                        if not self.database:
                            self.database = self.client.CreateDatabase(
                                {"id": self.config.database_id}
                            )
                    except cosmos_errors.HTTPFailure:
                        self.database = self.client.ReadDatabase(
                            "dbs/" + self.config.database_id
                        )

            self.__get_or_create_container()

    def __get_or_create_container(self):
        with self.__lock:
            container_def = {
                "id": self.config.container_id,
                "partitionKey": {
                    "paths": ["/id"],
                    "kind": documents.PartitionKind.Hash,
                },
            }
            try:
                if not self.container:
                    self.container = self.client.CreateContainer(
                        "dbs/" + self.database["id"],
                        container_def,
                        {"offerThroughput": self.config.container_throughput},
                    )
            except cosmos_errors.HTTPFailure as err:
                if err.status_code == http_constants.StatusCodes.CONFLICT:
                    self.container = self.client.ReadContainer(
                        "dbs/" + self.database["id"] + "/colls/" + container_def["id"]
                    )
                    if "partitionKey" not in self.container:
                        self.compatability_mode_partition_key = True
                    else:
                        paths = self.container["partitionKey"]["paths"]
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
        return None if self.compatability_mode_partition_key else {"partitionKey": key}

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

    def __item_link(self, identifier) -> str:
        """Return the item link of a item in the container.

        :param identifier:
        :return str:
        """
        return self.__container_link + "/docs/" + identifier

    @property
    def __container_link(self) -> str:
        """Return the container link in the database.

        :param:
        :return str:
        """
        return self.__database_link + "/colls/" + self.config.container_id

    @property
    def __database_link(self) -> str:
        """Return the database link.

        :return str:
        """
        return "dbs/" + self.config.database_id
