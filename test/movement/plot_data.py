import numpy as np
from test.movement.create_dataset import create_dataset
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from pprint import pprint

colors = ['b', 'c', 'y', 'm', 'r']
show_labels = ['standing', 'sitting']

for k, name in enumerate(['data-0.json', 'data-feet-0.json']):
    dataset = create_dataset(name).generate_sliding_windows()

    dataset = dataset.to_features()
    dataset.shuffle()

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

            sets_of_values = sample.timeseries.sets_of_values
            for i, value_set in enumerate(sets_of_values):
                for n, value in enumerate(value_set):
                    activity_data[l]['x'].append(value)
                    activity_data[l]['y'].append(i)
                    activity_data[l]['z'].append(n)


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
