import numpy as np

from abc import ABC, abstractmethod
from typing import List, Tuple, Union

from . import constants

from ..enums.side import SideEnum as Side
from ..landmarks import Landmarks

from .. import finger as FingerEnum

class HandAbstract(ABC):
    @property
    def side(self) -> Side:
        return self._side
    
    @property
    def landmarks(self) -> Landmarks:
        return self._landmarks
    
    @abstractmethod
    def finger_size(self, finger: FingerEnum) -> float:
        pass
    
    @abstractmethod
    def center_palm(self) -> np.ndarray:
        pass

    @abstractmethod
    def finger_is_raised(self, finger: FingerEnum, threshold: float = .7) -> bool:
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

# Implements the contants in the Hand abstract class
for name, value in [(name, getattr(constants, name))
                    for name in dir(constants)
                    if not name.startswith('_')]:
    if not callable(value) and not isinstance(value, type(constants)):
        setattr(HandAbstract, name, value)