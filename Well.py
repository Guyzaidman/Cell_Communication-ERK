import math
import matplotlib.pyplot as plt
import numpy as np
from Cell import Cell


class Well:
    """
    Well class consisting from:
    well_name: String, a unique identifier (optional)
    cells: list, consists of all cells in well
    """

    def __init__(self, ktr, x, y, name=""):
        """
        :param ktr: pandas.DataFrame, ktr intensities of all cells in well
        :param x: pandas.DataFrame, x coordinates of all cells in well
        :param y: pandas.DataFrame, y coordinates of all cells in well
        """
        self.well_name = name
        self.cells = []
        for a, b, c in zip(x, y, ktr):
            cell = Cell(x[a], y[b], ktr[c], cell_id=str(a))
            self.cells.append(cell)

    def plot_cells_locations(self, frame):
        """
        plotting all cells locations in specific frame
        :param frame: Integer, frame in question
        :return: None
        """
        x = [cell.x[frame] for cell in self.cells]
        y = [cell.y[frame] for cell in self.cells]
        plt.title(self.well_name)
        plt.xlabel("x")
        plt.ylabel("y")
        plt.scatter(x, y)
        plt.show()

    def get_all_correlations(self):
        """
        calculates pearson correlation between every pair of cells in well
        :return: list, all Pearson’s correlation coefficients
        """
        corr = []
        length = len(self.cells)
        for i in range(length):
            for j in range(i + 1, length):
                corr.append(self.cells[i].calc_ktr_correlation(self.cells[j])[0])

        return corr

    def plot_correlation_distribution(self, n=None):
        """
        plotting the correlation distribution of the well
        :param n: Integer, number of bars in plot
        :return: None
        """
        all_cor = self.get_all_correlations()
        all_cor = self.divide_to_n(all_cor, n=n)
        gap = 2/n
        a = -1
        ticks = []
        for i in range(n):
            ticks.append(a)
            a += gap
        # ticks = [i/n for i in range(n)]
        plt.bar(ticks, all_cor, width=2 / n)
        plt.title(self.well_name + " - correlation distribution plot")
        plt.show()

    def divide_to_n(self, cor_arr, n):
        """
        taking a list of size k with each element value within the interval [-1,1],
        returns a list of size n with each element value within the interval [0,1],
        which represents the distribution of the original elements in n "bins"
        :param cor_arr: list of real numbers between [-1,1]
        :param n: number of "bins"
        :return: numpy array of size n
        """
        res = np.zeros(shape=(n,))
        l = len(cor_arr)

        for x in cor_arr:
            index_x = math.floor(((x + 1) / 2) * n)
            res[index_x] += 1

        res = res / l

        return res
