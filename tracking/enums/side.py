from enum import Enum

class SideEnum(Enum):
    LEFT    = 0
    RIGHT   = 1
    
    @classmethod
    def mirror(cls, side):
        if side == cls.LEFT:
            return cls.RIGHT
        if side == cls.RIGHT:
            return cls.LEFT
        raise ValueError("Invalid side")
    
    @classmethod
    def from_string(cls, side: str):
        return cls[side.upper()]