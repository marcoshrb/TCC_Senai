import mediapipe as mp

from .drawing_hand import DrawMethods

from ..enums.side import SideEnum as Side
from ..landmarks import Landmarks

class Hand(DrawMethods):
    HAND_PALM_CONNECTIONS = mp.solutions.hands_connections.HAND_PALM_CONNECTIONS
    HAND_THUMB_CONNECTIONS = mp.solutions.hands_connections.HAND_THUMB_CONNECTIONS
    HAND_INDEX_FINGER_CONNECTIONS = mp.solutions.hands_connections.HAND_INDEX_FINGER_CONNECTIONS
    HAND_MIDDLE_FINGER_CONNECTIONS = mp.solutions.hands_connections.HAND_MIDDLE_FINGER_CONNECTIONS
    HAND_RING_FINGER_CONNECTIONS = mp.solutions.hands_connections.HAND_RING_FINGER_CONNECTIONS
    HAND_PINKY_FINGER_CONNECTIONS = mp.solutions.hands_connections.HAND_PINKY_FINGER_CONNECTIONS
    
    HAND_PALM = set().union(*HAND_PALM_CONNECTIONS)
    HAND_THUMB = set().union(*HAND_THUMB_CONNECTIONS)
    HAND_INDEX = set().union(*HAND_INDEX_FINGER_CONNECTIONS)
    HAND_MIDDLE = set().union(*HAND_MIDDLE_FINGER_CONNECTIONS)
    HAND_RING = set().union(*HAND_RING_FINGER_CONNECTIONS)
    HAND_PINKY = set().union(*HAND_PINKY_FINGER_CONNECTIONS)
    
    def __init__(self, side: Side, landmarks: Landmarks):
        self.side = side
        self.landmarks = landmarks