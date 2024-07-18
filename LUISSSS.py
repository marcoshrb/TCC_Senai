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


def center(points):
    length = len(points)
    dimensions = len(points[0])
    
    center = [0] * dimensions

    for point in points:
        for i in range(dimensions):
            center[i] += point[i]

    return tuple([c / length for c in center])

def direction(a, b):
    dir = [a[i] - b[i] for i in range(len(a))]
    length = math.sqrt(sum([d ** 2 for d in dir]))
    if length == 0:
        return [0] * len(dir)
    return tuple([dir[i] / length for i in range(len(dir))])

def distanceTo(point, direction, distance):
    return tuple([point[i] + direction[i] * distance for i in range(len(point))])

def normalize(value, min, max):
    return (value - min) / (max - min)

def rescale(value, originalscale, targetscale):
    return targetscale[0] + (normalize(value, originalscale[0], originalscale[1]) * (targetscale[1] - targetscale[0]))

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
                ponto_esquerdo = face_landmarks.landmark[ponto_esquerda_idx]
                ponto_direito = face_landmarks.landmark[ponto_direita_idx]

                
                centro_point = center([(ponto_direito.x, ponto_direito.y, ponto_direito.z),(ponto_esquerdo.x, ponto_esquerdo.y, ponto_esquerdo.z)])
                direcao = direction((ponto_central.x, ponto_central.y, ponto_central.z), centro_point)
                direcao = direcao[:-1]
                
                print(direcao)
                screen_x = rescale(direcao[0], (0.3, -0.3), (0, screen_w))
                screen_y = rescale(direcao[1], (-0.4, 0), (0, screen_h))

                pyautogui.moveTo(screen_x, screen_y)

                # ponto_central_cv = mp_drawing._normalized_to_pixel_coordinates(ponto_central.x, ponto_central.y, shape_x, shape_y)

                # screen_x = int(ponto_central_cv[0] * screen_w / shape_x)
                # screen_y = int(ponto_central_cv[1] * screen_h / shape_y)

                # screen_x = screen_w - screen_x
                
                # pyautogui.moveTo(screen_x, screen_y)
        except:
            pass
        
        # centro_x = int(shape_x / 2)
        # centro_y = int(shape_y / 2)
        # cv2.circle(frame, (centro_x, centro_y), 2, (255, 0, 0), -1)
        # cv2.circle(frame, (shape_x - 3, centro_y), 2, (255, 0, 0), -1)
        # cv2.circle(frame, (5, centro_y), 2, (255, 0, 0), -1)

        frame = cv2.flip(frame, 1)
        
        cv2.imshow('Camera', frame)
        if cv2.waitKey(10) & 0xFF == ord('c'):
            break
        
cap.release()
cv2.destroyAllWindows()