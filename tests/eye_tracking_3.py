import cv2
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import mediapipe as mp
import pyautogui

from utils import center, direction, distance, distanceTo, landmarkToTuple, draw_sequence_lines, draw_line, draw_point

mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh
screen_w, screen_h = pyautogui.size()

cap = cv2.VideoCapture(0)

##### INDEXES #####
face_idx = [356, 9, 127]

left_eye_idx = [362, 385, 387, 263, 373, 380]
right_eye_idx = [33, 160, 158, 133, 153, 144]

left_pupil_idx = 473
right_pupil_idx = 468
###################

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

def clear():
    ax.clear()

    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_zticklabels([])

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

def init():
    ax.grid(False)
    
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
    clear()
    
    if saida_facemesh.multi_face_landmarks:
        face_landmarks = saida_facemesh.multi_face_landmarks[0]
            
        face = [landmarkToTuple(face_landmarks.landmark[idx]) for idx in face_idx]
        left_eye = [landmarkToTuple(face_landmarks.landmark[idx]) for idx in left_eye_idx]
        right_eye = [landmarkToTuple(face_landmarks.landmark[idx]) for idx in right_eye_idx]
        left_pupil = landmarkToTuple(face_landmarks.landmark[left_pupil_idx])
        right_pupil = landmarkToTuple(face_landmarks.landmark[right_pupil_idx])
        
        draw_sequence_lines(ax, face)
        for a, b in zip(left_eye, left_eye[1:] + [left_eye[0]]):
            draw_line(ax, a, b, 'red')
            
        for a, b in zip(right_eye, right_eye[1:] + [right_eye[0]]):
            draw_line(ax, a, b, 'red')
            
        draw_point(ax, left_pupil)
        draw_point(ax, right_pupil)
        
        face_center = center([face[0], face[2]])
        face_direction = direction(face_center, face[1])
        
        left_eye_size = distance(left_eye[4], left_eye[5])
        right_eye_size = distance(right_eye[4], right_eye[5])
        
        left_eye_center = distanceTo(center(left_eye), face_direction, left_eye_size)
        right_eye_center = distanceTo(center(right_eye), face_direction, right_eye_size)
        
        draw_point(ax, left_eye_center, 'blue')
        draw_point(ax, right_eye_center, 'blue')
        
        left_eye_direction = direction(left_pupil, left_eye_center)
        right_eye_direction = direction(right_pupil, right_eye_center)
        
        left_eye_vision = distanceTo(left_pupil, left_eye_direction, 0.1)
        right_eye_vision = distanceTo(right_pupil, right_eye_direction, 0.1)
        
        draw_line(ax, left_pupil, left_eye_vision, 'blue')
        draw_line(ax, right_pupil, right_eye_vision, 'blue')
        
    return fig,
        
ani = FuncAnimation(fig, update, frames=range(100), init_func=init, blit=False)

plt.show()