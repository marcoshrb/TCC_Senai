import cv2
import mediapipe as mp
import numpy as np
import pyautogui

mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh
screen_w, screen_h = pyautogui.size()

p_olho_esquerdo = [385, 380, 387, 373, 362, 263]
p_olho_direito = [160, 144, 158, 153, 33, 133]
p_olhos = p_olho_esquerdo + p_olho_direito

def calculo_ear(face, p_olho_dir, p_olho_esq):
    try:
        face = np.array([[coord.x, coord.y] for coord in face])
        face_esq = face[p_olho_esq, :]
        face_dir = face[p_olho_dir, :]

        ear_esq = (np.linalg.norm(face_esq[0] - face_esq[1]) + np.linalg.norm(face_esq[2] - face_esq[3])) / (2 * (np.linalg.norm(face_esq[4] - face_esq[5])))
        ear_dir = (np.linalg.norm(face_dir[0] - face_dir[1]) + np.linalg.norm(face_dir[2] - face_dir[3])) / (2 * (np.linalg.norm(face_dir[4] - face_dir[5])))
    except:
        ear_esq = 0.0
        ear_dir = 0.0
    
    return ear_esq, ear_dir
    
ear_linear = 0.2
cap = cv2.VideoCapture(1)

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
                face = face_landmarks.landmark

                for id, landmark in enumerate(face[474:478]):
                    # mudar aq para mover o mouse uma maneira melhor

                    x = int(landmark.x * largura)
                    y = int(landmark.y * comprimento)
                    if id == 0 :
                        screen_x = int(screen_w / largura * x)
                        screen_y = int(screen_h / comprimento * y)
                        screen_x = screen_w - screen_x
                        pyautogui.moveTo(screen_x, screen_y)

                for id_coord, coord_xyz in enumerate(face):
                    if id_coord in p_olhos:
                        coord_cv = mp_drawing._normalized_to_pixel_coordinates(coord_xyz.x, coord_xyz.y, largura, comprimento)
                        cv2.circle(frame, coord_cv, 2, (255, 0, 0), -1)
                ear_esquerda, ear_direita = calculo_ear(face, p_olho_direito, p_olho_esquerdo)
                
                if ear_esquerda < ear_linear and ear_direita > ear_linear:
                    pyautogui.click()

        except:
            pass

        cv2.imshow('Camera', frame)
        if cv2.waitKey(10) & 0xFF == ord('c'):
            break
        
cap.release()
cv2.destroyAllWindows()