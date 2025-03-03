import numpy as np
from enum import Enum


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
    

def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    
    if angle > 180.0:
        angle = 360 - angle
        
    return angle



def process_pose_landmarks(landmarks, exercise_name, counting, counter, calories_burned):
    stage = None
    
       
    left_shoulder = [landmarks[PoseLandmark.LEFT_SHOULDER.value].x, 
                     landmarks[PoseLandmark.LEFT_SHOULDER.value].y]
    left_elbow = [landmarks[PoseLandmark.LEFT_ELBOW.value].x, 
                  landmarks[PoseLandmark.LEFT_ELBOW.value].y]
    left_wrist = [landmarks[PoseLandmark.LEFT_WRIST.value].x, 
                  landmarks[PoseLandmark.LEFT_WRIST.value].y]
    
    right_shoulder = [landmarks[PoseLandmark.RIGHT_SHOULDER.value].x, 
                      landmarks[PoseLandmark.RIGHT_SHOULDER.value].y]
    right_elbow = [landmarks[PoseLandmark.RIGHT_ELBOW.value].x, 
                   landmarks[PoseLandmark.RIGHT_ELBOW.value].y]
    right_wrist = [landmarks[PoseLandmark.RIGHT_WRIST.value].x, 
                   landmarks[PoseLandmark.RIGHT_WRIST.value].y]
    
    left_hip = [landmarks[PoseLandmark.LEFT_HIP.value].x, 
               landmarks[PoseLandmark.LEFT_HIP.value].y]
    right_hip = [landmarks[PoseLandmark.RIGHT_HIP.value].x, 
                landmarks[PoseLandmark.RIGHT_HIP.value].y]
    
    left_knee = [landmarks[PoseLandmark.LEFT_KNEE.value].x, 
                 landmarks[PoseLandmark.LEFT_KNEE.value].y]
    right_knee = [landmarks[PoseLandmark.RIGHT_KNEE.value].x, 
                  landmarks[PoseLandmark.RIGHT_KNEE.value].y]
    
    left_ankle = [landmarks[PoseLandmark.LEFT_ANKLE.value].x, 
                  landmarks[PoseLandmark.LEFT_ANKLE.value].y]
    right_ankle = [landmarks[PoseLandmark.RIGHT_ANKLE.value].x, 
                   landmarks[PoseLandmark.RIGHT_ANKLE.value].y]
      
    if exercise_name == "bicep_curl":
        left_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
        right_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)

        avg_angle = (left_angle + right_angle) / 2

        if avg_angle > 160:
            stage = "down"
        if avg_angle < 80 and stage == 'down':
            stage = "up"
            counter += 1
            calories_burned += 0.4
            print(counter)
    
    elif exercise_name == "front_raise":
        left_angle = calculate_angle(left_shoulder, left_hip, left_wrist)
        right_angle = calculate_angle(right_shoulder, right_hip, right_wrist)

        avg_angle = (left_angle + right_angle) / 2

        if avg_angle > 120:
            stage = "up"
        if avg_angle < 90 and stage == 'up':
            stage = "down"
            counter += 1
            calories_burned += 0.4
            print(counter)
    
    elif exercise_name == "squat":
        left_angle = calculate_angle(left_hip, left_knee, left_ankle)
        right_angle = calculate_angle(right_hip, right_knee, right_ankle)

        avg_angle = (left_angle + right_angle) / 2

        if avg_angle > 160:
            stage = "up"
        if avg_angle < 90 and stage == 'up':
            stage = "down"
            counter += 1
            calories_burned += 0.5
            print(counter)
    
    elif exercise_name == "pushup":
        if landmarks[PoseLandmark.LEFT_SHOULDER.value].visibility > landmarks[PoseLandmark.RIGHT_SHOULDER.value].visibility:
            # Use left side landmarks
            arm_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
            leg_angle = calculate_angle(left_hip, left_knee, left_ankle)
            body_angle = calculate_angle(left_shoulder, left_hip, left_ankle)
        else:
            # Use right side landmarks
            arm_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)
            leg_angle = calculate_angle(right_hip, right_knee, right_ankle)
            body_angle = calculate_angle(right_shoulder, right_hip, right_ankle)

        if arm_angle > 160 and leg_angle > 160 and body_angle > 160:
            stage = "up"
        if arm_angle < 90 and stage == 'up':
            stage = "down"
            counter += 1
            calories_burned += 0.3
            print(counter)
    
    return counter, calories_burned


# Example usage
landmarks = [...]  # Replace with actual landmarks data
exercise_name = "bicep_curl"
counting = True
counter = 0
calories_burned = 0.0

# counter, calories_burned = process_pose_landmarks(landmarks, exercise_name, counting, counter, calories_burned)