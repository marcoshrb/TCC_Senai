from typing import Union

from ..constants import CONFIG, MP_DRAWING

def normalize_pixel(
        x: Union[int, float],
        y: Union[int, float],
        width: Union[int, float] = None,
        height: Union[int, float] = None):
    
    return MP_DRAWING._normalized_to_pixel_coordinates(
        x, y, 
        width or CONFIG.VIDEO_CAPTURE.width, 
        height or CONFIG.VIDEO_CAPTURE.height)