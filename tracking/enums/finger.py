from enum import Enum

class FingerEnum(Enum):
    THUMB   = 0
    INDEX   = 1
    MIDDLE  = 2
    RING    = 3
    PINKY   = 4
    
    @classmethod
    def get_tip(cls, finger:'FingerEnum'):
        points = sorted(cls.get_points(finger))
        return points[-1]

    @classmethod
    def get_points(cls, finger:'FingerEnum'):
        from ..hand_tracking import constants
        if finger == cls.THUMB:
            return constants.HAND_THUMB
        elif finger == cls.INDEX:
            return constants.HAND_INDEX
        elif finger == cls.MIDDLE:
            return constants.HAND_MIDDLE
        elif finger == cls.RING:
            return constants.HAND_RING
        elif finger == cls.PINKY:
            return constants.HAND_PINKY
        else:
            raise ValueError("Invalid finger")
        
    @classmethod
    def get_connections(cls, finger:'FingerEnum'):
        from ..hand_tracking import constants
        if finger == cls.THUMB:
            return constants.HAND_THUMB_CONNECTIONS
        elif finger == cls.INDEX:
            return constants.HAND_INDEX_FINGER_CONNECTIONS
        elif finger == cls.MIDDLE:
            return constants.HAND_MIDDLE_FINGER_CONNECTIONS
        elif finger == cls.RING:
            return constants.HAND_RING_FINGER_CONNECTIONS
        elif finger == cls.PINKY:
            return constants.HAND_PINKY_FINGER_CONNECTIONS
        else:
            raise ValueError("Invalid finger")