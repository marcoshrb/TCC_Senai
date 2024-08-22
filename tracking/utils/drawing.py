from typing import Union

from ..constants import CONFIG, MP_DRAWING

def normalize_pixel(
        x: Union[int, float],
        y: Union[int, float],
        width: Union[int, float] = CONFIG.SCREEN_WIDTH,
        height: Union[int, float] = CONFIG.SCREEN_HEIGHT):
    return MP_DRAWING._normalized_to_pixel_coordinates(x, y, width, height)