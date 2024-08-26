import math
import numpy as np

class Math:
    @staticmethod
    def center(points: list) -> tuple:
        points = np.mean(points, axis=0)
        return tuple(points)

    @staticmethod
    def direction(a:tuple, b:tuple) -> tuple:
        dir = [a - b for a, b in zip(a, b)]
        length = math.sqrt(sum([d ** 2 for d in dir]))
        if length == 0:
            return [0] * len(dir)
        return tuple([dir / length for dir in dir])