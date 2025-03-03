import socketio
import csv
import numpy as np
from enum import Enum
from angleCalculation import calculate_angle
class PoseLandmark(Enum):
    NOSE = 0
    LEFT_EYE_INNER = 1
    LEFT_EYE = 2
    LEFT_EYE_OUTER = 3
    RIGHT_EYE_INNER = 4
    RIGHT_EYE = 5
    RIGHT_EYE_OUTER = 6
    LEFT_EAR = 7
    RIGHT_EAR = 8
    MOUTH_LEFT = 9
    MOUTH_RIGHT = 10
    LEFT_SHOULDER = 11
    RIGHT_SHOULDER = 12
    LEFT_ELBOW = 13
    RIGHT_ELBOW = 14
    LEFT_WRIST = 15
    RIGHT_WRIST = 16
    LEFT_PINKY = 17
    RIGHT_PINKY = 18
    LEFT_INDEX = 19
    RIGHT_INDEX = 20
    LEFT_THUMB = 21
    RIGHT_THUMB = 22
    LEFT_HIP = 23
    RIGHT_HIP = 24
    LEFT_KNEE = 25
    RIGHT_KNEE = 26
    LEFT_ANKLE = 27
    RIGHT_ANKLE = 28
    LEFT_HEEL = 29
    RIGHT_HEEL = 30
    LEFT_FOOT_INDEX = 31
    RIGHT_FOOT_INDEX = 32
    
def extract_angles(landmarks):
    angles = {
        "left_elbow": calculate_angle(landmarks[PoseLandmark.LEFT_SHOULDER.value], landmarks[PoseLandmark.LEFT_ELBOW.value], landmarks[PoseLandmark.LEFT_WRIST.value]),
        "right_elbow": calculate_angle(landmarks[PoseLandmark.RIGHT_SHOULDER.value], landmarks[PoseLandmark.RIGHT_ELBOW.value], landmarks[PoseLandmark.RIGHT_WRIST.value]),
        "left_shoulder": calculate_angle(landmarks[PoseLandmark.LEFT_HIP.value], landmarks[PoseLandmark.LEFT_SHOULDER.value], landmarks[PoseLandmark.LEFT_WRIST.value]),
        "right_shoulder": calculate_angle(landmarks[PoseLandmark.RIGHT_HIP.value], landmarks[PoseLandmark.RIGHT_SHOULDER.value], landmarks[PoseLandmark.RIGHT_WRIST.value]),
        "left_knee": calculate_angle(landmarks[PoseLandmark.LEFT_HIP.value], landmarks[PoseLandmark.LEFT_KNEE.value], landmarks[PoseLandmark.LEFT_ANKLE.value]),
        "right_knee": calculate_angle(landmarks[PoseLandmark.RIGHT_HIP.value], landmarks[PoseLandmark.RIGHT_KNEE.value], landmarks[PoseLandmark.RIGHT_ANKLE.value]),
        "left_hip": calculate_angle(landmarks[PoseLandmark.LEFT_SHOULDER.value], landmarks[PoseLandmark.LEFT_HIP.value], landmarks[PoseLandmark.LEFT_KNEE.value]),
        "right_hip": calculate_angle(landmarks[PoseLandmark.RIGHT_SHOULDER.value], landmarks[PoseLandmark.RIGHT_HIP.value], landmarks[PoseLandmark.RIGHT_KNEE.value]),
        "left_ankle": calculate_angle(landmarks[PoseLandmark.LEFT_KNEE.value], landmarks[PoseLandmark.LEFT_ANKLE.value], landmarks[PoseLandmark.LEFT_FOOT_INDEX.value]),
        "right_ankle": calculate_angle(landmarks[PoseLandmark.RIGHT_KNEE.value], landmarks[PoseLandmark.RIGHT_ANKLE.value], landmarks[PoseLandmark.RIGHT_FOOT_INDEX.value]),
        "left_wrist": calculate_angle(landmarks[PoseLandmark.LEFT_ELBOW.value], landmarks[PoseLandmark.LEFT_WRIST.value], landmarks[PoseLandmark.LEFT_INDEX.value]),
        "right_wrist": calculate_angle(landmarks[PoseLandmark.RIGHT_ELBOW.value], landmarks[PoseLandmark.RIGHT_WRIST.value], landmarks[PoseLandmark.RIGHT_INDEX.value]),
        "left_foot": calculate_angle(landmarks[PoseLandmark.LEFT_ANKLE.value], landmarks[PoseLandmark.LEFT_FOOT_INDEX.value], landmarks[PoseLandmark.LEFT_HEEL.value]),
        "right_foot": calculate_angle(landmarks[PoseLandmark.RIGHT_ANKLE.value], landmarks[PoseLandmark.RIGHT_FOOT_INDEX.value], landmarks[PoseLandmark.RIGHT_HEEL.value]),
        "left_body": calculate_angle(landmarks[PoseLandmark.LEFT_SHOULDER.value], landmarks[PoseLandmark.LEFT_HIP.value], landmarks[PoseLandmark.LEFT_ANKLE.value]),
        "right_body": calculate_angle(landmarks[PoseLandmark.RIGHT_SHOULDER.value], landmarks[PoseLandmark.RIGHT_HIP.value], landmarks[PoseLandmark.RIGHT_ANKLE.value])
    }
    return angles


sio = socketio.Server()
app = socketio.WSGIApp(sio)
output_csv = "exercise_data.csv"
with open(output_csv, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["exercise_name", "left_elbow", "right_elbow", "left_shoulder", "right_shoulder", "left_knee", "right_knee", "left_hip", "right_hip", "left_ankle", "right_ankle", "left_wrist", "right_wrist", "left_foot", "right_foot", "left_body", "right_body"])

# Handle incoming landmarks data
@sio.event
def connect(sid, environ):
    print('Client connected:', sid)

@sio.event
def disconnect(sid):
    print('Client disconnected:', sid)

@sio.event
def landmarks(sid, data):
    exercise_name = data['exercise_name']
    landmarks = data['landmarks']
    angles = extract_angles(landmarks)
    
    with open(output_csv, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([exercise_name, angles["left_elbow"], angles["right_elbow"], angles["left_shoulder"], angles["right_shoulder"], angles["left_knee"], angles["right_knee"], angles["left_hip"], angles["right_hip"], angles["left_ankle"], angles["right_ankle"], angles["left_wrist"], angles["right_wrist"], angles["left_foot"], angles["right_foot"], angles["left_body"], angles["right_body"]])

# Run the server
if __name__ == '__main__':
    import eventlet
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)