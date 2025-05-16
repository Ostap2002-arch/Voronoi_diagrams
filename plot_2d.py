from plotly.colors import sample_colorscale
from geovoronoi import voronoi_regions_from_coords
import numpy as np
from shapely.geometry import Polygon
import plotly.graph_objects as go


def plot_voronoi_2d(border: Polygon, wells: np.array, values_locus: np.array) -> go.Figure:
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
    values_locus = (values_locus - values_locus.min()) / (values_locus.max() - values_locus.min())
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
            x=1.15,
            xanchor='left',
            yanchor='top'
        )
    )

    return fig
