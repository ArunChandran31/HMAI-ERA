# import cv2
# import os
# import time
# import numpy as np
# import face_recognition
# from pymongo import MongoClient
# from pynput import mouse, keyboard
# from screeninfo import get_monitors
# from mtcnn import MTCNN
# from config import MONGO_URI, DB_NAME, INACTIVE_THRESHOLD, WARNING_THRESHOLD
# from datetime import datetime, timezone


# # Connect to MongoDB
# client = MongoClient(MONGO_URI)
# db = client[DB_NAME]
# activity_collection = db["employee_activity"]

# # Employee ID mapping (Hardcoded)
# EMPLOYEE_IDS = {
#     "arun": "E104",
#     "laurel": "E101",
#     "john": "E102",  # Add more employees if needed
#     "alice": "E103"
# }

# # Initialize MTCNN detector
# detector = MTCNN()

# KNOWN_FACES_DIR = "data"
# UNKNOWN_FACES_DIR = "unknown_faces"
# os.makedirs(UNKNOWN_FACES_DIR, exist_ok=True)

# known_faces = []
# known_names = []

# # Load reference images and encode faces
# for filename in os.listdir(KNOWN_FACES_DIR):
#     image_path = os.path.join(KNOWN_FACES_DIR, filename)
#     image = cv2.imread(image_path)
#     if image is None:
#         print(f"Error loading {filename}. Skipping...")
#         continue
#     rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#     detections = detector.detect_faces(rgb_image)
#     if not detections:
#         print(f"Warning: No face found in {filename}. Skipping...")
#         continue
#     x, y, width, height = detections[0]["box"]
#     top, right, bottom, left = y, x + width, y + height, x
#     face_encoding = face_recognition.face_encodings(rgb_image, [(top, right, bottom, left)])
#     if face_encoding:
#         known_faces.append(face_encoding[0])
#         known_names.append(os.path.splitext(filename)[0].lower())  # Convert to lowercase

# print(f"Loaded {len(known_faces)} known faces.")

# # Track user activity
# last_mouse_time = time.time()
# last_keyboard_time = time.time()
# mouse_positions = []
# unknown_face_timers = {}
# unknown_face_encodings = []

# def on_mouse_move(x, y):
#     global last_mouse_time, mouse_positions
#     current_time = time.time()
#     if current_time - last_mouse_time > 1:
#         mouse_positions.append((x, y))
#         if len(mouse_positions) > 10:
#             mouse_positions.pop(0)
#         last_mouse_time = current_time

# def on_key_press(key):
#     global last_keyboard_time
#     last_keyboard_time = time.time()

# mouse_listener = mouse.Listener(on_move=on_mouse_move)
# keyboard_listener = keyboard.Listener(on_press=on_key_press)
# mouse_listener.start()
# keyboard_listener.start()

# video_capture = cv2.VideoCapture(0)

# while True:
#     ret, frame = video_capture.read()
#     if not ret:
#         print("Failed to grab frame.")
#         continue

#     rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#     detections = detector.detect_faces(rgb_frame)
#     face_locations = []
#     face_encodings = []

#     for detection in detections:
#         x, y, width, height = detection["box"]
#         top, right, bottom, left = y, x + width, y + height, x
#         face_locations.append((top, right, bottom, left))

#     if face_locations:
#         face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

#     for face_encoding, (top, right, bottom, left) in zip(face_encodings, face_locations):
#         distances = face_recognition.face_distance(known_faces, face_encoding)
#         best_match_index = np.argmin(distances) if len(distances) > 0 else None

#         if best_match_index is not None and distances[best_match_index] < 0.5:
#             employee_name = known_names[best_match_index]
#         else:
#             employee_name = "Unknown"
#             if not any(np.linalg.norm(face_encoding - enc) < 0.5 for enc in unknown_face_encodings):
#                 unknown_face_encodings.append(face_encoding)
#                 unknown_face_timers[time.time()] = frame.copy()

#         # Fetch employee ID from hardcoded list
#         employee_id = EMPLOYEE_IDS.get(employee_name, "Unknown")

#         # Draw the bounding box and text
#         cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
#         cv2.putText(frame, f"{employee_name} ({employee_id})", (left, top - 10), 
#                     cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

#     screen_active = any(m.is_primary for m in get_monitors())
#     current_time = time.time()
#     mouse_active = (current_time - last_mouse_time) < INACTIVE_THRESHOLD
#     keyboard_active = (current_time - last_keyboard_time) < INACTIVE_THRESHOLD
#     working = (employee_name != "Unknown") and screen_active and (mouse_active or keyboard_active)

#     if len(mouse_positions) > 5:
#         movements = [abs(mouse_positions[i][0] - mouse_positions[i-1][0]) +
#                      abs(mouse_positions[i][1] - mouse_positions[i-1][1]) for i in range(1, len(mouse_positions))]
#         warning = sum(movements) < WARNING_THRESHOLD
#     else:
#         warning = False

#     # Store data in required format
#     activity_data = {
#         "employee_id": employee_id,
#         "employee_name": employee_name,
#         "timestamp": datetime.now(timezone.utc),
#         "working": working,
#         "warning": warning
#     }

#     if employee_name != "Unknown" and int(time.time()) % 5 == 0:
#         activity_collection.insert_one(activity_data)

#     for timestamp, face_frame in list(unknown_face_timers.items()):
#         if time.time() - timestamp > 60:
#             image_path = os.path.join(UNKNOWN_FACES_DIR, f"unknown_{int(timestamp)}.jpg")
#             cv2.imwrite(image_path, face_frame)
#             print(f"Saved unknown face to {image_path}")
#             del unknown_face_timers[timestamp]

#     cv2.imshow("Employee Monitoring", frame)

#     if cv2.waitKey(1) & 0xFF == ord("q"):
#         break

# video_capture.release()
# cv2.destroyAllWindows()
# mouse_listener.stop()
# keyboard_listener.stop()
import cv2
import os
import time
import numpy as np
import face_recognition
from pymongo import MongoClient
from pynput import mouse, keyboard
from screeninfo import get_monitors
from mtcnn import MTCNN
from config import MONGO_URI, DB_NAME, INACTIVE_THRESHOLD, WARNING_THRESHOLD
from datetime import datetime, timezone

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
activity_collection = db["employee_activity"]

EMPLOYEE_IDS = {
    "arun": "E104",
    "laurel": "E101",
    "john": "E102",
    "alice": "E103"
}

detector = MTCNN()

KNOWN_FACES_DIR = "data"
UNKNOWN_FACES_DIR = "unknown_faces"
os.makedirs(UNKNOWN_FACES_DIR, exist_ok=True)

known_faces = []
known_names = []


for filename in os.listdir(KNOWN_FACES_DIR):
    image_path = os.path.join(KNOWN_FACES_DIR, filename)
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error loading {filename}. Skipping...")
        continue
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    detections = detector.detect_faces(rgb_image)
    if not detections:
        print(f"Warning: No face found in {filename}. Skipping...")
        continue
    x, y, width, height = detections[0]["box"]
    face_encoding = face_recognition.face_encodings(rgb_image, [(y, x + width, y + height, x)])
    if face_encoding:
        known_faces.append(face_encoding[0])
        known_names.append(os.path.splitext(filename)[0].lower())

print(f"Loaded {len(known_faces)} known faces.")


last_mouse_time = time.time()
last_keyboard_time = time.time()
mouse_positions = []
unknown_face_timers = {}
unknown_face_encodings = []

def on_mouse_move(x, y):
    global last_mouse_time, mouse_positions
    current_time = time.time()
    if current_time - last_mouse_time > 1:
        mouse_positions.append((x, y))
        if len(mouse_positions) > 10:
            mouse_positions.pop(0)
        last_mouse_time = current_time

def on_key_press(key):
    global last_keyboard_time
    last_keyboard_time = time.time() 

mouse_listener = mouse.Listener(on_move=on_mouse_move)
keyboard_listener = keyboard.Listener(on_press=on_key_press)
mouse_listener.start()
keyboard_listener.start()

video_capture = cv2.VideoCapture(0)

while True:
    ret, frame = video_capture.read()
    if not ret:
        print("Failed to grab frame.")
        continue

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    detections = detector.detect_faces(rgb_frame)
    face_locations, face_encodings = [], []

    for detection in detections:
        x, y, width, height = detection["box"]
        face_locations.append((y, x + width, y + height, x))
    
    if face_locations:
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    employee_name = "Unknown"
    employee_id = "Unknown"

    for face_encoding, (top, right, bottom, left) in zip(face_encodings, face_locations):
        distances = face_recognition.face_distance(known_faces, face_encoding)
        best_match_index = np.argmin(distances) if len(distances) > 0 else None

        if best_match_index is not None and distances[best_match_index] < 0.5:
            employee_name = known_names[best_match_index]
            employee_id = EMPLOYEE_IDS.get(employee_name, "Unknown")
        else:
            if not any(np.linalg.norm(face_encoding - enc) < 0.5 for enc in unknown_face_encodings):
                unknown_face_encodings.append(face_encoding)
                unknown_face_timers[time.time()] = frame.copy()

        
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, f"{employee_name} ({employee_id})", (left, top - 10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

    screen_active = any(m.is_primary for m in get_monitors())
    current_time = time.time()
    mouse_active = (current_time - last_mouse_time) < INACTIVE_THRESHOLD
    keyboard_active = (current_time - last_keyboard_time) < INACTIVE_THRESHOLD
    working = (employee_name != "Unknown") and screen_active and (mouse_active or keyboard_active)
    status = "Working" if working else "Not Working"

    if len(mouse_positions) > 5:
        movements = [abs(mouse_positions[i][0] - mouse_positions[i-1][0]) +
                     abs(mouse_positions[i][1] - mouse_positions[i-1][1]) for i in range(1, len(mouse_positions))]
        warning = sum(movements) < WARNING_THRESHOLD
    else:
        warning = False

    
    activity_data = {
        "employee_id": employee_id,
        "employee_name": employee_name,
        "timestamp": datetime.now(timezone.utc),
        "working": working,
        "status": status,
        "warning": warning
    }

    if employee_name != "Unknown" and int(time.time()) % 5 == 0:
        activity_collection.insert_one(activity_data)

    for timestamp, face_frame in list(unknown_face_timers.items()):
        if time.time() - timestamp > 60:
            image_path = os.path.join(UNKNOWN_FACES_DIR, f"unknown_{int(timestamp)}.jpg")
            cv2.imwrite(image_path, face_frame)
            print(f"Saved unknown face to {image_path}")
            del unknown_face_timers[timestamp]

    cv2.imshow("Employee Monitoring", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

video_capture.release()
cv2.destroyAllWindows()
mouse_listener.stop()
keyboard_listener.stop()
