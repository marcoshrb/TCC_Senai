from typing import List, Tuple, Union
import numpy as np

from tracking.constants import CONFIG, MP_FACE_MESH
from tracking.landmarks import Landmarks

from .face_detector import FaceDetector

class Tracking:
    def __init__(
            self, max_num_faces = 1, 
            refine_landmarks=False,
            min_detection_confidence = 0.5, 
            min_tracking_confidence = 0.5
        ):
        self.facemesh = MP_FACE_MESH.FaceMesh(
            max_num_faces = max_num_faces,
            refine_landmarks = refine_landmarks,
            min_detection_confidence = min_detection_confidence,
            min_tracking_confidence = min_tracking_confidence)
        self.face = FaceDetector()
        
    def predict(self, image: Union[np.ndarray, None] = None) -> Tuple[List[tuple], List[Landmarks]]:
        landmarks = self.process(image)
        directions = [self.face.predict(landmark) for landmark in landmarks]
        
        return directions, landmarks
        
    def process(self, image: Union[np.ndarray, None] = None) -> List[Landmarks]:
        if image is None:
            _, image = CONFIG.VIDEO_CAPTURE.read()
        
        facemesh = self.facemesh.process(image)
        if facemesh.multi_face_landmarks:
            return [Landmarks(image, face.landmark) for face in facemesh.multi_face_landmarks]
        
        return []