import numpy as np

from ..abstract import HandAbstract

from ... import finger as FingerEnum
from ...utils import math

class MeasuresMethods(HandAbstract):
    def finger_size(self, finger: FingerEnum):
        points = sorted(FingerEnum.get_points(finger))
        points = self.landmarks._get_points(points)

        sizes = [
            math.euclidean_distance(points[i], points[i + 1])
            for i in range(len(points) - 1)]
        return sum(sizes)
    
    def center_palm(self):
        indexes = self.HAND_PALM
        points = self.landmarks._get_points(indexes)
        return np.mean(points, axis=0)