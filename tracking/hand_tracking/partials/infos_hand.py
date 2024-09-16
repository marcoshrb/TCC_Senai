import numpy as np

from ... import finger as FingerEnum
from ...utils import math

class InfosHand:
    def finger_is_raised(self, finger: FingerEnum, threshold: float = .7):
        center_palm = self.landmarks._get_points(self.HAND_PALM)
        center_palm = np.mean(center_palm, axis=0)
        
        points = sorted(FingerEnum.get_points(finger))
        points = self.landmarks._get_points(points)
        
        size = sum([
            math.euclidean_distance(points[i], points[i + 1]) 
            for i in range(len(points) - 1)])
        distance = math.euclidean_distance(points[-1], center_palm)
        
        return size * threshold < distance