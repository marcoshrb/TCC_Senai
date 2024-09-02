from typing import List, Tuple
from ..enums.side import SideEnum as Side

class Eye:
    def __init__(self, side: Side, predict: List[float], rect: Tuple[tuple, tuple]):
        self.side = side
        self.result = predict
        self.rect = rect
        
        self._predict = predict
        self._normalized = None
        self._position = None
        
    def __repr__(self):
        return repr(self.result)
        
    @property
    def left(self):
        return self.rect[0][0]
    
    @property
    def right(self):
        return self.rect[1][0]
    
    @property
    def top(self):
        return self.rect[0][1]
    
    @property
    def bottom(self):
        return self.rect[1][1]
        
    @property
    def width(self):
        return self.right - self.left
    
    @property
    def height(self):
        return self.bottom - self.top
        
    @property
    def normalized(self):
        if self._normalized is None:
            self._normalized = (self.result[0] / 300, self.result[1] / 100)
            
        return self._normalized
    
    @property
    def position(self):
        if self._position is None:
            x, y = self.normalized
            self._position = (x * 300, y * 100)
        
        return self._position
    
    @property
    def x(self):
        return self.position[0]
    
    @property
    def y(self):
        return self.position[1]