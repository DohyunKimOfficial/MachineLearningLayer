from giotto.ml.random_forest import RandomForest
from giotto.ml.timeseries import Timeseries
from giotto.ml.sample import Sample
from giotto.ml.dataset import Dataset
from test.movement.create_dataset import create_dataset
from pprint import pprint
from random import shuffle
import json
from itertools import islice

dataset = create_dataset('data-0.json').generate_sliding_windows()
samples = dataset.samples

def run():
    random_forest = RandomForest()

    shuffle(samples)

    split = int(round(len(samples) * 0.7))
    training = Dataset(samples[:split])
    testing = Dataset(samples[split:])

    random_forest.train(training)

    success = 0
    failed = 0
    for sample in testing.samples:
        label = random_forest.predict(sample.timeseries)
        if label == sample.label:
            success += 1
        else:
            failed += 1

    return 100 * success / (success + failed)

results = []
for i in range(50):
    results.append(run());

print reduce(lambda x, y: x + y, results) / len(results)
