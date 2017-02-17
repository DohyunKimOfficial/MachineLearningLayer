# -*- coding: utf-8 -*-
# This file as well as the whole tsfresh package are licenced under the MIT licence (see the LICENCE.txt)
# Maximilian Christ (maximilianchrist.com), Blue Yonder Gmbh, 2016

import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from functools import partial
from tsfresh.feature_extraction.settings import FeatureExtractionSettings
from tsfresh.transformers.feature_augmenter import FeatureAugmenter
from tsfresh.transformers.feature_selector import FeatureSelector
from tsfresh.utilities.dataframe_functions import impute, get_range_values_per_column, impute_dataframe_range


# TODO: Add more testcases
# TODO: Do we want to keep the flag `evaluate_only_added_features`?
# Pro: It offers more control
# Contra: The Transformer is more than an Augmenter
class RelevantFeatureAugmenter(BaseEstimator, TransformerMixin):

    def __init__(self,
                 evaluate_only_added_features=True,
                 feature_selection_settings=None,
                 feature_extraction_settings=None,
                 column_id=None, column_sort=None, column_kind=None, column_value=None,
                 timeseries_container=None):


        # We require to have IMPUTE!
        if feature_extraction_settings is None:
            feature_extraction_settings = FeatureExtractionSettings()
            # Range will be our default imputation strategy
            feature_extraction_settings.IMPUTE = impute

        self.feature_extractor = FeatureAugmenter(feature_extraction_settings,
                                                  column_id, column_sort, column_kind, column_value)
        self.feature_selector = FeatureSelector(feature_selection_settings)

        self.evaluate_only_added_features = evaluate_only_added_features
        self.timeseries_container = timeseries_container

    def set_timeseries_container(self, timeseries_container):
        self.timeseries_container = timeseries_container

    def fit(self, X, y):
        if self.timeseries_container is None:
            raise RuntimeError("You have to provide a time series using the set_timeseries_container function before.")

        self.feature_extractor.set_timeseries_container(self.timeseries_container)

        if self.evaluate_only_added_features:
            # Do not merge the time series features to the old features
            X_tmp = pd.DataFrame(index=X.index)
        else:
            X_tmp = X
        X_augmented = self.feature_extractor.transform(X_tmp)

        if self.feature_extractor.settings.IMPUTE is impute:
            col_to_max, col_to_min, col_to_median = get_range_values_per_column(X_augmented)
            self.feature_extractor.settings.IMPUTE = partial(impute_dataframe_range, col_to_max=col_to_max,
                                                             col_to_min=col_to_min, col_to_median=col_to_median)

        self.feature_selector.fit(X_augmented, y)

        return self

    def transform(self, X):
        if self.feature_selector.relevant_features is None:
            raise RuntimeError("You have to call fit before.")

        if self.timeseries_container is None:
            raise RuntimeError("You have to provide a time series using the set_timeseries_container function before.")

        self.feature_extractor.set_timeseries_container(self.timeseries_container)

        relevant_time_series_features = set(self.feature_selector.relevant_features) - set(pd.DataFrame(X).columns)

        relevant_extraction_settings = FeatureExtractionSettings.from_columns(relevant_time_series_features)
        relevant_extraction_settings.set_default = False
        relevant_extraction_settings.IMPUTE = self.feature_extractor.settings.IMPUTE
        relevant_feature_extractor = FeatureAugmenter(settings=relevant_extraction_settings,
                                                      column_id=self.feature_extractor.column_id,
                                                      column_sort=self.feature_extractor.column_sort,
                                                      column_kind=self.feature_extractor.column_kind,
                                                      column_value=self.feature_extractor.column_value)

        relevant_feature_extractor.set_timeseries_container(self.feature_extractor.timeseries_container)

        X_augmented = relevant_feature_extractor.transform(X)

        # return X_augmented.copy().loc[:, self.feature_selector.relevant_features]
        return X_augmented
