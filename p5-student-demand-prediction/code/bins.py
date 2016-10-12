import numpy as np

class Bins():
    def __init__(self, schedule=None, num_bins=6):
        # probably would be more efficient if we just calculate the bins once?
        self._schedule = schedule
        self._num_bins = num_bins
        self._start_times_per_bin = schedule.NUM_START_TIMES / self._num_bins

    def sum(self):
        return self._schedule.sum()

    def num_bins(self):
        return self._num_bins

    def __getitem__(self, index):
        start_index = index * self._start_times_per_bin
        end_index = (index + 1) * self._start_times_per_bin - 1

        return self._schedule.ix(start_index, end_index).sum().sum()

    def bins(self):
        array = []

        for i in range(0,self._num_bins):
            array.append(self[i])

        return np.array(array)

