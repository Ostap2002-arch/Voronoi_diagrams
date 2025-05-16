import sys
from os.path import dirname, abspath

import numpy as np
from typing import Tuple

sys.path.insert(0, dirname(abspath(__file__)))
from ar import earcut


def ear(X: np.ndarray, Y: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Триангуляция полигона
    :arg
    :param X: координаты х
    :param Y: координаты y
    :return Кортеж из массива i, j, k, используемых для построения в go.Mesh3d
    """
    data = []
    for x, y in zip(X, Y):
        data.append(x)
        data.append(y)

    tri = earcut(data)
    return np.array(tri[0::3]), np.array(tri[1::3]), np.array(tri[2::3])
