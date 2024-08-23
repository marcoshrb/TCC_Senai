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
        
    def predict(self, image: np.ndarray, landmarks: list) -> List[float]:
        height, width = self._get_image_shape(image)
        points = self._get_points(landmarks, width, height)
        
        image, mask, _ = self._cut_eye(image, points)
        image = self._apply_threshold(image, mask)
        
        indices = np.argwhere(image == 0)
        return np.mean(indices, axis=0)
        
    def _get_points(self, landmarks: list, width: int, height: int) -> List[Tuple[int, int]]:
        IDXs = Eye.LEFT_EYE_IDX if self._side == Side.LEFT else Eye.RIGHT_EYE_IDX
        return [
            normalize_pixel(point.x, point.y, width, height)
            for point 
            in [landmarks[idx] for idx in IDXs]]
        
    def _get_image_shape(self, image: np.ndarray) -> Tuple[int, int]:
        shape = image.shape
        if len(shape) != 2:
            raise IncorrectInstanceException(f"(shape: {shape})", "(shape: (h, w))", "Try convert to grayscale")
        return shape
    
    def _cut_eye(self, image: np.ndarray, 
                 points: List[Tuple[int, int]]
                ) -> Tuple[np.ndarray, np.ndarray, Tuple[int, int]]:
        points = np.array(points)
        
        minimum = np.min(points, axis=0)
        maximum = np.max(points, axis=0)
        
        image = image[minimum[1]:maximum[1], minimum[0]:maximum[0]]
        mask = np.zeros_like(image, dtype=np.uint8)
        
        points = [(x - minimum[0], y - minimum[0]) for x, y in points]
        points = np.array(points, dtype=np.int32).reshape((-1, 1, 2))
        cv2.fillPoly(mask, [points], 255)
        
        return image, mask, (minimum, max)
    
    def _apply_threshold(self, image: np.ndarray, mask: np.ndarray) -> np.ndarray:
        image = cv2.bitwise_and(image, image, mask=mask)
        image = cv2.adaptiveThreshold(
            image, 
            255, 
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY, 
            11, 
            2
        )
        
        background = np.ones_like(image, np.uint8) * 255
        background = cv2.bitwise_and(background, background, mask=~mask)
        
        return cv2.add(image, background)