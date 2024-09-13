from typing import List, Tuple, Union

import cv2
import numpy as np

from ... import finger
from ...utils.drawing import normalize_pixel

class DrawMethods:
    def draw(self,
             image: np.ndarray,
             color: Tuple[int, int, int],
             point_scale:Tuple[int, int] = (10, 75),
             connections: bool = True,
             thickness: int = 2,
             palm: bool = True,
             fingers: List[Union[int, finger]] = [
                 finger.THUMB,
                 finger.INDEX,
                 finger.MIDDLE,
                 finger.RING,
                 finger.PINKY]):
        hand_connections = set()
        if palm:
            hand_connections = hand_connections.union(self.HAND_PALM_CONNECTIONS if connections else self.HAND_PALM)
        for f in fingers:
            if f == finger.THUMB:
                hand_connections = hand_connections.union(self.HAND_THUMB_CONNECTIONS if connections else self.HAND_THUMB)
            if f == finger.INDEX:
                hand_connections = hand_connections.union(self.HAND_INDEX_FINGER_CONNECTIONS if connections else self.HAND_INDEX)
            if f == finger.MIDDLE:
                hand_connections = hand_connections.union(self.HAND_MIDDLE_FINGER_CONNECTIONS if connections else self.HAND_MIDDLE)
            if f == finger.RING:
                hand_connections = hand_connections.union(self.HAND_RING_FINGER_CONNECTIONS if connections else self.HAND_RING)
            if f == finger.PINKY:
                hand_connections = hand_connections.union(self.HAND_PINKY_FINGER_CONNECTIONS if connections else self.HAND_PINKY)
        
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
                radius = int((1 - norm) * (point_scale[1] - point_scale[0]))
                image = cv2.circle(image, pt, radius, color, -1)
                
        return image