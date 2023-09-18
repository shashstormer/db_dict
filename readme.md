# DB Dict

## Description :
This is a module which has beed designed to make it easier to work with databases 
in python using a dictionary like interface.

## Installation :
`pip install ...`

## Usage MongoDB :
```python
from dbdict import MongoDB_Dict

my_db_dict = MongoDB_Dict("my_db_name", "my_collection_name", "my_key_field", "my_connection_string")
# The connection string is optional and will default to 
# "mongodb://localhost:27017/"  if not provided here and not in the ENV var also
my_db_dict["my_key"] = {"my_key_field": "my_key", "other data": "my_value"}  # This will insert a new document into the collection
your_value = my_db_dict["my_key"] # This will return "my_value", the value in the database
print(your_value) # This will print {"my_key_field": "my_key", "other data": "my_value"}
del my_db_dict["my_key"] # This will delete the document from the collection
# now trying to retrive the value will raise a KeyError ,
# but you can use the "get" method like you do in a dictionary as usual
your_value = my_db_dict.get("my_key", "default_value") # This will return "default_value"
print(your_value) # This will print "default_value"
your_value = my_db_dict["my_key"] # This will raise a KeyError
```

