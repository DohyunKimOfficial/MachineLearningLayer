import json
from sklearn.metrics import accuracy_score
from giotto.ml.random_forest import RandomForest
from giotto.ml.rnn_neural_network import RNNNeuralNetwork
from giotto.ml.dataset import Dataset
from giotto.ml.cross_domain_feature_selection import CrossDomainFeatureSelection
from test.movement.create_dataset import create_dataset
from pprint import pprint
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

training = create_dataset('data-0.json').generate_sliding_windows()
testing = create_dataset('data-1.json').generate_sliding_windows()
selection = CrossDomainFeatureSelection()
training, testing = selection.fit(training, testing)

testing_other = create_dataset('data-1.json').generate_sliding_windows()
testing_other.samples = [testing_other.samples[0]]
testing_other = selection.transform(testing_other)

pprint(testing.samples[0].timeseries.sets_of_values)
pprint(testing_other.samples[0].timeseries.sets_of_values)

scaler = training.scaler()
training.scale(scaler)
testing.scale(scaler)

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
