import os
from dotenv import load_dotenv
import pymongo
import model_reader
from model_output import model_to_xlsx

load_dotenv()

CONNECTION_STRING = os.getenv('CONNECTION_STRING')
DATABASE = os.getenv('DATABASE_NAME')
COLLECTION = os.getenv('COLLECTION_TO_ANALYZE')

if DATABASE == '':
  raise ValueError("Database name cannot be a blank string. Edit the .env file.")
if COLLECTION == '':
  raise ValueError("The collection name must be provided in .env")

print(f"Connecting to: {CONNECTION_STRING}")
client = pymongo.MongoClient(CONNECTION_STRING, serverSelectionTimeoutMS=5000)
connected = False

try:
  server_info = client.server_info()
  if server_info['ok']:
    connected = True
  
except Exception:
  print("Unable to connect to the server. Cancelling.")

if connected:
  print("Connected to server. Now attempting to access documents.\n")
  for collection in COLLECTION.split(','):
    print(collection)
    results = model_reader.read(client, DATABASE, collection)
    model_to_xlsx(collection, results)