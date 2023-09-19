import threading
import mysql.connector
import time
import os
import json


class MySqlDB:
    def __init__(self, db_name, table_name, key_field, conn_params=None):
        if not conn_params:
            conn_params = {
                "host": os.getenv("MYSQL_HOST", "localhost"),
                "port": int(os.getenv("MYSQL_PORT", 3306)),
                "user": os.getenv("MYSQL_USER", "root"),
                "password": os.getenv("MYSQL_PASSWORD", ""),
            }
        self.conn = mysql.connector.connect(**conn_params)
        self.cursor = self.conn.cursor(dictionary=True)
        self.table_name = table_name
        self.key_field = key_field
        self.lock = threading.Lock()
        self.create_database_if_not_exists(db_name)
        self.conn.database = db_name
        self._create_table()

    def create_database_if_not_exists(self, db_name):
        create_db_query = f"CREATE DATABASE IF NOT EXISTS {db_name}"
        with self.lock:
            self.cursor.execute(create_db_query)
            self.conn.commit()

    def _create_table(self):
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {self.table_name} (
            {self.key_field} VARCHAR(255) PRIMARY KEY,
            data JSON
        )
        """

        self.cursor.execute(create_table_query)
        self.conn.commit()

    def __getitem__(self, key, monitor=True):
        query = f"SELECT * FROM {self.table_name} WHERE {self.key_field} = %s"
        self.cursor.execute(query, (key,))
        document = self.cursor.fetchone()
        if document:
            got = json.loads(document["data"])
            if monitor:
                threading.Thread(target=self.monitor, args=[got]).start()
            return got
        else:
            raise KeyError(f"Key '{key}' not found")

    def __contains__(self, key):
        try:
            document = self.__getitem__(key, monitor=False)
        except KeyError:
            return False
        return document is not None

    def fetch_all(self):
        query = f"SELECT * FROM {self.table_name}"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def __iter__(self):
        for document in self.fetch_all():
            yield document

    def __setitem__(self, key, value):
        with self.lock:
            query = f"""
            INSERT INTO {self.table_name} ({self.key_field}, data)
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE data = %s
            """
            data = (key, json.dumps(value), json.dumps(value))
            self.cursor.execute(query, data)
            self.conn.commit()

    def __delitem__(self, key):
        with self.lock:
            query = f"DELETE FROM {self.table_name} WHERE {self.key_field} = %s"
            self.cursor = self.conn.cursor(dictionary=True)
            self.cursor.execute(query, (key,))
            if self.cursor.rowcount == 0:
                raise KeyError(f"Key '{key}' not found")
            self.conn.commit()

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def monitor(self, data):
        old_data = data.copy()
        current_data = data
        while True:
            time.sleep(0.2)
            if old_data != current_data:
                with self.lock:
                    old_data = current_data.copy()
                    self[current_data[self.key_field]] = current_data

    def update(self, key, value):
        self[key] = value


if __name__ == "__main__":
    db = MySqlDB("test_db", "test_table", "keyfield")
    db["test"] = {"keyfield": "test", "my data": {"random data": True}}
    print(db["test"])
    db.update("test", {"test": "test2"})
    print("test" in db)
    print(db["test"])
    del db["test"]
    print("test" in db)
    print(db.get("test", "not found"))
    print(db["test"])
