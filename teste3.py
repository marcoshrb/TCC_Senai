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

def calculate_direction(face_landmarks, largura, comprimento):

    ponto_central = face_landmarks.landmark[ponto_central_idx]
    ponto_esquerda = face_landmarks.landmark[ponto_esquerda_idx]
    ponto_direita = face_landmarks.landmark[ponto_direita_idx]

    ponto_central_cv = mp_drawing._normalized_to_pixel_coordinates(ponto_central.x, ponto_central.y, largura, comprimento)
    ponto_esquerda_cv = mp_drawing._normalized_to_pixel_coordinates(ponto_esquerda.x, ponto_esquerda.y, largura, comprimento)
    ponto_direita_cv = mp_drawing._normalized_to_pixel_coordinates(ponto_direita.x, ponto_direita.y, largura, comprimento)

    distancia_esquerda = math.sqrt((ponto_central_cv[0] - ponto_esquerda_cv[0])**2 + (ponto_central_cv[1] - ponto_esquerda_cv[1])**2)
    distancia_direita = math.sqrt((ponto_central_cv[0] - ponto_direita_cv[0])**2 + (ponto_central_cv[1] - ponto_direita_cv[1])**2)

    if distancia_esquerda > distancia_direita:
        return "Direita"
    elif distancia_direita > distancia_esquerda:
        return "Esquerda"
    else:
        return "Centro"

with mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5, refine_landmarks=True) as facemesh:
    while cap.isOpened():

        successo, frame = cap.read()

        if not successo:
            print("Ignorando o frame vazio da camêra.")
            continue

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        saida_facemesh = facemesh.process(frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        comprimento, largura, _ = frame.shape

        try:
            for face_landmarks in saida_facemesh.multi_face_landmarks:
                for id_coord in [ponto_central_idx, ponto_esquerda_idx, ponto_direita_idx]:
                    coord_xyz = face_landmarks.landmark[id_coord]
                    coord_cv = mp_drawing._normalized_to_pixel_coordinates(coord_xyz.x, coord_xyz.y, largura, comprimento)
                    cv2.circle(frame, coord_cv, 2, (255, 0, 0), -1)

                # for id, landmark in enumerate(face[474:478]):
                #     # mudar aq para mover o mouse uma maneira melhor

                #     x = int(landmark.x * largura)
                #     y = int(landmark.y * comprimento)
                #     if id == 0 :
                #         screen_x = int(screen_w / largura * x)
                #         screen_y = int(screen_h / comprimento * y)
                #         screen_x = screen_w - screen_x
                #         pyautogui.moveTo(screen_x, screen_y)

                direcao = calculate_direction(face_landmarks, largura, comprimento)
                frame = cv2.flip(frame, 1)
                cv2.putText(frame, f"Direcao: {direcao}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

        except:
            pass
        
        
        cv2.imshow('Camera', frame)
        if cv2.waitKey(10) & 0xFF == ord('c'):
            break
        
cap.release()
cv2.destroyAllWindows()