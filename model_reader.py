from typing import Dict
from pymongo import MongoClient

def read(client: MongoClient, database: str, collection: str, limit:int=1000, filter:dict={}) -> Dict: 
  """
  Given a pymongo client, a database name, and a collection name, finds the field names
  and the types of data in each field and returns them as a dictionary.

  Optional:
  limit: Number of docs to analyze at a time.
  filter: A DSL query to limit the docs to a subset. 
  """
  number_of_documents = 0
  skip=124347
  counts = {
    # Example of end result this dict should be.
    # 'field_name': {
    #   'type_1': 10,
    #   'type_2': 5
    # },
    # 'next_field_name': {
    #   'type_1': 5,
    #   'type_2': 10,
    # }
  }

  aggregation_count_of_documents_in_collection = client[database][collection].aggregate([
    {
        '$count': 'count'
    }
  ])

  for count in aggregation_count_of_documents_in_collection:
    # Cursors are weird.
    number_of_documents = count['count']
    print(f"Found {number_of_documents} documents in collection: '{database}'.")

  while skip < number_of_documents:
    # We'll eventually loop across the number_of_documents, paginating out 1,000 at a time and recording the results.
    results = client[database][collection].find(
      filter=filter,
      skip=skip,
      limit=limit
    )

    for result in results:
      for field_name, field_type in result.items():
        # I don't care what the value is - only what the type is, so convert is straight away.
        field_type = type(field_type)
        # option 1 - field name does not exist.
        ## check for the field name - it doesn't exist, so we create one.
        if field_name not in counts:
          counts[field_name] = {
            field_type: 1
          }
        # option 2 - field name does exist, the type does not exist.
        elif field_name in counts and field_type not in counts[field_name]:
          counts[field_name][field_type] = 1
        # option 3 - field name does exist, type does exist.
        elif field_name in counts and field_type in counts[field_name]:
          counts[field_name][field_type] += 1
    skip += 1000
    
  return counts
  # Uncomment to print to console.
  # for k, v in counts.items():
  #   print(k, v)