from typing import List, Union
import numpy as np
from tracking.constants import CONFIG, MP_FACE_MESH
from tracking.landmarks import Landmarks

class Tracking:
    def __init__(
            self, max_num_faces = 1, 
            min_detection_confidence = 0.5, 
            min_tracking_confidence = 0.5
        ):
        self.facemesh = MP_FACE_MESH.FaceMesh(
            max_num_faces = max_num_faces,
            min_detection_confidence = min_detection_confidence,
            min_tracking_confidence = min_tracking_confidence)
        
    def predict(self, image: Union[np.ndarray, None] = None) -> List[Landmarks]:
        if image is None:
            _, image = CONFIG.VIDEO_CAPTURE.read()
        
        facemesh = self.facemesh.process(image)
        if facemesh.multi_face_landmarks:
            return [Landmarks(image, face.landmark) for face in facemesh.multi_face_landmarks]
        
        return []