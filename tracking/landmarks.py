from typing import List, Tuple
from numbers import Number

import numpy as np

from .utils import normalize_pixel

class Landmarks:
    def __init__(self, image: np.ndarray, landmarks: list):
        self._image = image
        self._landmarks = landmarks
        
    def _get_points(self, indexes: list) -> List[Tuple[Number, Number, Number]]:
        '''
        Returns:
        3D coordinades list
        '''
        return [
            (point.x, point.y, point.z)
            for point
            in [self._landmarks[idx] for idx in indexes]]
        
    def _get_pixels(self, indexes: list) -> List[Tuple[Number, Number]]:
        '''
        Returns:
        2D coordinades list
        '''
        height, width = self._image.shape[:2]
        return [
            normalize_pixel(point.x, point.y, width, height)
            for point
            in [self._landmarks[idx] for idx in indexes]]