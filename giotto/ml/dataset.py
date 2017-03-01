from random import shuffle
from pandas import Series
from pandas import DataFrame
from sklearn import preprocessing
from pprint import pprint
from giotto.ml.tsfresh_features import TsfreshFeatures
from giotto.ml.sample import Sample
import numpy as np


class Dataset:
    def __init__(self, samples=[]):
        self.samples = samples

    def generate_sliding_windows(self, length=10):
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

    def to_tsfresh_features(self, use_features=[]):
        timeseries, used_features = TsfreshFeatures(dataset=self).extract(use_features)

        new_samples = []
        for i, sample in enumerate(self.samples):
            new_samples.append(Sample(timeseries=timeseries[i],
                                      label=sample.label))

        return Dataset(samples=new_samples), used_features

    def shuffle(self):
        shuffle(self.samples)

    def indexed_labels(self, labels):
        y = []

        for sample in self.samples:
            y.append(labels.index(sample.label))
        return np.array(y, dtype=np.int32)

    def num_series_per_timeseries(self):
        return len(self.timeseries()[0].sets_of_values)

    def length_per_timeseries(self):
        return self.timeseries()[0].length()

    def transpose_samples(self):
        x = []

        for sample in self.samples:
            sets_of_values = sample.timeseries.sets_of_values
            transposed = np.array(sets_of_values, dtype=np.float32).transpose()
            x.append(transposed)

        return np.array(x, dtype=np.float32)

    def to_x_data_frame(self):
        keys = range(self.num_series_per_timeseries())
        d = {'id': []}
        for key in keys:
            d[str(key)] = []

        for i, timeseries in enumerate(self.timeseries()):
            for _ in range(timeseries.length()):
                d['id'].append(i)

            for n, value_set in enumerate(timeseries.sets_of_values):
                d[str(n)] += value_set

        return DataFrame(data=d)

    def to_y_series(self, labels=None):
        if labels is None:
            labels = self.labels()
        y = self.indexed_labels(labels)
        return Series(y)
