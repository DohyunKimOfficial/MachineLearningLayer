import json
from giotto.ml.rnn_neural_network import RNNNeuralNetwork
from giotto.ml.dataset import Dataset
from test.movement.create_dataset import create_dataset
from pprint import pprint
from random import shuffle
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import tensorflow as tf  # Version r0.10
from sklearn import metrics

import os
from itertools import islice

training = create_dataset('data-0.json').generate_sliding_windows()
testing = create_dataset('data-1.json').generate_sliding_windows()

# dataset = create_dataset('data-0.json').generate_sliding_windows()
# samples = dataset.samples
# shuffle(samples)
# split = int(round(len(samples) * 0.7))
# training = Dataset(samples[:split])
# testing = Dataset(samples[split:])

# training.shuffle()
# testing.shuffle()

classifier = RNNNeuralNetwork()
classifier.test(training, testing)
