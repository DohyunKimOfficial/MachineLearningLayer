class Sample:
    def __init__(self, timeseries = [], label = None):
        self.timeseries = timeseries
        self.label = label

    def generate_sliding_windows(self, length = 10):
        new_timeseries = self.timeseries.generate_sliding_windows(length)
        new_samples = []
        for timeseries in new_timeseries:
            new_samples.append(Sample(timeseries=timeseries, label=self.label))

        return new_samples

    def to_features(self):
        new_timeseries = self.timeseries.to_features()
        return Sample(timeseries=new_timeseries, label=self.label)
