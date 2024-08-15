import numpy as np
import mediapipe as mp
import cv2

mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh

cap = cv2.VideoCapture(0)
cv2.namedWindow('Camera', cv2.WINDOW_NORMAL)

left_eye_idx = [362, 385, 387, 263, 373, 380]
right_eye_idx = [33, 160, 158, 133, 153, 144]

threshold = 50
with mp_face_mesh.FaceMesh(max_num_faces=1, min_detection_confidence=0.5, min_tracking_confidence=0.5) as facemesh:
    while cap.isOpened():
        successo, frame = cap.read()
        height, width = frame.shape[:2]
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        
        if not successo:
            continue
        
        saida_facemesh = facemesh.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        if saida_facemesh.multi_face_landmarks:
            face_landmarks = saida_facemesh.multi_face_landmarks[0]
            landmarks = [{
                '3D': (landmark.x, landmark.y, landmark.z),
                '2D': (mp_drawing._normalized_to_pixel_coordinates(landmark.x, landmark.y, width, height))} for landmark in face_landmarks.landmark]
            
            left_eye = np.array([landmarks[idx]['2D'] for idx in left_eye_idx if landmarks[idx]['2D'] is not None])
            right_eye = np.array([landmarks[idx]['2D'] for idx in right_eye_idx if landmarks[idx]['2D'] is not None])
            
            left_eye_box = (np.min(left_eye, axis=0), np.max(left_eye, axis=0))
            left_eye_relative = [(x - left_eye_box[0][0], y - left_eye_box[0][1]) for (x, y) in left_eye]
            left_eye_relative = np.array(left_eye_relative, dtype=np.int32).reshape((-1, 1, 2))
            
            left_eye_frame = gray_frame[left_eye_box[0][1]:left_eye_box[1][1], left_eye_box[0][0]:left_eye_box[1][0]]
            left_eye_mask = np.zeros(left_eye_frame.shape[:2], dtype=np.uint8)
            cv2.fillPoly(left_eye_mask, [left_eye_relative], 255)
            
            background = np.ones_like(left_eye_frame) * 255
            left_eye_frame = cv2.bitwise_and(left_eye_frame, left_eye_frame, mask=left_eye_mask)
            left_eye_frame = cv2.add(left_eye_frame, cv2.bitwise_and(background, background, mask=~left_eye_mask))
            
            left_eye_frame = cv2.resize(left_eye_frame, (300, 100), interpolation=cv2.INTER_LINEAR)
            _, left_eye_bin = cv2.threshold(left_eye_frame, threshold, 255, cv2.THRESH_BINARY)
            
            print(np.mean(np.argwhere(left_eye_bin == 0), axis=0))
            frame = left_eye_bin
        
        cv2.imshow('Camera', frame)
        key = cv2.waitKey(10) & 0xFF
        if key == 27:
            break
        elif key == 115:
            threshold -= 1
        elif key == 119:
            threshold += 1