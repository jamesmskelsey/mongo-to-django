from itertools import count
import os
from dotenv import load_dotenv
import pymongo

load_dotenv()

CONNECTION_STRING = os.getenv('CONNECTION_STRING')
DATABASE = os.getenv('DATABASE_NAME')
COLLECTION = os.getenv('COLLECTION_TO_ANALYZE')

print(f"Connecting to: {CONNECTION_STRING}")
client = pymongo.MongoClient(CONNECTION_STRING, serverSelectionTimeoutMS=5000)
connected = False

try:
  server_info = client.server_info()
  if server_info['ok']:
    connected = True
  
except Exception:
  print("Unable to connect to the server.")

if connected:
  print("Connected to server. Now attempting to access documents.")
  number_of_documents = 0
  filter = {}
  skip=0
  limit=1000
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

  aggregation_count_of_documents_in_collection = client['g2link']['companies'].aggregate([
    {
        '$count': 'count'
    }
  ])

  for count in aggregation_count_of_documents_in_collection:
    # Cursors are weird.
    number_of_documents = count['count']
    print(f"Found {number_of_documents} documents in collection: '{COLLECTION}'.")

  while skip < number_of_documents:
    # We'll eventually loop across the number_of_documents, paginating out 1,000 at a time and recording the results.
    results = client[DATABASE][COLLECTION].find(
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

  for k, v in counts.items():
    print(k, v)