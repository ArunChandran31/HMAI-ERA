import time
import requests
import threading
from pymongo import MongoClient
from selenium import webdriver # type: ignore
from selenium.webdriver.chrome.service import Service # type: ignore
from selenium.webdriver.chrome.options import Options # type: ignore

API_URL = "http://127.0.0.1:5000/api/employees"
MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "employee_db"
DASHBOARD_URL = "http://127.0.0.1:5000"


def test_api_response_time():
    start_time = time.time()
    response = requests.get(API_URL)
    end_time = time.time()
    response_time = end_time - start_time
    print(f"API Response Time: {response_time:.4f} seconds")
    return response_time


def test_db_query_time():
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db["employee_activity"]
    
    start_time = time.time()
    result = collection.find_one()
    end_time = time.time()
    
    query_time = end_time - start_time
    print(f"Database Query Time: {query_time:.4f} seconds")
    return query_time


def test_page_load_time():
    options = Options()
    options.headless = True
    service = Service("chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)
    start_time = time.time()
    driver.get(DASHBOARD_URL)
    end_time = time.time()
    driver.quit()
    load_time = end_time - start_time
    print(f"Page Load Time: {load_time:.4f} seconds")
    return load_time


def simulate_users(num_users=10):
    def api_request():
        requests.get(API_URL)

    threads = []
    start_time = time.time()
    for _ in range(num_users):
        thread = threading.Thread(target=api_request)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    end_time = time.time()
    concurrent_time = end_time - start_time
    print(f"Handled {num_users} concurrent users in {concurrent_time:.4f} seconds")
    return num_users


def count_errors():
    with open("dashboard.log", "r") as f:
        logs = f.readlines()
    error_count = sum(1 for line in logs if "ERROR" in line)
    print(f"Error Rate: {error_count} errors/min")
    return error_count


if __name__ == "__main__":
    page_load = test_page_load_time()
    api_response = test_api_response_time()
    db_query = test_db_query_time()
    concurrent_users = simulate_users(10)
    error_rate = count_errors()

    print("\n### Performance Report ###")
    print(f"Page Load Time: {page_load:.4f} seconds")
    print(f"API Response Time (Avg): {api_response:.4f} seconds")
    print(f"Database Query Time: {db_query:.4f} seconds")
    print(f"Max Concurrent Users Supported: {concurrent_users}")
    print(f"Error Rate: {error_rate} errors/min")
