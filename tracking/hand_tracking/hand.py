from . import partials

from ..enums.side import SideEnum as Side
from ..landmarks import Landmarks

class Hand(*[
        getattr(partials, name) 
        for name in dir(partials) 
        if name.endswith('Methods')]):  
      
    def __init__(self, side: Side, landmarks: Landmarks):
        self._side = side
        self._landmarks = landmarks