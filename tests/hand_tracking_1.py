import sys
import cv2
import mediapipe as mp

sys.path.append('./')
import tracking as tck

from tracking.landmarks import Landmarks
from tracking.hand_tracking import Hand

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)
cv2.namedWindow('Camera', cv2.WINDOW_NORMAL)

with mp_hands.Hands() as hands:
    while cap.isOpened():
        sucess, frame = cap.read()
        
        if not sucess:
            continue
        
        hands_objs = []
        results = hands.process(frame)
        if results.multi_hand_landmarks:
            hands_objs = [Hand(
                tck.side.mirror(tck.side.from_string(hand.classification[0].label)),
                Landmarks(frame, marks.landmark))
                     for hand, marks
                     in zip(results.multi_handedness, results.multi_hand_landmarks)]
            
            print(mp_hands.HAND_CONNECTIONS)
        
        cv2.imshow('Camera', frame)
        
        if cv2.waitKey(10) & 0xFF == 27:
            break