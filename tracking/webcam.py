from typing import Tuple, Union
import numpy as np
import cv2

from .exceptions import IncorrectInstanceException

class WebCam:
    def __init__(self, video_capture: Union[cv2.VideoCapture, int] = 0):
        self._video_capture = video_capture if isinstance(video_capture, cv2.VideoCapture) else cv2.VideoCapture(video_capture)
        self._frame = None
        self._width = 0
        self._height = 0
      
    def read(self) -> Tuple[bool, np.ndarray]:
        sucess, frame = self._video_capture.read()
        if sucess:
            self._frame = frame
            return sucess, frame
        return sucess, self._frame
    
    @property
    def width(self) -> Union[int, float]:
        return self._width
    
    @property
    def height(self) -> Union[int, float]:
        return self._height
    
    @property
    def frame(self) -> np.ndarray:
        return self._frame
    
    @frame.setter
    def frame(self, value: np.ndarray):
        if not isinstance(value, np.ndarray):
            raise IncorrectInstanceException(type(value), np.ndarray)
        self._height, self._width = value.shape[:2]
        self._frame = value
        
    @property
    def isOpened(self) -> bool:
        return self._video_capture.isOpened()
    
    def close(self):
        self._video_capture.release()