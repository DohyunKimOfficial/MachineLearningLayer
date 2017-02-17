from pandas import DataFrame
from pprint import pprint
from pandas import Series
from tsfresh.feature_extraction import extract_features, \
    MinimalFeatureExtractionSettings, \
    ReasonableFeatureExtractionSettings
from tsfresh import select_features
from tsfresh.utilities.dataframe_functions import impute
from tsfresh.transformers.feature_augmenter import FeatureAugmenter
from tsfresh.transformers.feature_selector import FeatureSelector

from giotto.ml.timeseries import Timeseries

import logging
logging.basicConfig()

class TsfreshFeatures:
    def __init__(self, dataset):
        self.dataset = dataset
        self.labels = dataset.labels()

    def extract(self, use_features=[]):
        x = self.__x_data_frame()
        y = self.__y_series()

        settings = ReasonableFeatureExtractionSettings()
        extracted_features = extract_features(x, column_id='id', \
                feature_extraction_settings=settings)
        if len(use_features) == 0:
            impute(extracted_features)
            features_filtered = select_features(extracted_features, y)
            use_features = features_filtered.keys()
        else:
            features_filtered = extracted_features[use_features]

        keys = features_filtered.keys()
        timeseries = []
        for index, row in features_filtered.iterrows():
            values = []
            for key in keys:
                if key == 'id':
                    continue

                value = row[key]
                values.append(value)

            timeseries.append(Timeseries([values]))

        return timeseries, use_features

    def __x_data_frame(self):
        dataset = self.dataset
        keys = range(dataset.num_series_per_timeseries())
        d = { 'id': [] }
        for key in keys:
            d[str(key)] = []

        for i, timeseries in enumerate(dataset.timeseries()):
            for _ in range(timeseries.length()):
                d['id'].append(i)

            for n, value_set in enumerate(timeseries.sets_of_values):
                d[str(n)] += value_set

        return DataFrame(data=d)

    def __y_series(self):
        y = self.dataset.indexed_labels(self.labels)
        return Series(y)
