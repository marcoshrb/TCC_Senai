from typing import List, Tuple
import cv2
import numpy as np

from ..landmarks import Landmarks
from ..enums.side import SideEnum as Side
from ..exceptions import InvalidFlagException, IncorrectInstanceException

class EyeDetector:
    LEFT_EYE_IDX = [362, 385, 387, 263, 373, 380]
    RIGHT_EYE_IDX = [33, 160, 158, 133, 153, 144]
    
    def __init__(self, side: Side):
        if side not in [Side.LEFT, Side.RIGHT]:
            raise InvalidFlagException("expected tracking.side.LEFT or tracking.side.RIGHT")
        self._side = side
        
    def predict(self, landmarks: Landmarks) -> Tuple[List[float], Tuple[tuple, tuple]]:
        self._get_image_shape(landmarks._image)
        
        IDXs = EyeDetector.LEFT_EYE_IDX if self._side == Side.LEFT else EyeDetector.RIGHT_EYE_IDX
        points = landmarks._get_pixels(IDXs)
        
        image, mask, rect = self._cut_eye(landmarks._image, points)
        image = self._apply_threshold(image, mask)
        
        indices = np.argwhere(image == 0)
        if len(indices) == 0:
            return np.mean(list(rect), axis=0) - rect[0], rect
        return np.mean(indices, axis=0)[::-1], rect
        
    def _get_image_shape(self, image: np.ndarray) -> Tuple[int, int]:
        shape = image.shape
        if len(shape) != 2:
            raise IncorrectInstanceException(f"(shape: {shape})", "(shape: (h, w))", "Try convert to grayscale")
        return shape
    
    def _cut_eye(self, image: np.ndarray, 
                 points: List[Tuple[int, int]]
                ) -> Tuple[np.ndarray, np.ndarray, Tuple[tuple, tuple]]:
        points = np.array(points)
        
        minimum = np.min(points, axis=0)
        maximum = np.max(points, axis=0)
        
        image = image[minimum[1]:maximum[1], minimum[0]:maximum[0]]
        mask = np.zeros_like(image, dtype=np.uint8)
        
        points = [(x - minimum[0], y - minimum[1]) for x, y in points]
        points = np.array(points, dtype=np.int32).reshape((-1, 1, 2))
        cv2.fillPoly(mask, [points], 255)
        
        return image, mask, (minimum, maximum)
    
    def _apply_threshold(self, image: np.ndarray, mask: np.ndarray) -> np.ndarray:
        image = cv2.resize(image, (300, 100), interpolation=cv2.INTER_LINEAR)
        mask = cv2.resize(mask, (300, 100), interpolation=cv2.INTER_LINEAR)
        
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