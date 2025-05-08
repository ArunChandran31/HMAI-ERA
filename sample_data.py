from pymongo import MongoClient
from datetime import datetime, timedelta, timezone
import random

# Connect to MongoDB
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "employee_monitoring"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
activity_collection = db["employee_activity"]

# Sample Employees
employees = [
    {"employee_id": "E101", "employee_name": "Laurel"},
    {"employee_id": "E102", "employee_name": "John"},
    {"employee_id": "E103", "employee_name": "Alice"},
    {"employee_id": "E104", "employee_name": "Arun"},
    {"employee_id": "E105", "employee_name": "David"},
]

# Generate random data for the last 7 days
start_date = datetime.now(timezone.utc) - timedelta(days=7)
data = []

for _ in range(200):  # Insert 200 sample records
    employee = random.choice(employees)
    timestamp = start_date + timedelta(minutes=random.randint(0, 7 * 24 * 60))  # Random timestamp in last 7 days
    working = random.choice([True, False])
    warning = random.choices([False, True], weights=[80, 20])[0]  # 20% chance of warning
    status = "Working" if working else "Not Working"

    data.append({
        "employee_id": employee["employee_id"],
        "employee_name": employee["employee_name"],
        "timestamp": timestamp,
        "working": working,
        "status": status,
        "warning": warning
    })

# Insert into MongoDB
activity_collection.insert_many(data)

print("Inserted 200 sample employee activity records successfully!")
