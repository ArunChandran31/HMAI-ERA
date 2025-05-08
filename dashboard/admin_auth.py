from pymongo import MongoClient
from werkzeug.security import generate_password_hash

client = MongoClient("mongodb://localhost:27017/")
db = client["employee_monitoring"]
admin_collection = db["users"]

admin_data = {
    "username": "arun",
    "password": "password"
}

admin_collection.insert_one(admin_data)
print("Admin created successfully!")
