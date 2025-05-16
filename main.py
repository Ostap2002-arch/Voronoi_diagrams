import argparse

from plotly.colors import sample_colorscale
from geovoronoi import voronoi_regions_from_coords
import numpy as np
from shapely.geometry import Polygon
import plotly.graph_objects as go
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
    values_locus = (values_locus - values_locus.min()) / (values_locus.max() - values_locus.min())
    return Polygon(border_data), wells_data, values_locus


def create_voronoi_plot(border: Polygon, wells: np.array, values_locus: np.array) -> go.Figure:
    """Функция создания диаграммы Вороного.
    :arg
    :param border: граница контура
    :param wells: данные по скважинам
    :param values_locus: информация о локусах (массив чисел от 1 до 100)
    :return go.Figure -  график, но не показывает его
    """
    region_polys, _ = voronoi_regions_from_coords(wells, border)

    fig = go.Figure()

    # Получаем цвета локусов
    colorscale = ['rgb(0, 0, 255)', 'rgb(255, 0, 0)']
    colors = sample_colorscale(colorscale, values_locus)

    for i, poly in enumerate(region_polys.values()):
        x, y = poly.exterior.xy
        fig.add_trace(go.Scatter(
            x=list(x), y=list(y),
            fill="toself",
            fillcolor=colors[i],
            line=dict(color="black", width=2),
            hoverinfo="skip",
            showlegend=False,
            marker=dict(
                colorscale=colorscale,
                cmin=0,
                cmax=100,
                colorbar=dict(
                    tickvals=[1, 50, 100],
                )
            )
        ))

    # Скважины
    fig.add_trace(go.Scatter(
        x=wells[:, 0], y=wells[:, 1],
        mode="markers",
        marker=dict(color="black", size=8),
        name="Скважины"
    ))

    # Настройки макета
    fig.update_layout(
        title="Диаграмма Вороного с учётом границ залежи",
        width=800,
        height=800,
        hovermode="closest",
        legend=dict(
            x=1.15,  # Сдвиг вправо
            xanchor='left',  # Якорь по горизонтали ('left', 'center', 'right')
            yanchor='top'  # Якорь по вертикали ('top', 'middle', 'bottom')
        )
    )

    return fig


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--border', type=str, help="Файл с границами (border.txt)", default=None)
    parser.add_argument('--wells', type=str, help="Файл с координатами скважин (wells.txt)", default=None)
    args = parser.parse_args()

    if args.border:
        PATH_TO_BORDER = args.border
    else:
        PATH_TO_BORDER = 'border.txt'

    if args.wells:
        PATH_TO_WELLS = args.wells
    else:
        PATH_TO_WELLS = 'wells.txt'

    border, wells, values_locus = load_data(PATH_TO_BORDER, PATH_TO_WELLS)
    fig = create_voronoi_plot(border, wells, values_locus)
    fig.show()


if __name__ == "__main__":
    main()
