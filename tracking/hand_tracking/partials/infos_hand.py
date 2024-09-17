import numpy as np

from ..abstract import HandAbstract

from ... import finger as FingerEnum
from ...utils import math

class InfosMethods(HandAbstract):
    def finger_is_raised(self, finger: FingerEnum, threshold: float = .7) -> bool:
        size = self.finger_size(finger)
        
        center_palm = self.center_palm()
        finger_tip = self.landmarks._get_points([FingerEnum.get_tip(finger)])[0]

        distance = math.euclidean_distance(finger_tip, center_palm)

        return size * threshold < distance