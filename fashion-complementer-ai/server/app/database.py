import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME   = os.getenv("DB_NAME", "fashion_db")

client = MongoClient(MONGO_URI)
db     = client[DB_NAME]

history_collection = db["predictions"]
items_collection   = db["fashion_items"]

# Ensure indexes exist
items_collection.create_index("image_path", unique=True)
items_collection.create_index("category")
items_collection.create_index("style")


# FastAPI dependency injection
def get_items_collection():
    return items_collection
