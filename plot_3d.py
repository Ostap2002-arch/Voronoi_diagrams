import sys
from os.path import dirname, abspath
from plotly.colors import sample_colorscale
from geovoronoi import voronoi_regions_from_coords
import numpy as np
from shapely.geometry import Polygon
import plotly.graph_objects as go

sys.path.insert(0, dirname(abspath(__file__)))
from ear_cropping import ear


def plot_voronoi_3d(border: Polygon, wells: np.array, height: np.array) -> go.Figure:
    """Функция создания диаграммы Вороного.
    :arg
    :param border: граница контура
    :param wells: данные по скважинам
    :param height: информация о локусах (массив чисел от 1 до 100)
    :return go.Figure -  график, но не показывает его
    """
    # Создание полигонов
    region_polys, region_pts = voronoi_regions_from_coords(wells, border)
    fig = go.Figure()

    # Работа с цветом
    colorscale = ['rgb(0, 0, 255)', 'rgb(255, 0, 0)']  # Основная палитра
    color_locus = (height - height.min()) / (height.max() - height.min())
    list_color = sample_colorscale(colorscale, color_locus)
    colors = {key: value for key, value in zip(region_polys.values(), list_color)}

    # Отрисовка локусов в объёме
    for poly, h in zip(region_polys.values(), height):
        x, y = poly.exterior.xy
        x = np.array(list(x))[::-1]
        x = x.astype(int)  # преобразует все элементы массива в int
        y = np.array(list(y))[::-1]
        y = y.astype(int)  # преобразует все элементы массива в int

        # Триангуляция с помощью метода
        i, j, k = ear(x, y)

        # Отрисовка "крышек" полигона
        fig.add_trace(
            go.Mesh3d(
                x=list(x),
                y=list(y),
                z=[0] * len(x),
                i=i,
                j=j,
                k=k,
                color=colors[poly],  # Цвет полигона
                flatshading=True
            )
        )

        fig.add_trace(
            go.Mesh3d(
                x=list(x),
                y=list(y),
                z=[h] * len(x),
                i=i,
                j=j,
                k=k,
                color=colors[poly],  # Цвет полигона
                flatshading=True
            )
        )

        # Ручная триангуляция боковой поверхности
        X = list()
        Y = list()
        Z = list()

        for i in range(len(x) * 2):
            if i % 2 == 0:
                Z.append(0)
            else:
                Z.append(h)
            X.append(x[i // 2])
            Y.append(y[i // 2])

        i = list(range(0, len(x) + len(x) - 1 - 1))
        j = list(range(1, len(x) + len(x) - 1))
        k = list(range(2, len(x) + len(x) - 1 + 1))

        # Отрисовка боковой поверхности полигона
        fig.add_trace(
            go.Mesh3d(
                x=X,
                y=Y,
                z=Z,
                i=i,
                j=j,
                k=k,
                color=colors[poly],  # Цвет полигона
                flatshading=True
            )
        )

    # Создание списка высот для каждой из скважин, так как высота привязана не к ним, а к полигонам
    heigh_wells = {value[0]: key for key, value in zip(height, region_pts.values())}
    heigh_wells = dict(sorted(heigh_wells.items()))
    heigh_wells = np.array(list(heigh_wells.values()))

    # Нанесение скважин и шкалы
    fig.add_trace(go.Scatter3d(
        x=wells[:, 0],
        y=wells[:, 1],
        z=heigh_wells,
        mode='markers',  # Режим отображения точек
        marker=dict(
            size=5,  # Размер точек
            color='black',  # Цвет в зависимости от z (можно задать массив цветов)
            colorscale=colorscale,
            cmin=0,
            cmax=100,
            colorbar=dict(
                tickvals=[1, 50, 100],
            )
        )))

    # Настройки макета
    fig.update_layout(
        title="Диаграмма Вороного с учётом границ залежи",
        width=800,
        height=800,
        hovermode="closest"
    )

    return fig
