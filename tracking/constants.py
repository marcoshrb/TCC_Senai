import mediapipe as mp

from tracking.config import Config

CONFIG = Config()
MP_DRAWING = mp.solutions.drawing_utils
MP_FACE_MESH = mp.solutions.face_mesh
MP_HAND_MESH = mp.solutions.hands