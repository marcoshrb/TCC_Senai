import numpy as np

from .exceptions import IncorrectInstanceException

class Calibration:
    def __init__(self, shape:tuple, gap:int = 0):
        matrix = np.ndarray(shape, dtype=object)
        it = np.nditer(matrix, flags=['multi_index', 'refs_ok'])
        for _ in it:
            matrix[it.multi_index] = ([[] for _ in range(len(shape))], None)
                
        self._matrix = matrix
        self._gap = gap
        
    @classmethod
    def from_matrix(cls, matrix:np.ndarray, gap:int = 0) -> 'Calibration':
        if not isinstance(matrix, np.ndarray) or matrix.dtype != object:
            raise IncorrectInstanceException(type(matrix), np.ndarray, 'dtype=object')
        it = np.nditer(matrix, flags=['multi_index'])
        for _ in it:
            index = it.multi_index
            value = matrix[index]
            if type(value) is list:
                matrix[index] = (value, None)
            elif type(value) != tuple or type(value[0]) != list:
                raise IncorrectInstanceException(
                    f'{type(value)}: ({[type(v) for v in value[:2]]})', 
                    f'({np.ndarray}: ({list}, None || number)) or ({np.ndarray}: {list})')
            
        instance = cls(matrix.shape, gap=gap)
        instance._matrix = matrix.copy()
        return instance
    
    def __getitem__(self, index):
        shape = len(index)
        value = self._matrix[index]
        if shape != len(self._matrix.shape):
            return value
        if value[1] is None:
            value[1] = np.mean(value[0], axis=1)
        return value[1]
    
    def __setitem__(self, index, value):
        self._matrix[index] = value
                
    def append(self, index, value):
        shape = len(index)
        if shape != len(self._matrix.shape):
            raise IncorrectInstanceException(f'index=tuple[{shape}]', f'index=tuple[{len(self._matrix.shape)}]', 'Incorrect index dimesions')
        for i in range(shape):
            self._matrix[index][0][i].append(value[i])