from random import shuffle
from sklearn import preprocessing
from pprint import pprint
import numpy as np

class Dataset:
    def __init__(self, samples=[]):
        self.samples = samples

    def generate_sliding_windows(self, length = 10):
        new_samples = []
        for sample in self.samples:
            new_samples += sample.generate_sliding_windows(length)

        return Dataset(new_samples)

    def scaler(self):
        data = self.to_1d()
        scaler = preprocessing.StandardScaler().fit(data)

        return scaler

    def scale(self, scaler):
        for timeseries in self.timeseries():
            timeseries.scale(scaler)

    def to_1d(self):
        one_d = list(map(lambda ts: ts.to_1d()[0], self.timeseries()))
        return np.array(one_d, dtype=np.float32)

    def timeseries(self):
        return list(map(lambda sample: sample.timeseries, self.samples))

    def labels(self):
        labels = list(map(lambda sample: sample.label, self.samples))
        return list(set(labels))

    def sample_labels(self):
        return list(map(lambda sample: sample.label, self.samples))

    def to_features(self):
        new_samples = list(map(lambda sample: sample.to_features(), self.samples))
        return Dataset(samples=new_samples)

    def shuffle(self):
        shuffle(self.samples)

    def indexed_labels(self, labels):
        y = []

        for sample in self.samples:
            y.append(labels.index(sample.label))
        return np.array(y, dtype=np.int32)

    def transpose_samples(self):
        x = []

        for sample in self.samples:
            example_x = []

            num_values = 0
            sets_of_values = sample.timeseries.sets_of_values
            transposed = np.array(sets_of_values, dtype=np.float32).transpose()
            x.append(transposed)

        return np.array(x, dtype=np.float32)
