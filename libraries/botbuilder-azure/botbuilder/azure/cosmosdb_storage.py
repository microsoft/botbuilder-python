# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import Dict, List
from copy import deepcopy
import json
from botbuilder.core.storage import Storage, StoreItem
import azure.cosmos.cosmos_client as cosmos_client


class CosmosDbStorage(Storage):
    def __init__(self, config, dictionary=None):
        super(CosmosDbStorage, self).__init__()
        self.config = config
        self.client = cosmos_client.CosmosClient(self.config['ENDPOINT'], {'masterKey': self.config['MASTERKEY']})
        self.db = None
        self.container = None

    async def delete(self, keys: List[str]):
        try:
            #check if the database and container exists and if not create
            if not self.container_exists:
                self.create_db_and_container()
            #call the function for each key
            map(self.__delete_key, keys)
        except TypeError as e:
            raise e

    async def __delete_key(self, key_to_delete):
        print(f'try to delete: {self.document_link(self.sanitize_key(key_to_delete))}')
        await self.client.DeleteItem(self.document_link(self.sanitize_key(key_to_delete)))

    async def read(self, keys: List[str]):
        try:
            #check if the database and container exists and if not create
            if not self.container_exists:
                self.create_db_and_container()
            #create a comma seperated list of keys
            parameters = ",".join(map(self.sanitize_key, keys))
            #create the query 
            query = {
                'query': f'SELECT c.id, c.realId, c.document, c._etag FROM c WHERE c.id in (@ids)',
                "parameters": [
                        { "name":"@ids", "value": parameters }
                    ]
                }
            options = { 'enableCrossPartitionQuery': True }
            #run the query and store the results as a list
            results = list(self.client.QueryItems(self.container_link, query, options))
            #return a dict with a key and a StoreItem
            return {r.get('realId'): self.__create_si_from_result(r) for r in results}
        except TypeError as e:
            raise e

    def __create_si_from_result(self, result):
        #get the document item from the result and turn into a dict
        doc = eval(result.get('document'))
        #readd the e_tag from Cosmos
        doc['e_tag'] = result.get('_etag')
        #create and return the StoreItem 
        return StoreItem(**doc)

    async def write(self, changes: Dict[str, StoreItem]):
        try:
            #check if the database and container exists and if not create
            if not self.container_exists:
                self.create_db_and_container()
                # iterate over the changes
            for (key, change) in changes.items():
                #store the e_tag
                e_tag = change.e_tag
                #create a copy of the change and delete the e_tag since CosmosDB handles that
                change_copy = deepcopy(change)
                del change_copy.e_tag
                #create the new document
                doc = {'id': self.sanitize_key(key), 'realId': key, 'document': str(change_copy)}
                #if it's a new document, then the e_tag will be * so do an insert
                if (e_tag == '*'):
                    self.client.UpsertItem(database_or_Container_link=self.container_link, 
                                document=doc, 
                                options={'disableAutomaticIdGeneration': True}
                                )
                #otherwise let cosmosdb decide if its the same and replace if necessary
                elif(len(e_tag) > 0):
                    access_condition = { 'type': 'IfMatch', 'condition': e_tag }
                    self.client.ReplaceItem(document_link=self.document_link(self.sanitize_key(key)), 
                                new_document=doc, 
                                options={'accessCondition': access_condition}
                                )
                #error when there is no e_tag
                else:
                    raise KeyError('cosmosdb_storage.wite(): etag missing')
        except Exception as e:
            raise e

    def document_link(self, id):
        return self.container_link + '/docs/' + id

    @property
    def container_link(self):
        return self.database_link + '/colls/' +  self.container

    @property
    def database_link(self):
        return 'dbs/' + self.db

    @property
    def container_exists(self):
        return self.db and self.container

    def create_db_and_container(self):
        db_id = self.config['DOCUMENTDB_DATABASE']
        container_name = self.config['DOCUMENTDB_CONTAINER']
        self.db = self.get_or_create_database(self.client, db_id)
        self.container = self.get_or_create_container(self.client, container_name)

    def get_or_create_database(self, doc_client, id):
        dbs = list(doc_client.QueryDatabases({
            "query": "SELECT * FROM r WHERE r.id=@id",
            "parameters": [
                { "name":"@id", "value": id }
            ]
        }))
        if len(dbs) > 0:
            return dbs[0]['id']
        else:
            res = doc_client.CreateDatabase({ 'id': id })
            return res['id']

    def get_or_create_container(self, doc_client, container):        
        containers = list(doc_client.QueryContainers(
            self.database_link,
            {
                "query": "SELECT * FROM r WHERE r.id=@id",
                "parameters": [
                    { "name":"@id", "value": container }
                ]
            }
        ))
        if len(containers) > 0:
            return containers[0]['id']
        else:
            # Create a container
            res = doc_client.CreateContainer(self.database_link, { 'id': container })
            return res['id']

    def sanitize_key(self, key):
        bad_chars = ['\\', '?', '/', '#', '\t', '\n', '\r']
        return ''.join(map(lambda x: '*'+str(ord(x)) if x in bad_chars else x, key))
