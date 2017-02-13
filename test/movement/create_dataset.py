from giotto.ml.timeseries import Timeseries
from giotto.ml.sample import Sample
from giotto.ml.dataset import Dataset
import json

def create_sample(item):
    solutions = []
    timeseries = Timeseries(sets_of_values=item['timeseries'])
    return Sample(timeseries=timeseries, label=item['label'])

def create_dataset(file_name):
    with open('test/movement/' + file_name) as data_file:
        data = json.load(data_file)

    samples = list(map(create_sample, data))
    return Dataset(samples)
