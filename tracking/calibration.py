import json
from typing import Union
import numpy as np

from .exceptions import IncorrectInstanceException
from .utils import math

class Calibration:
    def __init__(self, shape:tuple):
        matrix = np.ndarray(shape, dtype=object)
        it = np.nditer(matrix, flags=['multi_index', 'refs_ok'])
        for _ in it:
            matrix[it.multi_index] = ([[] for _ in range(len(shape))], None)
                
        self._matrix = matrix
        
    @classmethod
    def from_matrix(cls, matrix:np.ndarray) -> 'Calibration':
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
            
        instance = cls(matrix.shape)
        instance._matrix = matrix.copy()
        return instance
    
    @classmethod
    def from_file(cls, file:str) -> 'Calibration':
        with open(file, 'r') as file:
            data = json.load(file)
            shape = tuple(data['shape'])
            dim = len(shape)
            values = np.array(data['values'], dtype=object)

        instance = cls(shape)
        it = np.nditer(instance._matrix, flags=['multi_index', 'refs_ok'])
        for _ in it:
            index = it.multi_index
            value = values[index].tolist() if isinstance(values[index], np.ndarray) else values[index]
            if not isinstance(value, list) or len(value) != dim:
                raise Exception('Values ​​in the file are incompatible with the model shape')
            mean = np.array([np.mean(val) for val in value])
            instance[index] = (value, mean)
        return instance
    
    def __getitem__(self, index):
        shape = len(index)
        value = self._matrix[index]
        if shape != len(self._matrix.shape):
            return value
        if value[1] is None:
            value = (value[0], np.mean(value[0], axis=1))
            self._matrix[index] = value
        return value[1]
    
    def __setitem__(self, index, value):
        self._matrix[index] = value
                
    def append(self, index: tuple, value: tuple):
        shape = len(index)
        if shape != len(self._matrix.shape):
            raise IncorrectInstanceException(f'index=tuple[{shape}]', f'index=tuple[{len(self._matrix.shape)}]', 'Incorrect index dimesions')
        for i in range(shape):
            self._matrix[index][0][i].append(value[i])
            self._matrix[index] = (self._matrix[index][0], None)

    def normalize(self, values) -> tuple:
        shape = self._matrix.shape
        it = np.nditer(self._matrix, flags=['multi_index', 'refs_ok'])
        ref = tuple([0.5] * len(shape))

        minimum_distance = math.inf
        minimum_start = None
        minimum_norms = None

        for _ in it:
            start = it.multi_index
            end = tuple(i + 1 for i in start)

            if 0 in set((shape - end for shape, end in zip(shape, end))):
                continue

            start_values = self[start]
            end_values = self[end]

            norms = [
                (x - min) / (max - min) 
                for min, max, x 
                in zip(start_values, end_values, values)]
            
            if all(0 <= x <= 1 for x in norms):
                return tuple(min + norm for min, norm in zip(start, norms))
            
            distance = math.euclidean_distance(norms, ref)
            if distance < minimum_distance:
                minimum_distance = distance
                minimum_start = start
                minimum_norms = norms
                
        return tuple(min + norm for min, norm in zip(minimum_start, minimum_norms))
    
    def predict(self, values, dimension:tuple, gap:Union[int, tuple] = 0) -> tuple:
        shape = self._matrix.shape
        dim = len(shape)

        if not isinstance(gap, tuple):
            gap = [gap] * dim

        square = [(dim - gap * 2) / shape for shape, dim, gap in zip(shape, dimension, gap)]
        norms = self.normalize(values)
        result = (gap + (size * value) for value, size, gap in zip(norms, square, gap))

        return tuple(result)
    
    def to_json(self):
        shape = self._matrix.shape
        values = np.ndarray(shape, dtype=object)
        it = np.nditer(values, flags=['multi_index', 'refs_ok'])
        for _ in it:
            index = it.multi_index
            values[index] = self._matrix[index][0]
        return {"shape": list(shape), "values": values.tolist()}

    def save(self, file:str):
        with open(file, 'w') as file:
            json.dump(self.to_json(), file, indent=4)