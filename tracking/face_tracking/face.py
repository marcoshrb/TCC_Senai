from ..utils import math

from ..landmarks import Landmarks

class Face:
    FACE_LEFT_IDX = 356
    FACE_CENTER_IDX = 9
    FACE_RIGHT_IDX = 127
    
    def predict(self, landmarks: Landmarks) -> tuple:
        IDXs = [Face.FACE_LEFT_IDX, Face.FACE_CENTER_IDX, Face.FACE_RIGHT_IDX]
        left_point, center_point, right_point = landmarks._get_points(IDXs)
        
        mean_point = math.center([left_point, right_point])
        direction = math.direction(center_point, mean_point)
        
        return direction