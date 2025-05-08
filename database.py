from pymongo import MongoClient
import datetime
import config


def get_db():
    client = MongoClient(config.MONGO_URI)
    db = client[config.DB_NAME]
    return db


def init_db():
    db = get_db()
    if "employees" not in db.list_collection_names():
        db.create_collection("employees")
    if "activity_logs" not in db.list_collection_names():
        db.create_collection("activity_logs")
    print("Database initialized successfully.")


def log_activity(employee_id, face_detected, screen_active, mouse_active, keyboard_active, status):
    db = get_db()
    log_entry = {
        "employee_id": employee_id,
        "timestamp": datetime.datetime.utcnow(),
        "face_detected": face_detected,
        "screen_active": screen_active,
        "mouse_active": mouse_active,
        "keyboard_active": keyboard_active,
        "status": status
    }
    db.activity_logs.insert_one(log_entry)

if __name__ == "__main__":
    init_db()
