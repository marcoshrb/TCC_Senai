import cv2
import mediapipe as mp
import numpy as np
import pyautogui

from utils import center, direction, distance, distanceTo, landmarkToTuple, rescale

pyautogui.FAILSAFE = False

mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh
screen_w, screen_h = pyautogui.size()

cap = cv2.VideoCapture(0)

##### INDEXES #####
face_idx = [356, 9, 127]

left_eye_idx = [385, 380, 387, 373, 362, 263]
right_eye_idx = [160, 144, 158, 153, 33, 133]

left_pupil = 473
right_pupil = 468
###################

stabiler_size = 10
stabiler = [(0,0)] * stabiler_size

cv2.namedWindow('Camera', cv2.WINDOW_NORMAL)

with mp_face_mesh.FaceMesh(max_num_faces=1, min_detection_confidence=0.5, min_tracking_confidence=0.5, refine_landmarks=True) as facemesh:
    while cap.isOpened():
        successo, frame = cap.read()
        
        if not successo:
            continue
        
        print("=========")
        saida_facemesh = facemesh.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        
        if saida_facemesh.multi_face_landmarks:
            face_landmarks = saida_facemesh.multi_face_landmarks[0]
            
            face_center = center([landmarkToTuple(face_landmarks.landmark[0]), landmarkToTuple(face_landmarks.landmark[2])])
            face_direction = direction(face_center, landmarkToTuple(face_landmarks.landmark[1]))
            
            left_eye = [landmarkToTuple(face_landmarks.landmark[idx]) for idx in left_eye_idx]
            right_eye = [landmarkToTuple(face_landmarks.landmark[idx]) for idx in right_eye_idx]
            
            left_eye_size = distance(left_eye[4], left_eye[5])
            right_eye_size = distance(right_eye[4], right_eye[5])
            
            left_eye_center = distanceTo(center(left_eye), face_direction, left_eye_size / 2)
            right_eye_center = distanceTo(center(right_eye), face_direction, right_eye_size / 2)
            
            left_eye_direction = direction(landmarkToTuple(face_landmarks.landmark[left_pupil]), left_eye_center)
            right_eye_direction = direction(landmarkToTuple(face_landmarks.landmark[right_pupil]), right_eye_center)
            
            vision_direction = center([left_eye_direction, right_eye_direction])
            print(vision_direction)
            
            left_eye_top = center([left_eye[0], left_eye[2]])
            left_eye_bottom = center([left_eye[1], left_eye[3]])
            left_eye_angle = direction(left_eye_top, left_eye_bottom)
            
            right_eye_top = center([right_eye[0], right_eye[2]])
            right_eye_bottom = center([right_eye[1], right_eye[3]])
            right_eye_angle = direction(right_eye_top, right_eye_bottom)
            
            mid_direction = center([left_eye_angle, right_eye_angle])
            print(mid_direction)
            
            screen_x = rescale(vision_direction[0], (0.11, -0.27), (0, screen_w))
            screen_y = rescale(mid_direction[2], (-0.22, -0.28), (0, screen_h))
            
            stabiler.pop(0)
            stabiler.append((screen_x, screen_y))

            avg_x, avg_y = np.mean(stabiler, axis=0)
            pyautogui.moveTo(avg_x, avg_y)
            
        cv2.imshow('Camera', frame)
        if cv2.waitKey(10) & 0xFF == 27:
            break