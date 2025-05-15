import argparse
from geovoronoi import voronoi_regions_from_coords
import numpy as np
from shapely.geometry import Polygon
import plotly.graph_objects as go
from typing import Tuple
import plotly.io as pio
import os


def load_data(PATH_TO_BORDER: str, PATH_TO_WELLS: str) -> Tuple[Polygon, np.array]:
    """Функция загрузки данных: границы и координаты скважин.
    :arg
    :param PATH_TO_WELLS: путь к данным скважин
    :param PATH_TO_BORDER: путь к данным контура
    :return Tuple - кортеж из полигона и данные о скважинах в формате np.array
    """
    border_data = np.loadtxt(PATH_TO_BORDER)[:, :2]
    wells_data = np.loadtxt(PATH_TO_WELLS, skiprows=5)[:, :2]
    return Polygon(border_data), wells_data


def create_voronoi_plot(border: Polygon, wells: np.array) -> go.Figure:
    """Функция создания диаграммы Вороного.
    :arg
    :param border: граница контура
    :param wells: данные по скважинам
    :return go.Figure -  график, но не показывает его
    """
    region_polys, _ = voronoi_regions_from_coords(wells, border)

    fig = go.Figure()

    for poly in region_polys.values():
        x, y = poly.exterior.xy
        fig.add_trace(go.Scatter(
            x=list(x), y=list(y),
            fill="toself",
            fillcolor="rgba(0,100,80,0.2)",
            line=dict(color="blue", width=2),
            hoverinfo="skip",
            showlegend=False
        ))

    # Скважины
    fig.add_trace(go.Scatter(
        x=wells[:, 0], y=wells[:, 1],
        mode="markers",
        marker=dict(color="red", size=8),
        name="Скважины"
    ))

    # Настройки макета
    fig.update_layout(
        title="Диаграмма Вороного с учётом границ залежи",
        width=800,
        height=800,
        hovermode="closest"
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

    border, wells = load_data(PATH_TO_BORDER, PATH_TO_WELLS)
    fig = create_voronoi_plot(border, wells)
    fig.show()


if __name__ == "__main__":
    main()
