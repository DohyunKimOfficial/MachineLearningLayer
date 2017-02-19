from giotto.ml.dataset import Dataset
from giotto.ml.sample import Sample
from giotto.ml.timeseries import Timeseries
# from pprint import pprint
from numpy import mean


class DatasetFetcher:
    def __init__(self, bd_helper):
        self.bd_helper = bd_helper

    def fetch(self, sample_defs):
        samples = []

        for sample_def in sample_defs:
            max_length = 0
            sets_of_values = []
            for uuid in sample_def['inputs']:
                data = self.bd_helper.get_timeseries_data(
                        uuid=uuid,
                        start_time=sample_def['start'],
                        end_time=sample_def['end'])

                if data is None:
                    return None

                max_length = max(max_length, len(data))
                sets_of_values.append(data)
                if len(data) == 0:
                    return None

            # normalize lengths
            sets_of_values = [[v[i] if len(v) > i else mean(v)
                for i in range(max_length)] for v in sets_of_values]

            timeseries = Timeseries(sets_of_values=sets_of_values)
            sample = Sample(timeseries=timeseries)
            if 'label' in sample_def:
                sample.label = sample_def['label']
            samples.append(sample)

        dataset = Dataset(samples=samples)
        return dataset
