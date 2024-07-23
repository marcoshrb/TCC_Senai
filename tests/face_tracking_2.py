import cv2
import mediapipe as mp
import numpy as np
import time

mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh

p_olho_esquerdo = [385, 380, 387, 373, 362, 263]
p_olho_direito = [160, 144, 158, 153, 33, 133]
# pupila_direito = [468, 469, 470, 471, 472]
pupila_direito = [468]
# pupila_esquerda = [473, 474, 475, 476, 477]
pupila_esquerda = [473]

p_olhos = p_olho_esquerdo + p_olho_direito + pupila_direito + pupila_esquerda

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
    media_ear = (ear_esq + ear_dir) / 2
    return media_ear

def where_to_look(face, p_olho_dir, p_olho_esq, pupila_dir, pupila_esq):
    try:
        face = np.array([[coord.x, coord.y] for coord in face])
        p_olho_esq = face[p_olho_esq, :]
        p_olho_dir = face[p_olho_dir, :]
        pupila_dir = face[pupila_dir, :]
        pupila_esq = face[pupila_esq, :]

        vetor_esq = np.mean(pupila_esq - p_olho_esq, axis=0)
        vetor_dir = np.mean(pupila_dir - p_olho_dir, axis=0)

        vetor_esq /= np.linalg.norm(vetor_esq)
        vetor_dir /= np.linalg.norm(vetor_dir)

        if np.dot(vetor_dir, [1, 0]) > 0.5: 
            return "Esquerda"
        elif np.dot(vetor_esq, [-1, 0]) > 0.5:  
            return "Direita"
        else:
            return "Frente" 
    except Exception as e:
        print(f"Erro ao determinar direção do olhar: {e}")
        return "Indeterminado"


ear_linear = 0.3
dormindo = 0

cap = cv2.VideoCapture(0)
with mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5, refine_landmarks=True) as facemesh:
    while cap.isOpened():
        successo, frame = cap.read()
        if not successo:
            print("Ignorando o frame vazio da camêra.")
            continue
        comprimento, largura, fps = frame.shape

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        saida_facemesh = facemesh.process(frame)

        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        try:
            for face_landmarks in saida_facemesh.multi_face_landmarks:
                # mp_drawing.draw_landmarks(frame, face_landmarks, mp_face_mesh.FACEMESH_CONTOURS,
                # landmark_drawing_spec = mp_drawing.DrawingSpec(color=(255,102,102), thickness=1, circle_radius=1),
                # connection_drawing_spec = mp_drawing.DrawingSpec(color=(102,204,0), thickness=1, circle_radius=1))

                face = face_landmarks.landmark
                for id_coord, coord_xyz in enumerate(face):
                    if id_coord in p_olhos:
                        coord_cv = mp_drawing._normalized_to_pixel_coordinates(coord_xyz.x, coord_xyz.y, largura, comprimento)
                        cv2.circle(frame, coord_cv, 2, (255, 0, 0), -1)
                ear = calculo_ear(face, p_olho_direito, p_olho_esquerdo)
                cv2.rectangle(frame, (0, 1), (290, 140), (58, 58, 55), -1)
                cv2.putText(frame, f"EAR: {round(ear, 2)}", (1, 24), cv2.FONT_HERSHEY_DUPLEX, 0.9, (255, 255, 255), 2)

                direcao_olhar = where_to_look(face, p_olho_direito, p_olho_esquerdo, pupila_direito, pupila_esquerda)
                cv2.putText(frame, f"Direcao do Olhar: {direcao_olhar}", (1, 100), cv2.FONT_HERSHEY_DUPLEX, 0.9, (255, 255, 255), 2)
                
                if ear < ear_linear:
                    t_inicial = time.time() if dormindo == 0 else t_inicial
                    dormindo = 1
                if dormindo == 1 and ear >= ear_linear:
                    dormindo = 0
                t_final = time.time()

                tempo = (t_final - t_inicial) if dormindo == 1 else 0.0

                cv2.putText(frame, f"Tempo: {round(tempo, 3)}", (1, 80), cv2.FONT_HERSHEY_DUPLEX, 0.9, (255, 255, 255), 2)
                if tempo >= 1.5:
                    cv2.rectangle(frame, (30, 400), (610, 452), (109, 233, 219), -1)
                    cv2.putText(frame, f"Acorda Baiano!", (80, 435), cv2.FONT_HERSHEY_DUPLEX, 0.85, (58,58,55), 1)
        except:
            pass

        cv2.imshow('Camera', frame)

        if cv2.waitKey(10) & 0xFF == ord('c'):
            break
cap.release()
cv2.destroyAllWindows()