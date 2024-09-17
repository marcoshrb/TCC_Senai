from . import partials

from .abstract import HandAbstract
from ..enums.side import SideEnum as Side
from ..landmarks import Landmarks

class Hand(*[
        getattr(partials, name) 
        for name in dir(partials) 
        if name.endswith('Methods')], HandAbstract):  
      
    def __init__(self, side: Side, landmarks: Landmarks):
        self._side = side
        self._landmarks = landmarks