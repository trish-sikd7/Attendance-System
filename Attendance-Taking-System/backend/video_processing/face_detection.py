import cv2
import face_recognition
import numpy as np
import os
import csv
import datetime
from video_processing.database_module import get_student_details,save_student_attendance
import json

KNOWN_FACES_DIR = 'known_faces'
TOLERANCE = 0.4

known_faces = []
known_names = []

# Load known faces
for file in os.listdir(KNOWN_FACES_DIR):
    if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
        # Extract student ID from the file name
        student_id = os.path.splitext(file)[0]  # Extracts '1001' from '1001.jpg'

        image = face_recognition.load_image_file(os.path.join(KNOWN_FACES_DIR, file))
        encoding = face_recognition.face_encodings(image)[0]
        known_faces.append(encoding)
        known_names.append(student_id)

# Function to check if the person's attendance is already marked within 10 minutes


def is_attendance_marked(id):
    current_time = datetime.datetime.now()
    if not os.path.exists('attendance.csv'):
        with open('attendance.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Id','Name', 'Timestamp'])
        return False

    with open('attendance.csv', mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == id:
                attendance_time = datetime.datetime.strptime(
                    row[2], "%Y-%m-%d %H:%M:%S.%f")
                if (current_time - attendance_time).seconds < 600:
                    return True
    return False

# Function to handle the video stream for face recognition


async def handle_stream(data, websocket):
    try:
        content = data  # Content received from the frontend (frame data)
        nparr = np.frombuffer(content, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        response = {}

        # Perform face recognition
        face_locations = face_recognition.face_locations(image)

        if len(face_locations) == 0:  # No face detected
            response['message'] = "No face detected"
            response['student_data'] = {}
            await websocket.send_json((response))
            return
        elif len(face_locations) > 1:  # Multiple faces detected
            response['message'] = "Multiple faces detected. Can't mark attendance"
            response['student_data'] = {}
            await websocket.send_json((response))
            return

        unknown_face_encodings = face_recognition.face_encodings(
            image, face_locations)

        for face_encoding in unknown_face_encodings:
            matches = face_recognition.compare_faces(
                known_faces, face_encoding, TOLERANCE)

            match_index = next(
                (i for i, match in enumerate(matches) if match), None)

            if match_index is not None:
                student_id = known_names[match_index]
                student_data = get_student_details(student_id)
                name = student_data['name']

                if not is_attendance_marked(student_id):
                    with open('attendance.csv', mode='a', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow([student_id,name, datetime.datetime.now()])
                        student_data['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    save_student_attendance(student_data, content)
                    response['message'] = f"Attendance marked for {name}"
                else:
                    response['message'] = f"{name} - Your attendance was already taken recently"
                response['student_data'] = student_data
                await websocket.send_json((response))
                return

        # No match found
        response['message'] = "Face not recognized as any known student"
        response['student_data'] = {}
        await websocket.send_json(response)

    except Exception as e:
        print(e)