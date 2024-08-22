from typing import List, Tuple
import cv2
import numpy as np

from ..utils import normalize_pixel

from ..enums.side import Side
from ..exceptions import InvalidFlagException, IncorrectInstanceException

class Eye:
    LEFT_EYE_IDX = [362, 385, 387, 263, 373, 380]
    RIGHT_EYE_IDX = [33, 160, 158, 133, 153, 144]
    
    def __init__(self, side: Side):
        if side not in [Side.LEFT, Side.RIGHT]:
            raise InvalidFlagException("expected tracking.side.LEFT or tracking.side.RIGHT")
        self._side = side
        
    def predict(self, image: np.ndarray, landmarks: list) -> List[int | float]:
        height, width = self._get_image_shape(image)
        points = self._get_points(landmarks)
        
        image, mask, (minimum, _) = self._cut_eye(image, points)
        
    def _get_points(self, landmarks: list) -> List[Tuple[int | float, int | float]]:
        IDXs = Eye.LEFT_EYE_IDX if self._side == Side.LEFT else Eye.RIGHT_EYE_IDX
        return [
            normalize_pixel(point.x, point.y)
            for point 
            in [landmarks[idx] for idx in IDXs]]
        
    def _get_image_shape(self, image: np.ndarray) -> Tuple[int | float, int | float]:
        shape = image.shape
        if len(shape) != 2:
            raise IncorrectInstanceException(f"(shape: {shape})", "(shape: (h, w))", "Try convert to grayscale")
        return shape
    
    def _cut_eye(self, image: np.ndarray, 
                 points: List[Tuple[int | float, int | float]]
                ) -> Tuple[np.ndarray, np.ndarray, Tuple[int | float, int | float]]:
        points = np.array(points)
        
        minimum = np.min(points, axis=0)
        maximum = np.max(points, axis=0)
        
        