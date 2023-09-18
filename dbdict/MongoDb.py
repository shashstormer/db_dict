import threading
from pymongo import MongoClient
import time
import os


class MongoDB:
    def __init__(self, db_name, collection, key_field, conn_string=None):
        if not conn_string:
            conn_string = os.getenv("MONGO_CONNECTION_STRING")
        self.client = MongoClient(conn_string)
        self._collection = collection
        self.key_field = key_field
        self.collection = self.client[db_name][self._collection]
        self.lock = threading.Lock()

    def __getitem__(self, key, moniter=True):
        document = self.collection.find_one({self.key_field: key})
        if document:
            threading.Thread(target=self.monitor, args=[document],).start()
            return document
        else:
            raise KeyError(f"Key '{key}' not found")

    def __contains__(self, key):
        try:
            document = self.__getitem__(key, False)
        except KeyError:
            return False
        return document is not None

    def fetch_all(self):
        return self.collection.find()

    def __iter__(self):
        cursor = self.fetch_all()
        for document in cursor:
            yield document

    def __setitem__(self, key, value):
        with self.lock:
            result = self.collection.update_one(
                {self.key_field: key},
                {"$set": value},
                upsert=True
            )

            if not result.matched_count and not result.upserted_id:
                raise ValueError(f"Failed to update/insert data for key '{key}'")

    def __delitem__(self, key):
        with self.lock:
            result = self.collection.delete_one({self.key_field: key})
            if result.deleted_count == 0:
                raise KeyError(f"Key '{key}' not found")

    def get(self, key, default=False):
        try:
            return self[key]
        except KeyError:
            return default

    def monitor(self, data):
        old = data.copy()
        while True:
            time.sleep(0.2)
            if old != data:
                with self.lock:
                    old = data.copy()
                    self.collection.update_one({self.key_field: data[self.key_field]}, {"$set": data},)

    def update(self, data):
        with self.lock:
            self.collection.update_one({self.key_field: data[self.key_field]}, {"$set": data})
