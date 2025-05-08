import time
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from pymongo import MongoClient
from config import MONGO_URI, DB_NAME


client = MongoClient(MONGO_URI)
db = client[DB_NAME]
activity_collection = db["employee_activity"]


def fetch_activity_data():
    """Retrieve stored employee activity data."""
    return list(activity_collection.find())


def evaluate_face_recognition(predicted_labels, true_labels):
    """Evaluate face recognition performance."""
    accuracy = accuracy_score(true_labels, predicted_labels)
    precision = precision_score(true_labels, predicted_labels, average="weighted", zero_division=1)
    recall = recall_score(true_labels, predicted_labels, average="weighted", zero_division=1)
    f1 = f1_score(true_labels, predicted_labels, average="weighted", zero_division=1)

    print("\nFace Recognition Performance:")
    print(f"Accuracy: {accuracy:.2f}")
    print(f"Precision: {precision:.2f}")
    print(f"Recall: {recall:.2f}")
    print(f"F1-score: {f1:.2f}")


def evaluate_system_latency():
    """Measure system response time for database queries."""
    start_time = time.time()
    fetch_activity_data()
    latency = time.time() - start_time

    print(f"\nDatabase Query Latency: {latency:.4f} seconds")


def analyze_activity_data():
    """Check employee working status accuracy."""
    data = fetch_activity_data()
    
    predicted_working = [entry["working"] for entry in data]
    true_working = [True] * len(predicted_working)

    evaluate_face_recognition(predicted_working, true_working)
    evaluate_system_latency()

if __name__ == "__main__":
    analyze_activity_data()
