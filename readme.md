# DB Dictionary

## Description :
This is a module which has been designed to make it easier to work with databases 
in python using a dictionary like interface.

## Installation :
`pip install DBDictionary`

# Supported Databases:

MongoDB - MongoDB_Dict

MySqlDB - MySqlDB_Dict

## Usage :

### It is the same for all databases

### Sample for MongoDB
```python
from DBDictionary import MongoDB_Dict

my_db_dict = MongoDB_Dict("my_db_name", "my_collection_name", "my_key_field", "my_connection_string")
# The connection string is optional and will default to 
# "mongodb://localhost:27017/"  if not provided here and not in the ENV var also
my_db_dict["my_key"] = {"my_key_field": "my_key",
                        "other data": "my_value"}  # This will insert a new document into the collection
your_value = my_db_dict["my_key"]  # This will return "my_value", the value in the database
print(your_value)  # This will print {"my_key_field": "my_key", "other data": "my_value"}
del my_db_dict["my_key"]  # This will delete the document from the collection
# now trying to retrive the value will raise a KeyError ,
# but you can use the "get" method like you do in a dictionary as usual
your_value = my_db_dict.get("my_key", "default_value")  # This will return "default_value"
print(your_value)  # This will print "default_value"
your_value = my_db_dict["my_key"]  # This will raise a KeyError

# editing and updating a document :
your_value["other data"] = "my_new_value"  # This will edit the value in the memory
my_db_dict.update(your_value)  # This will update the document in the database

# When you edit a dictionary like this :
my_db_dict["my_key"][
    "other data"] = "my_new_value"  # This will have no effect on the database and any changes will be lost
```

### It is the same for other databases also

