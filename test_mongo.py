from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")

db = client["fashion_db"]

result = db.fashion_items.insert_one({
    "name": "Test Shoes",
    "category": "shoes",
    "style": "casual"
})

print("Connected!")
print(result.inserted_id)