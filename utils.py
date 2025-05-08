from pymongo import MongoClient
from datetime import datetime, timedelta, timezone

MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "employee_monitoring"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
activity_collection = db["employee_activity"]

# Check for last 7 days data
start_date = datetime.now(timezone.utc) - timedelta(days=7)
query = {"timestamp": {"$gte": start_date}}

count = activity_collection.count_documents(query)
print(f"Records found in last 7 days: {count}")
