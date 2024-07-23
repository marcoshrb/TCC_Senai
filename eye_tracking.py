import cv2
import mediapipe as mp
import pyautogui

mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh
screen_w, screen_h = pyautogui.size()

cap = cv2.VideoCapture(0)

##### INDEXES #####
face_idx = [356, 9, 127]

left_eye_idx = [385, 380, 387, 373, 362, 263]
rigth_eye_idx = [160, 144, 158, 153, 33, 133]

pupila_direito = [468]
pupila_esquerda = [473]
###################

cv2.namedWindow('Camera', cv2.WINDOW_NORMAL)

with mp_face_mesh.FaceMesh(max_num_faces=1, min_detection_confidence=0.5, min_tracking_confidence=0.5, refine_landmarks=True) as facemesh:
    while cap.isOpened():
        successo, frame = cap.read()
        
        if not successo:
            continue
        
        saida_facemesh = facemesh.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        print("=================")
        
        if saida_facemesh.multi_face_landmarks:
            shape_y, shape_x, _ = frame.shape
            face_landmarks = saida_facemesh.multi_face_landmarks[0]
            
            for idx in face_idx:
                point = face_landmarks.landmark[idx]
                coord = mp_drawing._normalized_to_pixel_coordinates(point.x, point.y, shape_x, shape_y)
                cv2.circle(frame, coord, 2, (255, 0, 0), -1)
                print(f"{idx} = [{point.x}, {point.y}, {point.z}]")
                
            for idx in left_eye_idx + rigth_eye_idx:
                point = face_landmarks.landmark[idx]
                coord = mp_drawing._normalized_to_pixel_coordinates(point.x, point.y, shape_x, shape_y)
                cv2.circle(frame, coord, 1, (0, 255, 0), -1)
                print(f"{idx} = [{point.x}, {point.y}, {point.z}]")
                
            for idx in pupila_direito + pupila_esquerda:
                point = face_landmarks.landmark[idx]
                coord = mp_drawing._normalized_to_pixel_coordinates(point.x, point.y, shape_x, shape_y)
                cv2.circle(frame, coord, 5, (0, 0, 255), 2)
                print(f"{idx} = [{point.x}, {point.y}, {point.z}]")
            
        cv2.imshow('Camera', frame)
        if cv2.waitKey(10) & 0xFF == 27:
            break