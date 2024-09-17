from typing import List, Tuple, Union

import cv2
import numpy as np

from ..abstract import HandAbstract

from ... import finger as FingerEnum
from ...utils.drawing import normalize_pixel

class DrawMethods(HandAbstract):
    def draw(self,
             image: np.ndarray,
             color: Tuple[int, int, int],
             point_scale:Tuple[int, int] = (10, 75),
             connections: bool = True,
             thickness: int = 2,
             palm: bool = True,
             fingers: List[Union[int, FingerEnum]] = [
                 FingerEnum.THUMB,
                 FingerEnum.INDEX,
                 FingerEnum.MIDDLE,
                 FingerEnum.RING,
                 FingerEnum.PINKY]):
        hand_connections = set()
        if palm:
            hand_connections = hand_connections.union(self.HAND_PALM_CONNECTIONS if connections else self.HAND_PALM)
        for f in fingers:
            hand_connections = hand_connections.union(FingerEnum.get_connections(f) if connections else FingerEnum.get_points(f))
        
        for connection in hand_connections:
            height, width = self.landmarks._image.shape[:2]
            if isinstance(connection, tuple):
                pts = self.landmarks._get_points([*connection])
                
                pt1 = pts[0]
                pt1 = normalize_pixel(pt1[0], pt1[1], width, height)
                
                pt2 = pts[1]
                pt2 = normalize_pixel(pt2[0], pt2[1], width, height)
                image = cv2.line(image, pt1, pt2, color, thickness)
            else:
                pts = self.landmarks._get_points([connection])
                
            for point in pts:
                pt = normalize_pixel(point[0], point[1], width, height)
                norm = min(max((point[2] + 1), 0), 1)
                radius = int(point_scale[0] + ((1 - norm) * (point_scale[1] - point_scale[0])))
                image = cv2.circle(image, pt, radius, color, -1)
                
        return image
    
    def draw_fingertips(self,
                   image: np.ndarray,
                   color: Tuple[int, int, int],
                   point_scale:Tuple[int, int] = (10, 75),
                   fingers: List[Union[int, FingerEnum]] = [
                       FingerEnum.THUMB,
                       FingerEnum.INDEX,
                       FingerEnum.MIDDLE,
                       FingerEnum.RING,
                       FingerEnum.PINKY]):
        fingerstips = []
        for f in fingers:
            if f == FingerEnum.THUMB:
                fingerstips.append(max(self.HAND_THUMB))
            if f == FingerEnum.INDEX:
                fingerstips.append(max(self.HAND_INDEX))
            if f == FingerEnum.MIDDLE:
                fingerstips.append(max(self.HAND_MIDDLE))
            if f == FingerEnum.RING:
                fingerstips.append(max(self.HAND_RING))
            if f == FingerEnum.PINKY:
                fingerstips.append(max(self.HAND_PINKY))

        height, width = self.landmarks._image.shape[:2]
        points = self.landmarks._get_points(fingerstips)
        for point in points:
            pt = normalize_pixel(point[0], point[1], width, height)
            norm = min(max(point[2] + 1, 0), 1)
            radius = int(point_scale[0] + ((1 - norm) * (point_scale[1] - point_scale[0])))
            image = cv2.circle(image, pt, radius, color, -1)

        return image