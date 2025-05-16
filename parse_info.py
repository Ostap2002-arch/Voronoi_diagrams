import sys
from os.path import dirname, abspath
import numpy as np
from shapely.geometry import Polygon
from typing import Tuple


def load_data(PATH_TO_BORDER: str, PATH_TO_WELLS: str) -> Tuple[Polygon, np.array, np.array]:
    """Функция загрузки данных: границы и координаты скважин.
    :arg
    :param PATH_TO_WELLS: путь к данным скважин
    :param PATH_TO_BORDER: путь к данным контура
    :return Tuple - кортеж из полигона, данных о скважинах в формате np.array, информации о локусах
    """
    border_data = np.loadtxt(PATH_TO_BORDER)[:, :2]
    wells_data = np.loadtxt(PATH_TO_WELLS, skiprows=5)[:, :2]

    # Создание рандомные данных (от 1 до 100), для каждой скважины
    # В дальнейшем можно импортировать какую-то информацию

    values_locus = np.random.randint(0, 100, size=len(wells_data[:, 0]))

    return Polygon(border_data), wells_data, values_locus
