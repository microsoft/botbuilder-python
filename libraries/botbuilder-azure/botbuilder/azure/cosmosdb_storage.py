"""CosmosDB Middleware for Python Bot Framework.

This is middleware to store items in CosmosDB.
Part of the Azure Bot Framework in Python.
"""

# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import Dict, List
import json
from botbuilder.core.storage import Storage, StoreItem
import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.errors as cosmos_errors


class CosmosDbConfig():
    """The class for CosmosDB configuration for the Azure Bot Framework."""

    def __init__(self, **kwargs):
        """Create the Config object.

        :param endpoint:
        :param masterkey:
        :param database:
        :param container:
        :param filename:
        :return CosmosDbConfig:
        """
        self.__config_file = kwargs.pop('filename', None)
        if self.__config_file:
            kwargs = json.load(open(self.__config_file))
        self.endpoint = kwargs.pop('endpoint')
        self.masterkey = kwargs.pop('masterkey')
        self.database = kwargs.pop('database', 'bot_db')
        self.container = kwargs.pop('container', 'bot_container')


class CosmosDbStorage(Storage):
    """The class for CosmosDB middleware for the Azure Bot Framework."""

    def __init__(self, config: CosmosDbConfig):
        """Create the storage object.

        :param config:
        """
        super(CosmosDbStorage, self).__init__()
        self.config = config
        self.client = cosmos_client.CosmosClient(
            self.config.endpoint,
            {'masterKey': self.config.masterkey}
            )
        # these are set by the functions that check 
        # the presence of the db and container or creates them
        self.db = None
        self.container = None

    async def read(self, keys: List[str]) -> dict:
        """Read storeitems from storage.

        :param keys:
        :return dict:
        """
        try:
            # check if the database and container exists and if not create
            if not self.__container_exists:
                self.__create_db_and_container()
            if len(keys) > 0:
                # create the parameters object
                parameters = [
                    {'name': f'@id{i}', 'value': f'{self.__sanitize_key(key)}'}
                    for i, key in enumerate(keys)
                    ]
                # get the names of the params
                parameter_sequence = ','.join(param.get('name')
                                              for param in parameters)
                # create the query
                query = {
                    "query":
                    f"SELECT c.id, c.realId, c.document, c._etag \
FROM c WHERE c.id in ({parameter_sequence})",
                    "parameters": parameters
                    }
                options = {'enableCrossPartitionQuery': True}
                # run the query and store the results as a list
                results = list(
                    self.client.QueryItems(
                        self.__container_link, query, options)
                    )
                # return a dict with a key and a StoreItem
                return {
                    r.get('realId'): self.__create_si(r) for r in results
                    }
            else:
                raise Exception('cosmosdb_storage.read(): \
provide at least one key')
        except TypeError as e:
            raise e

    async def write(self, changes: Dict[str, StoreItem]):
        """Save storeitems to storage.

        :param changes:
        :return:
        """
        try:
            # check if the database and container exists and if not create
            if not self.__container_exists:
                self.__create_db_and_container()
                # iterate over the changes
            for (key, change) in changes.items():
                # store the e_tag
                e_tag = change.e_tag
                # create the new document
                doc = {'id': self.__sanitize_key(key),
                       'realId': key,
                       'document': self.__create_dict(change)
                       }
                # the e_tag will be * for new docs so do an insert
                if (e_tag == '*' or not e_tag):
                    self.client.UpsertItem(
                        database_or_Container_link=self.__container_link,
                        document=doc,
                        options={'disableAutomaticIdGeneration': True}
                        )
                # if we have an etag, do opt. concurrency replace
                elif(len(e_tag) > 0):
                    access_condition = {'type': 'IfMatch', 'condition': e_tag}
                    self.client.ReplaceItem(
                        document_link=self.__item_link(
                            self.__sanitize_key(key)),
                        new_document=doc,
                        options={'accessCondition': access_condition}
                        )
                # error when there is no e_tag
                else:
                    raise Exception('cosmosdb_storage.write(): etag missing')
        except Exception as e:
            raise e

    async def delete(self, keys: List[str]):
        """Remove storeitems from storage.

        :param keys:
        :return:
        """
        try:
            # check if the database and container exists and if not create
            if not self.__container_exists:
                self.__create_db_and_container()
            # call the function for each key
            for k in keys:
                self.client.DeleteItem(
                    document_link=self.__item_link(self.__sanitize_key(k)))
                # print(res)
        except cosmos_errors.HTTPFailure as h:
            # print(h.status_code)
            if h.status_code != 404:
                raise h
        except TypeError as e:
            raise e

    def __create_si(self, result) -> StoreItem:
        """Create a StoreItem from a result out of CosmosDB.

        :param result:
        :return StoreItem:
        """
        # get the document item from the result and turn into a dict
        doc = result.get('document')
        # readd the e_tag from Cosmos
        doc['e_tag'] = result.get('_etag')
        # create and return the StoreItem
        return StoreItem(**doc)

    def __create_dict(self, si: StoreItem) -> Dict:
        """Return the dict of a StoreItem.

        This eliminates non_magic attributes and the e_tag.

        :param si:
        :return dict:
        """
        # read the content
        non_magic_attr = ([attr for attr in dir(si)
                          if not attr.startswith('_') or attr.__eq__('e_tag')])
        # loop through attributes and write and return a dict
        return ({attr: getattr(si, attr)
                for attr in non_magic_attr})

    def __sanitize_key(self, key) -> str:
        """Return the sanitized key.

        Replace characters that are not allowed in keys in Cosmos.

        :param key:
        :return str:
        """
        # forbidden characters
        bad_chars = ['\\', '?', '/', '#', '\t', '\n', '\r']
        # replace those with with '*' and the
        # Unicode code point of the character and return the new string
        return ''.join(
            map(
                lambda x: '*'+str(ord(x)) if x in bad_chars else x, key
                )
            )

    def __item_link(self, id) -> str:
        """Return the item link of a item in the container.

        :param id:
        :return str:
        """
        return self.__container_link + '/docs/' + id

    @property
    def __container_link(self) -> str:
        """Return the container link in the database.

        :param:
        :return str:
        """
        return self.__database_link + '/colls/' + self.container

    @property
    def __database_link(self) -> str:
        """Return the database link.

        :return str:
        """
        return 'dbs/' + self.db

    @property
    def __container_exists(self) -> bool:
        """Return whether the database and container have been created.

        :return bool:
        """
        return self.db and self.container

    def __create_db_and_container(self):
        """Call the get or create methods."""
        db_id = self.config.database
        container_name = self.config.container
        self.db = self.__get_or_create_database(self.client, db_id)
        self.container = self.__get_or_create_container(
            self.client, container_name
            )

    def __get_or_create_database(self, doc_client, id) -> str:
        """Return the database link.

        Check if the database exists or create the db.

        :param doc_client:
        :param id:
        :return str:
        """
        # query CosmosDB for a database with that name/id
        dbs = list(doc_client.QueryDatabases({
            "query": "SELECT * FROM r WHERE r.id=@id",
            "parameters": [
                {"name": "@id", "value": id}
            ]
        }))
        # if there are results, return the first (db names are unique)
        if len(dbs) > 0:
            return dbs[0]['id']
        else:
            # create the database if it didn't exist
            res = doc_client.CreateDatabase({'id': id})
            return res['id']

    def __get_or_create_container(self, doc_client, container) -> str:
        """Return the container link.

        Check if the container exists or create the container.

        :param doc_client:
        :param container:
        :return str:
        """
        # query CosmosDB for a container in the database with that name
        containers = list(doc_client.QueryContainers(
            self.__database_link,
            {
                "query": "SELECT * FROM r WHERE r.id=@id",
                "parameters": [
                    {"name": "@id", "value": container}
                ]
            }
        ))
        # if there are results, return the first (container names are unique)
        if len(containers) > 0:
            return containers[0]['id']
        else:
            # Create a container if it didn't exist
            res = doc_client.CreateContainer(
                self.__database_link, {'id': container})
            return res['id']
