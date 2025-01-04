from pymongo import MongoClient
from decouple import config
from pymongo.collection import Collection

print("Initializing database...")
MONGO_URI = config("MONGO_URI")
print(f"Connecting to MongoDB at {MONGO_URI}")
client = MongoClient(MONGO_URI)
db = client["sensor_db"]
sensor_collection: Collection = db["sensors"]
