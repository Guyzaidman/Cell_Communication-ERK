from State import State
import matplotlib.pyplot as plt


class Cell:
    def __init__(self, col_x, col_y, col_ktr, cell_id):
        self.id = cell_id

        self.states = []
        for i, x, y, k in zip(range(len(col_x)), col_x, col_y, col_ktr):
            s = State(frame=i, x=x, y=y, ktr_intensity=k)
            self.states.append(s)
        self.states.sort(key=lambda e: e.frame)

        self.number_of_frames = len(self.states)
        self.min_ktr_intensity = (min(self.states, key=lambda x: x.ktr_intensity)).ktr_intensity
        self.max_ktr_intensity = (max(self.states, key=lambda x: x.ktr_intensity)).ktr_intensity

    def __len__(self):
        return len(self.states)

    def __getitem__(self, item):
        if item > self.max_frame():
            raise IndexError("list index out of range: " + str(self.max_frame()))
        return self.states[item]

    def min_frame(self):
        return self.states[0].frame

    def max_frame(self):
        return self.states[len(self.states) - 1].frame

    def plot_ktr_intensity_time_series(self):
        x = []
        y = []
        for state in self.states:
            y.append(state.ktr_intensity)
            x.append(state.frame)

        plt.title("cell " + str(self.id))
        plt.plot(x, y)
        plt.show()

    # def plot_h2b_intensity_time_series(self):
    #     x = []
    #     y = []
    #     for state in self.states:
    #         y.append(state.h2b_intensity)
    #         x.append(state.frame)
    #
    #     plt.title("cell " + str(self.states[0].track))
    #     plt.plot(x, y)
    #     plt.show()

    def cell_position_in_frame_i(self, i):
        for state in self.states:
            if state.frame is i:
                return state.x, state.y

        raise Exception("frame is not found for cell " + str(self.id))
