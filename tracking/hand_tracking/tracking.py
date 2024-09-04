from collections import namedtuple
from typing import List, NamedTuple, Union

import numpy as np
import tracking as tck

from ..landmarks import Landmarks
from ..hand_tracking import Hand
from ..constants import CONFIG, MP_HAND_MESH

class Tracking:
    def __init__(self,
                 static_image_mode=False,
                 max_num_hands=2,
                 model_complexity=1,
                 min_detection_confidence=0.5,
                 min_tracking_confidence=0.5) -> None:
        self.handsmesh = MP_HAND_MESH.Hands(
            static_image_mode,
            max_num_hands,
            model_complexity,
            min_detection_confidence,
            min_tracking_confidence)
        
    def predict(self, image: Union[np.ndarray, None] = None, side_mirror = False):
        results = self.process(image)
        
        hands = [Hand((
            tck.side.mirror(tck.side.from_string(hand.label))
                if side_mirror 
                else tck.side.from_string(hand.label)),
            Landmarks(image, marks))
                 for hand, marks, image
                 in results]
        
        return hands
        
    def process(self, image: Union[np.ndarray, None] = None) -> List[NamedTuple]:
        if image is None:
            _, image = CONFIG.VIDEO_CAPTURE.read()
            
        hands = self.handsmesh.process(image)
        if hands.multi_hand_landmarks:
            Result = namedtuple('hand', ['classification', 'landmarks', 'image'])
            return [
                Result(
                    classification=hand.classification[0],
                    landmarks=marks.landmark,
                    image=image)
                for hand, marks
                in zip(hands.multi_handedness, hands.multi_hand_landmarks)
            ]
        return []