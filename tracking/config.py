from typing import Optional
from .webcam import WebCam

from .exceptions import IncorrectInstanceException

class Config:
    def __init__(self):
        self._screen_width = 0
        self._screen_height = 0
        self._video_capture = None
            
    @property
    def SCREEN_WIDTH(self) -> int:
        return self._screen_width
    
    @SCREEN_WIDTH.setter
    def SCREEN_WIDTH(self, value: int):
        if not isinstance(value, int):
            raise IncorrectInstanceException(type(value), int)
        self._screen_width = value
        
    @property
    def SCREEN_HEIGHT(self) -> int:
        return self._screen_height
    
    @SCREEN_HEIGHT.setter
    def SCREEN_HEIGHT(self, value: int):
        if not isinstance(value, int):
            raise IncorrectInstanceException(type(value), int)
        self._screen_height = value
        
    @property
    def VIDEO_CAPTURE(self) -> Optional[WebCam]:
        return self._video_capture
    
    @VIDEO_CAPTURE.setter
    def VIDEO_CAPTURE(self, value: WebCam):
        if not isinstance(value, WebCam):
            raise IncorrectInstanceException(type(value), WebCam)
        self._video_capture = value