import argparse
import sys
from os.path import dirname, abspath

sys.path.insert(0, dirname(abspath(__file__)))

from parse_info import load_data
from plot_2d import plot_voronoi_2d
from plot_3d import plot_voronoi_3d


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--border', type=str, help="Файл с границами (border.txt)", default=None)
    parser.add_argument('--wells', type=str, help="Файл с координатами скважин (wells.txt)", default=None)
    parser.add_argument('--graph', type=str, help="Выбор графики (2d или 3d)", default='2d')
    args = parser.parse_args()

    if args.border:
        PATH_TO_BORDER = args.border
    else:
        PATH_TO_BORDER = 'border.txt'

    if args.wells:
        PATH_TO_WELLS = args.wells
    else:
        PATH_TO_WELLS = 'wells.txt'

    # Импорт данный
    border, wells, values_locus = load_data(PATH_TO_BORDER, PATH_TO_WELLS)

    # Создание диаграммы
    if args.graph == '2d':
        fig = plot_voronoi_2d(border, wells, values_locus)
    else:
        fig = plot_voronoi_3d(border, wells, values_locus)
    fig.show()


if __name__ == "__main__":
    main()
