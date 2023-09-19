"""
Database Wrapper Interface

This module provides a generic interface for creating database wrappers for different databases.

Usage:
    This module defines a generic interface for database wrappers. Contributors can use this
    interface as a template to create wrappers for specific databases.

"""

class DatabaseWrapper:
    def __init__(self, db_name, collection, key_field, conn_string=None):
        """
        Initialize the database wrapper.

        Args:
            db_name (str): The name of the database.
            collection (str): The name of the collection/table within the database.
            key_field (str): The name of the field used as the key for records.
            conn_string (str, optional): Database connection string. Defaults to None. Uses ENV variable if not provided.

        """
        pass

    def __getitem__(self, key, monitor=True):
        """
        Get a record by its key.

        Args:
            key (str): The key to look up the record.
            monitor (bool, optional): Whether to start monitoring changes. Defaults to True.

        Returns:
            dict: The record matching the key.

        Raises:
            KeyError: If the key is not found in the collection.

        """
        pass

    def __contains__(self, key):
        """
        Check if a key exists in the collection.

        Args:
            key (str): The key to check.

        Returns:
            bool: True if the key exists, False otherwise.

        """
        pass

    def fetch_all(self):
        """
        Fetch all records from the collection.

        Returns:
            iterable: An iterable containing all records in the collection.

        """
        pass

    def __setitem__(self, key, value):
        """
        Insert or update a record in the collection.

        Args:
            key (str): The key to identify the record.
            value (dict): The record data to insert or update.

        Raises:
            ValueError: If the insertion or update fails.

        """
        pass

    def __delitem__(self, key):
        """
        Delete a record from the collection by its key.

        Args:
            key (str): The key of the record to delete.

        Raises:
            KeyError: If the key is not found in the collection.

        """
        pass

    def get(self, key, default=None):
        """
        Get a record by its key, or return a default value if the key does not exist.

        Args:
            key (str): The key to look up the record.
            default (any, optional): The value to return if the key is not found. Defaults to None.

        Returns:
            dict or any: The record matching the key or the default value if not found.

        """
        pass

    def monitor(self, data):
        """
        Monitor changes to a record and update it in the collection.

        Args:
            data (dict): The record to monitor for changes.

        """
        pass

    def update(self, data):
        """
        Update a record in the collection.

        Args:
            data (dict): The updated record data.

        """
        pass

# Optional: Contributors can create specific database wrappers by inheriting from DatabaseWrapper and implementing the methods accordingly.
