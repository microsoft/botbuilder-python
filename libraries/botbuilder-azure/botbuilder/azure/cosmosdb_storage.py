"""CosmosDB Middleware for Python Bot Framework.

This is middleware to store items in CosmosDB.
Part of the Azure Bot Framework in Python.
"""

# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
from hashlib import sha256
from typing import Dict, List
from threading import Semaphore
import json
from jsonpickle.pickler import Pickler
from jsonpickle.unpickler import Unpickler
import azure.cosmos.cosmos_client as cosmos_client  # pylint: disable=no-name-in-module,import-error
import azure.cosmos.errors as cosmos_errors  # pylint: disable=no-name-in-module,import-error
from botbuilder.core.storage import Storage


class CosmosDbConfig:
    """The class for CosmosDB configuration for the Azure Bot Framework."""

    def __init__(
        self,
        endpoint: str = None,
        masterkey: str = None,
        database: str = None,
        container: str = None,
        partition_key: str = None,
        database_creation_options: dict = None,
        container_creation_options: dict = None,
        **kwargs,
    ):
        """Create the Config object.

        :param endpoint:
        :param masterkey:
        :param database:
        :param container:
        :param filename:
        :return CosmosDbConfig:
        """
        self.__config_file = kwargs.get("filename")
        if self.__config_file:
            kwargs = json.load(open(self.__config_file))
        self.endpoint = endpoint or kwargs.get("endpoint")
        self.masterkey = masterkey or kwargs.get("masterkey")
        self.database = database or kwargs.get("database", "bot_db")
        self.container = container or kwargs.get("container", "bot_container")
        self.partition_key = partition_key or kwargs.get("partition_key")
        self.database_creation_options = database_creation_options or kwargs.get(
            "database_creation_options"
        )
        self.container_creation_options = container_creation_options or kwargs.get(
            "container_creation_options"
        )


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


class CosmosDbStorage(Storage):
    """The class for CosmosDB middleware for the Azure Bot Framework."""

    def __init__(
        self, config: CosmosDbConfig, client: cosmos_client.CosmosClient = None
    ):
        """Create the storage object.

        :param config:
        """
        super(CosmosDbStorage, self).__init__()
        self.config = config
        self.client = client or cosmos_client.CosmosClient(
            self.config.endpoint, {"masterKey": self.config.masterkey}
        )
        # these are set by the functions that check
        # the presence of the database and container or creates them
        self.database = None
        self.container = None
        self._database_creation_options = config.database_creation_options
        self._container_creation_options = config.container_creation_options
        self.__semaphore = Semaphore()

    async def read(self, keys: List[str]) -> Dict[str, object]:
        """Read storeitems from storage.

        :param keys:
        :return dict:
        """
        try:
            # check if the database and container exists and if not create
            if not self.__container_exists:
                self.__create_db_and_container()
            if keys:
                # create the parameters object
                parameters = [
                    {
                        "name": f"@id{i}",
                        "value": f"{CosmosDbKeyEscape.sanitize_key(key)}",
                    }
                    for i, key in enumerate(keys)
                ]
                # get the names of the params
                parameter_sequence = ",".join(param.get("name") for param in parameters)
                # create the query
                query = {
                    "query": f"SELECT c.id, c.realId, c.document, c._etag FROM c WHERE c.id in ({parameter_sequence})",
                    "parameters": parameters,
                }

                if self.config.partition_key:
                    options = {"partitionKey": self.config.partition_key}
                else:
                    options = {"enableCrossPartitionQuery": True}

                # run the query and store the results as a list
                results = list(
                    self.client.QueryItems(self.__container_link, query, options)
                )
                # return a dict with a key and an object
                return {r.get("realId"): self.__create_si(r) for r in results}

            # No keys passed in, no result to return.
            return {}
        except TypeError as error:
            raise error

    async def write(self, changes: Dict[str, object]):
        """Save storeitems to storage.

        :param changes:
        :return:
        """
        if changes is None:
            raise Exception("Changes are required when writing")
        if not changes:
            return
        try:
            # check if the database and container exists and if not create
            if not self.__container_exists:
                self.__create_db_and_container()
                # iterate over the changes
            for (key, change) in changes.items():
                # store the e_tag
                e_tag = None
                if isinstance(change, dict):
                    e_tag = change.get("e_tag", None)
                elif hasattr(change, "e_tag"):
                    e_tag = change.e_tag
                # create the new document
                doc = {
                    "id": CosmosDbKeyEscape.sanitize_key(key),
                    "realId": key,
                    "document": self.__create_dict(change),
                }
                if e_tag == "":
                    raise Exception("cosmosdb_storage.write(): etag missing")
                # the e_tag will be * for new docs so do an insert
                if e_tag == "*" or not e_tag:
                    self.client.UpsertItem(
                        database_or_Container_link=self.__container_link,
                        document=doc,
                        options={"disableAutomaticIdGeneration": True},
                    )
                # if we have an etag, do opt. concurrency replace
                elif e_tag:
                    access_condition = {"type": "IfMatch", "condition": e_tag}
                    self.client.ReplaceItem(
                        document_link=self.__item_link(
                            CosmosDbKeyEscape.sanitize_key(key)
                        ),
                        new_document=doc,
                        options={"accessCondition": access_condition},
                    )
        except Exception as error:
            raise error

    async def delete(self, keys: List[str]):
        """Remove storeitems from storage.

        :param keys:
        :return:
        """
        try:
            # check if the database and container exists and if not create
            if not self.__container_exists:
                self.__create_db_and_container()

            options = {}
            if self.config.partition_key:
                options["partitionKey"] = self.config.partition_key

            # call the function for each key
            for key in keys:
                self.client.DeleteItem(
                    document_link=self.__item_link(CosmosDbKeyEscape.sanitize_key(key)),
                    options=options,
                )
                # print(res)
        except cosmos_errors.HTTPFailure as http_failure:
            # print(h.status_code)
            if http_failure.status_code != 404:
                raise http_failure
        except TypeError as error:
            raise error

    def __create_si(self, result) -> object:
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

    def __create_dict(self, store_item: object) -> Dict:
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
        return self.__database_link + "/colls/" + self.container

    @property
    def __database_link(self) -> str:
        """Return the database link.

        :return str:
        """
        return "dbs/" + self.database

    @property
    def __container_exists(self) -> bool:
        """Return whether the database and container have been created.

        :return bool:
        """
        return self.database and self.container

    def __create_db_and_container(self):
        """Call the get or create methods."""
        with self.__semaphore:
            db_id = self.config.database
            container_name = self.config.container
            self.database = self._get_or_create_database(self.client, db_id)
            self.container = self._get_or_create_container(self.client, container_name)

    def _get_or_create_database(  # pylint: disable=invalid-name
        self, doc_client, id
    ) -> str:
        """Return the database link.

        Check if the database exists or create the database.

        :param doc_client:
        :param id:
        :return str:
        """
        # query CosmosDB for a database with that name/id
        dbs = list(
            doc_client.QueryDatabases(
                {
                    "query": "SELECT * FROM r WHERE r.id=@id",
                    "parameters": [{"name": "@id", "value": id}],
                }
            )
        )
        # if there are results, return the first (database names are unique)
        if dbs:
            return dbs[0]["id"]

        # create the database if it didn't exist
        res = doc_client.CreateDatabase({"id": id}, self._database_creation_options)
        return res["id"]

    def _get_or_create_container(self, doc_client, container) -> str:
        """Return the container link.

        Check if the container exists or create the container.

        :param doc_client:
        :param container:
        :return str:
        """
        # query CosmosDB for a container in the database with that name
        containers = list(
            doc_client.QueryContainers(
                self.__database_link,
                {
                    "query": "SELECT * FROM r WHERE r.id=@id",
                    "parameters": [{"name": "@id", "value": container}],
                },
            )
        )
        # if there are results, return the first (container names are unique)
        if containers:
            return containers[0]["id"]

        # Create a container if it didn't exist
        res = doc_client.CreateContainer(
            self.__database_link, {"id": container}, self._container_creation_options
        )
        return res["id"]
