from typing import Union, Tuple, List
import cv2

from .enums import TypeEnum as type
from .enums import Side as side
from .exceptions import InvalidFlagException

from .webcam import WebCam

def init(
        screen_size: Union[Tuple[int, int], List[int]],
        video_capture: Union[cv2.VideoCapture, int] = 0,
        *flags: Union[int, type]
):
    from .constants import CONFIG
    CONFIG.SCREEN_WIDTH, CONFIG.SCREEN_HEIGHT = screen_size
    CONFIG.VIDEO_CAPTURE = WebCam(video_capture)
    
    for flag in set(flags):
        value = flag.value if isinstance(flag, type) else flag
        
        if value == 0:
            pass
        elif value == 1:
            pass
        elif value == 2:
            pass
        else:
            raise InvalidFlagException(f"Invalid Flag {flag}, use a tracking.type value")