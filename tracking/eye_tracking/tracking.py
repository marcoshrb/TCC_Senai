from typing import List, Tuple, Union
import cv2
import numpy as np

from tracking.constants import CONFIG
from tracking.landmarks import Landmarks

from .eye_detector import EyeDetector
from .eye import Eye

from ..enums.side import SideEnum as Side
from ..face_tracking import Tracking as FaceTracking

class Tracking:
    def __init__(
            self, max_num_faces = 1, 
            refine_landmarks=False,
            min_detection_confidence = 0.5, 
            min_tracking_confidence = 0.5
        ):
        self.face_tracking = FaceTracking(
            max_num_faces=max_num_faces,
            refine_landmarks=refine_landmarks,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )
        self.left_eye = EyeDetector(Side.LEFT)
        self.right_eye = EyeDetector(Side.RIGHT)
        
    def predict(self, image: Union[np.ndarray, None] = None) -> List[Tuple[Eye, Eye]]:
        landmarks = self.face_tracking.process(image)
        landmarks = [Landmarks(cv2.cvtColor(landmark._image, cv2.COLOR_BGR2GRAY), landmark._landmarks) for landmark in landmarks]
        
        results = [(
                self.left_eye.predict(landmark), 
                self.right_eye.predict(landmark))
            for landmark 
            in landmarks]
            
        eyes = [(
            Eye(Side.LEFT, *result[0]),
            Eye(Side.RIGHT, *result[1])
        ) 
            for result 
            in results]
        
        return eyes