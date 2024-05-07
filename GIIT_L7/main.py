import matplotlib.pyplot as plt
from scipy.spatial import Delaunay, Voronoi, voronoi_plot_2d
import numpy as np


def main():
    points = []
    with open("points.txt", "r") as file:
        for line in file:
            x, y = line.strip().split(" ")
            points.append([float(x), float(y)])

    points = np.array(points)

    tri = Delaunay(points)
    vor = Voronoi(points)

    plt.figure(figsize=(10, 5))

    plt.subplot(1, 2, 1)
    plt.triplot(points[:, 0], points[:, 1], tri.simplices)
    plt.plot(points[:, 0], points[:, 1], 'o')
    plt.title('Триангуляция Делоне')
    plt.xlabel('X')
    plt.ylabel('Y')

    plt.subplot(1, 2, 2)
    voronoi_plot_2d(vor)
    plt.plot(points[:, 0], points[:, 1], 'o')
    plt.title('Диаграмма Вороного')
    plt.xlabel('X')
    plt.ylabel('Y')

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
