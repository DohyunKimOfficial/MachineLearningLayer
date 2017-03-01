import numpy as np


def average_sample_length(sensor):
    samples = sensor['samples']
    lengths = list(map(lambda s: float(s['end']) - float(s['start']), samples))
    return np.mean(lengths)
