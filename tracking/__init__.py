from typing import Union, Tuple, List
import cv2

from .config import Config
from .enums import TypeEnum as type
from .exceptions import InvalidFlagException

def init(
        screen_size: Union[Tuple[int, int], List[int]],
        video_capture: Union[cv2.VideoCapture, int] = 0,
        *flags: Union[int, type]
):
    Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT = screen_size
    Config.VIDEO_CAPTURE = video_capture if isinstance(video_capture, cv2.VideoCapture) else cv2.VideoCapture(video_capture)
    
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