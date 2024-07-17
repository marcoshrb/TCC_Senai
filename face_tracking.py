import cv2
import mediapipe as mp
import numpy as np
import pyautogui
import math

mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh
screen_w, screen_h = pyautogui.size()

ponto_central_idx = 9
ponto_esquerda_idx = 356
ponto_direita_idx = 127

cap = cv2.VideoCapture(0)

cv2.namedWindow('Camera', cv2.WINDOW_NORMAL)
cv2.setWindowProperty('Camera', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

max_x = 0
min_x = 0

def calculate_direction(face_landmarks, largura, comprimento):

    ponto_central = face_landmarks.landmark[ponto_central_idx]
    ponto_esquerda = face_landmarks.landmark[ponto_esquerda_idx]
    ponto_direita = face_landmarks.landmark[ponto_direita_idx]

    ponto_central_cv = mp_drawing._normalized_to_pixel_coordinates(ponto_central.x, ponto_central.y, largura, comprimento)
    ponto_esquerda_cv = mp_drawing._normalized_to_pixel_coordinates(ponto_esquerda.x, ponto_esquerda.y, largura, comprimento)
    ponto_direita_cv = mp_drawing._normalized_to_pixel_coordinates(ponto_direita.x, ponto_direita.y, largura, comprimento)

    distancia_esquerda = math.sqrt((ponto_central_cv[0] - ponto_esquerda_cv[0])**2 + (ponto_central_cv[1] - ponto_esquerda_cv[1])**2)
    distancia_direita = math.sqrt((ponto_central_cv[0] - ponto_direita_cv[0])**2 + (ponto_central_cv[1] - ponto_direita_cv[1])**2)

    print("distancia_direita: ", distancia_direita)
    print("distancia_esquerda: ", distancia_esquerda)

    if distancia_esquerda > distancia_direita:
        # valor = (distancia_esquerda - distancia_direita) * (-1)
        # valor = distancia_direita * (-1)
        valor = distancia_esquerda * (-1)
    elif distancia_direita > distancia_esquerda:
        # valor = distancia_direita - distancia_esquerda
        # valor = distancia_esquerda
        valor = distancia_direita
    else:
        valor = 0

    return valor

with mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5, refine_landmarks=True) as facemesh:
    while cap.isOpened():

        successo, frame = cap.read()

        if not successo:
            continue

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        saida_facemesh = facemesh.process(frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        shape_y, shape_x, _ = frame.shape

        try:
            for face_landmarks in saida_facemesh.multi_face_landmarks:
                
                
                ponto_central = face_landmarks.landmark[ponto_central_idx]
                ponto_central_cv = mp_drawing._normalized_to_pixel_coordinates(ponto_central.x, ponto_central.y, shape_x, shape_y)

                # valor = calculate_direction(face_landmarks, shape_x, shape_y)

                screen_x = int(ponto_central_cv[0] * screen_w / shape_x)
                screen_y = int(ponto_central_cv[1] * screen_h / shape_y)

                screen_x = screen_w - screen_x

                # if screen_x > max_x:
                max_x = screen_x
                
                cv2.circle(frame, (screen_x, screen_y), 2, (0, 0, 255), -1)    
                
                pyautogui.moveTo(screen_x, screen_y)
        except:
            pass
        
        centro_x = int(shape_x / 2)
        centro_y = int(shape_y / 2)
        cv2.circle(frame, (centro_x, centro_y), 2, (255, 0, 0), -1)
        cv2.circle(frame, (shape_x - 3, centro_y), 2, (255, 0, 0), -1)
        cv2.circle(frame, (5, centro_y), 2, (255, 0, 0), -1)

        frame = cv2.flip(frame, 1)
        
        cv2.imshow('Camera', frame)
        if cv2.waitKey(10) & 0xFF == ord('c'):
            break
        
cap.release()
cv2.destroyAllWindows()