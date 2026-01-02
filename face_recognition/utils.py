from requests.exceptions import RequestException 
import requests
import face_recognition
import cv2
import numpy as np

# Configuration
API_BASE_URL = "http://localhost:5000" # Assuming backend is running locally

def get_face_encoding(image):
    """
    Detects face and returns the 128-d encoding.
    Returns None if no face or multiple faces found.
    """
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    boxes = face_recognition.face_locations(rgb_image)
    
    if len(boxes) == 0:
        print("No face detected.")
        return None

    if len(boxes) > 1:
        print("Multiple faces detected. Please ensure only one person is in frame.")
        return None
        
    encodings = face_recognition.face_encodings(rgb_image, boxes)
    return encodings[0]

def register_student_api(name, encoding, block='D'):
    """
    Sends registration data to the backend.
    """
    url = f"{API_BASE_URL}/register_student"
    payload = {
        "name": name,
        "face_encoding": encoding.tolist(),
        "block": block
    }

    try:
        res = requests.post(url, json=payload)
        return res.json(), res.status_code

    except RequestException as e:
        print(f"Error connecting to backend: {e}")
        return None, 500

def fetch_known_encodings():
    """
    Fetches all known student encodings from the backend.
    Returns a dictionary mapping ID to details.
    """
    url = f"{API_BASE_URL}/get_encodings"
    try:
        res = requests.get(url)
        if res.status_code == 200:
            return res.json()
        else:
            print(f"Failed to fetch encodings: {res.status_code}")
            return {}
    except RequestException as e:
        print(f"Error connecting to backend: {e}")
        return {}

def recognize_face(image, known_encodings_dict):
    """
    Matches the face in the image against known encodings.
    Returns (student_id, name) if match found, else (None, None).
    """
    unknown_encoding = get_face_encoding(image)
    if unknown_encoding is None:
        return None, None

    known_ids = []
    known_encodings = []
    
    for s_id, data in known_encodings_dict.items():
        known_ids.append(s_id)
        known_encodings.append(np.array(data['encoding']))

    if not known_encodings:
        return None, None

    matches = face_recognition.compare_faces(known_encodings, unknown_encoding, tolerance=0.5)
    face_distances = face_recognition.face_distance(known_encodings, unknown_encoding)
    
    best = np.argmin(face_distances)
    if matches[best]:
        student_id = known_ids[best]
        name = known_encodings_dict[student_id]['name']
        return student_id, name
    
    return None, None
