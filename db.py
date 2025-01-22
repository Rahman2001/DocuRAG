from datetime import datetime

from bson import ObjectId
from pymongo import MongoClient


class MongoDB:
    def __init__(self, database_name: str, collection_name: str):
        self.__client = MongoClient('localhost', 27017)
        self.__db = self.__client[database_name]
        self.__record_table = self.__db[collection_name]

    def create_record(self, record: dict):
        record['_id'] = record['idempotencyKey']
        record.pop('idempotencyKey')
        record['datetime'] = datetime.now()
        result = self.__record_table.insert_one(record)
        print(f'result.inserted_id: {result.inserted_id}')
        return record['_id']

    def delete_record(self, document_id: str):
        document_id = document_id.replace('-success', '')
        result = self.__record_table.delete_one({'_id': document_id})
        return result.deleted_count

    def get_by_id(self, document_id: str):
        document = self.__record_table.find_one({'_id': document_id})
        return document

