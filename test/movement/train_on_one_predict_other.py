from giotto.ml.random_forest import RandomForest
from test.movement.create_dataset import create_dataset
from sklearn.metrics import accuracy_score
from pprint import pprint
from random import shuffle
import json
from itertools import islice

training = create_dataset('data-0.json').generate_sliding_windows()
testing = create_dataset('data-feet-1.json').generate_sliding_windows()

def run():
    random_forest = RandomForest()

    training.shuffle
    testing.shuffle

    random_forest.train(training)

    computed_labels = []
    actual_labels = []
    for test in testing.samples:
        label = random_forest.predict(test.timeseries)
        computed_labels.append(label)
        actual_labels.append(test.label)

    return accuracy_score(actual_labels, computed_labels)

results = []
for i in range(50):
    accuracy = run()
    print accuracy
    results.append(accuracy);

print reduce(lambda x, y: x + y, results) / len(results)
