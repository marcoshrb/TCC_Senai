from . import constants
from .partials.drawing_hand import DrawMethods

from ..enums.side import SideEnum as Side
from ..landmarks import Landmarks

class Hand(DrawMethods):    
    def __init__(self, side: Side, landmarks: Landmarks):
        self.side = side
        self.landmarks = landmarks

# Implements the contants in the Hand class
for name, value in [(name, getattr(constants, name)) 
                    for name in dir(constants) 
                    if not name.startswith('_')]:
    if not callable(value) and not isinstance(value, type(constants)):
        setattr(Hand, name, value)