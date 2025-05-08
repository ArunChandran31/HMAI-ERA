from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb://localhost:27017/")
db = client["employee_monitoring"]
activity_collection = db["employee_activity"]
work_hours_collection = db["emp_work_hours"]
employee_ids = activity_collection.distinct("employee_id")
fmt = "%Y-%m-%dT%H:%M:%S.%f%z"

for employee_id in employee_ids:
    records = activity_collection.find(
        {"employee_id": employee_id, "working": True},
        {"timestamp": 1}
    )
    
    timestamps = sorted([record["timestamp"] for record in records])
    datetime_stamps = timestamps 
    
    if not datetime_stamps:
        continue

    total_seconds = 0
    for i in range(1, len(datetime_stamps)):
        diff = (datetime_stamps[i] - datetime_stamps[i - 1]).total_seconds()
        if diff < 1800:  
            total_seconds += diff

    total_hours = total_seconds / 3600
    work_hours_collection.update_one(
        {"employee_id": employee_id, "date": str(datetime_stamps[0].date())},
        {"$set": {"total_hours": total_hours}},
        upsert=True
    )

    print(f"Updated work hours for {employee_id}: {total_hours:.2f} hours")

print("Work hours calculation complete!")
