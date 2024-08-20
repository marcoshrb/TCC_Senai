from typing import Union
import cv2

class WebCam:
    def __init__(self, video_capture: Union[cv2.VideoCapture, int] = 0,):
        self._video_capture = video_capture if isinstance(video_capture, cv2.VideoCapture) else cv2.VideoCapture(video_capture)
    
    def close(self):
        self._video_capture.release()