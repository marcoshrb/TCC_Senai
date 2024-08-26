from typing import List, Tuple

import numpy as np

from ..utils import math

from ..landmarks import Landmarks
from ..exceptions import IncorrectInstanceException

class Face:
    FACE_LEFT_IDX = 356
    FACE_CENTER_IDX = 9
    FACE_RIGHT_IDX = 127
    
    def predict(self, landmarks: Landmarks) -> List[float]:
        self._get_image_shape(landmarks._image)
        
        IDXs = [Face.FACE_LEFT_IDX, Face.FACE_CENTER_IDX, Face.FACE_RIGHT_IDX]
        left_point, center_point, right_point = landmarks._get_points(IDXs)
        
        mean_point = math.center([left_point, right_point])
        direction = math.direction(center_point, mean_point)
        
        return direction
        
    def _get_image_shape(self, image: np.ndarray) -> Tuple[int, int]:
        shape = image.shape
        if len(shape) != 2:
            raise IncorrectInstanceException(f"(shape: {shape})", "(shape: (h, w))", "Try convert to grayscale")
        return shape