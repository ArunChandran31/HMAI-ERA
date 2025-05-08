import cv2
import face_recognition

# Load image using OpenCV
image = cv2.imread("data/arun.jpg")  # Replace with actual path

# Convert from BGR to RGB
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Process with face_recognition
encoding = face_recognition.face_encodings(image)