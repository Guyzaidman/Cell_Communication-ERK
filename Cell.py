import matplotlib.pyplot as plt
from scipy.stats import pearsonr


class Cell:
    """
    Cell class consisting of:
    id: String, a unique identifier (optional)
    x: pandas.Series of the x coordinates of the cell
    y: pandas.Series of the y coordinates of the cell
    ktr: pandas.Series of the erk-ktr levels of the cell
    """
    def __init__(self, col_x, col_y, col_ktr, cell_id=''):
        self.id = cell_id
        if len(col_x) != len(col_y) != len(col_ktr):
            raise ValueError("x, y and ktr Series should of same length")
        self.x = col_x
        self.y = col_y
        self.ktr = col_ktr

        self.number_of_frames = len(col_ktr)
        self.min_ktr_intensity = min(col_ktr)
        self.max_ktr_intensity = max(col_ktr)

    def __len__(self):
        return self.number_of_frames

    def plot_ktr(self):
        """
        plotting cell's ktr intensity time series
        :return: None
        """
        self.ktr.plot()
        plt.title("cell " + str(self.id))
        plt.show()

    def get_cell_position(self, frame):
        """
        :param frame: Integer, the position in the time series
        :return: tuple, (x,y) coordinates of the cell
        """
        return self.x[frame], self.y[frame]

    def calc_ktr_correlation(self, other):
        """
        calculates the pearson correlation of the ktr intensity
        between self cell and other cell using scipy.stats.pearsonr:
        https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.stats.pearsonr.html
        :param other: Cell,
        :return: tuple, (Pearson’s correlation coefficient, 2-tailed p-value)
        """
        return pearsonr(self.ktr, other.ktr)
