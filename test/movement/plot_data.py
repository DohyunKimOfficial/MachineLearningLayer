import numpy as np
from test.movement.create_dataset import create_dataset
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from tsfresh.feature_extraction import MinimalFeatureExtractionSettings, \
    ReasonableFeatureExtractionSettings
from tsfresh.transformers import RelevantFeatureAugmenter
from tsfresh.feature_extraction import extract_features
from tsfresh import select_features
from tsfresh.utilities.dataframe_functions import impute
from pprint import pprint

colors = ['b', 'c', 'y', 'm', 'r'] * 100
show_labels = ['sitting', 'walking']

datasets = ['data-0.json', 'data-1.json']

scaler = None

feature_keys = []
for k, name in enumerate(datasets):
    dataset = create_dataset(name).generate_sliding_windows()

    dataset, feature_keys = dataset.to_tsfresh_features(feature_keys)
    # dataset.shuffle()
    if scaler == None:
        scaler = dataset.scaler()
    dataset.scale(scaler)

    labels = dataset.labels()

    activity_data = {}
    for label in show_labels:
        activity_data[label] = {
            'x': [],
            'y': [],
            'z': []
        }


    for sample in dataset.samples[::5]:
        if sample.label in show_labels:
            l = sample.label

            features = sample.timeseries.to_1d()[0]
            sets_of_values = sample.timeseries.sets_of_values
            for i, value in enumerate(features):
                activity_data[l]['x'].append(value)
                activity_data[l]['y'].append(i)


    # fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')
    # ax.scatter(x, y, z, c=colors, alpha=0.5)

    plt.figure(k + 1)
    plt.title('Plot ' + name)

    scatters = []
    for i, label in enumerate(show_labels):

        scatters.append(plt.scatter(activity_data[label]['x'],
        activity_data[label]['y'],
        color=colors[i], alpha=0.5))

    plt.legend(scatters,
            show_labels,
            scatterpoints=1,
            loc='lower left',
            ncol=3,
            fontsize=8)


plt.show()
