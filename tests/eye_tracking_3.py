import cv2
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import mediapipe as mp
import pyautogui

from utils import landmarkToTuple, draw_sequence_lines

mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh
screen_w, screen_h = pyautogui.size()

cap = cv2.VideoCapture(0)

##### INDEXES #####
face_idx = [356, 9, 127]

left_eye_idx = [385, 380, 387, 373, 362, 263]
right_eye_idx = [160, 144, 158, 153, 33, 133]

left_pupil_idx = 473
right_pupil_idx = 468
###################

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

def init():
    ax.grid(False)

    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_zticklabels([])

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    
    return fig, ax

facemesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
    refine_landmarks=True
)

def update(frame):
    if not cap.isOpened():
        return fig,
    
    successo, frame = cap.read()
    if not  successo:
        return fig,
    
    saida_facemesh = facemesh.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    ax.cla()
    
    if saida_facemesh.multi_face_landmarks:
        face_landmarks = saida_facemesh.multi_face_landmarks[0]
            
        face = [landmarkToTuple(face_landmarks.landmark[idx]) for idx in face_idx]
        left_eye = [landmarkToTuple(face_landmarks.landmark[idx]) for idx in left_eye_idx]
        rigth_eye = [landmarkToTuple(face_landmarks.landmark[idx]) for idx in right_eye_idx]
        left_pupil = landmarkToTuple(face_landmarks.landmark[left_pupil_idx])
        right_pupil = landmarkToTuple(face_landmarks.landmark[right_pupil_idx])
        
        draw_sequence_lines(ax, face)
        
ani = FuncAnimation(fig, update, frames=range(100), init_func=init, blit=True)

plt.show()