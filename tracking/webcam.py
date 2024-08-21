from typing import Tuple, Union
import numpy as np
import cv2

from .exceptions import IncorrectInstanceException

class WebCam:
    def __init__(self, video_capture: Union[cv2.VideoCapture, int] = 0):
        self._video_capture = video_capture if isinstance(video_capture, cv2.VideoCapture) else cv2.VideoCapture(video_capture)
        self._frame = None
      
    def read(self) -> Tuple[bool, np.ndarray]:
        sucess, frame = self._video_capture.read()
        return (sucess, frame if sucess else self._frame)
    
    @property
    def frame(self) -> np.ndarray:
        return self._frame()
    
    @frame.setter
    def frame(self, value: np.ndarray):
        if not isinstance(value, np.ndarray):
            raise IncorrectInstanceException(type(value), np.ndarray)
        self._frame = value
    
    def close(self):
        self._video_capture.release()