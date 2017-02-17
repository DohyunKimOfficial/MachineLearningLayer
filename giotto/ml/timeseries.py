from giotto.ml.features import Features
from sklearn import preprocessing
from pprint import pprint
import numpy as np
from itertools import islice

class Timeseries:
    def __init__(self, sets_of_values = []):
        self.sets_of_values = sets_of_values

    def scale(self, scaler):
        one_d = self.to_1d()
        scaled = scaler.transform(one_d)
        self.sets_of_values = scaled.reshape(len(self.sets_of_values), -1)

    def generate_sliding_windows(self, length = 10):
        solutions = []
        for values in self.sets_of_values:
            for i, new_values in enumerate(self.__window(values, n=10)):
                if len(solutions) <= i:
                    solutions.append([])

                solutions[i].append(new_values)


        new_timeseries = []
        for solution in solutions[::2]:
            if len(solution) == len(self.sets_of_values):
                new_timeseries.append(Timeseries(sets_of_values=solution))

        return new_timeseries

    def __window(self, seq, n=10):
        "Returns a sliding window (of width n) over data from the iterable"
        "   s -> (s0,s1,...s[n-1]), (s1,s2,...,sn), ...                   "
        it = iter(seq)
        result = tuple(islice(it, 20))
        if len(result) == n:
            yield result
        for elem in it:
            result = result[1:] + (elem,)
            yield result

    def to_features(self):
        return Timeseries(Features(timeseries=self).to_features())

    def length(self):
        return max(list(map(lambda values: len(values), self.sets_of_values)))

    def to_1d(self):
        sets_of_values = self.sets_of_values
        features = np.array(sets_of_values, dtype=np.float32)

        return features.reshape(1, -1)
