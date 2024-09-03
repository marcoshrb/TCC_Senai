from ..enums.side import SideEnum as Side
from ..landmarks import Landmarks

class Hand:
    def __init__(self, side: Side, landmarks: Landmarks):
        self.side = side
        self.landmarks = landmarks