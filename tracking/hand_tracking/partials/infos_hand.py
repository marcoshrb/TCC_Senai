import numpy as np

from ..abstract import HandAbstract

from ... import finger as FingerEnum
from ...utils import math

class InfosMethods(HandAbstract):
    def finger_is_raised(self, finger: FingerEnum, threshold: float = .7) -> bool:
        center_palm = self.landmarks._get_points(self.HAND_PALM)
        center_palm = np.mean(center_palm, axis=0)
        
        size = self.finger_size(finger)
        finger_tip = self.landmarks._get_points([FingerEnum.get_tip(finger)])[0]

        distance = math.euclidean_distance(finger_tip, center_palm)
        
        print(f'{size * threshold} < {distance}')
        return size * threshold < distance