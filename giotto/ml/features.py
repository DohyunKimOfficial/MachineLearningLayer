import numpy as np


def exponential(x, a, b, c):
    return a * np.exp(-b * x) + c


def linear(x, a, b):
    return a * x + b


def quadratic(x, a, b, c):
    return a * x * x + b * x + c


class Features:
    def __init__(self, timeseries):
        self.timeseries = timeseries

    def label(self):
        return self.sample.label

    def to_features(self):
        sets_of_values = self.timeseries.sets_of_values
        sets_of_features = []

        for val_set in sets_of_values:

            vals = np.array(val_set).astype('float')
            features = []
            # average
            features.append(np.average(vals))

            # std
            features.append(np.std(vals))

            # peak count
            features.append(self.peak_count(vals))

            # median
            features.append(np.median(vals))

            # min
            min = np.min(vals)
            features.append(min)

            # max
            max = np.max(vals)
            features.append(max)

            # zero crossing
            features.append(self.zero_crossing(vals))

            # max - min
            features.append(max - min)
            # features[col,7] = features[col-1,5] - features[col-1,4]

            # xdata = np.array(range(len(vals)))
            # ydata = vals

            # try:
            #     popt_linear, pcov_linear = curve_fit(linear, xdata, ydata)
            #     features[col,8], features[col,9] = popt_linear
            # except RuntimeError as exc:
            #     features[col,8], features[col,9] = [0, 0]

            # try:
            #     popt_quadratic, pcov_quadratic = curve_fit(quadratic, xdata, ydata)
            #     features[col,10], features[col,11], features[col,12] = popt_quadratic
            # except RuntimeError as exc:
            #     features[col,10], features[col,11], features[col,12] = [0, 0, 0]
            #
            # try:
            #     popt_exponential, pcov_exponential = curve_fit(exponential, xdata, ydata)
            #     features[col,13], features[col,14], features[col,15] = popt_quadratic
            # except RuntimeError as exc:
            #     features[col,13], features[col,14], features[col,15] = [0, 0, 0]

            sets_of_features.append(features)

        return sets_of_features

    def zero_crossing(self, data):
        '''Counts the number of zero-crossing in given timesries data'''
        count = 0
        for idx in range(len(data)-1):
            if data[idx]*data[idx+1] < 0:
                count = count + 1

        return count

    def peak_count(self, data):
        '''Counts the number of peaks in given timesries data'''
        count = 0
        std = np.std(data)
        for idx in range(len(data)-2):
            if data[idx+1] > std*2 and (data[idx+1] - data[idx]) * (data[idx+2] - data[idx+1]) < 0:
                count = count + 1

        return count
