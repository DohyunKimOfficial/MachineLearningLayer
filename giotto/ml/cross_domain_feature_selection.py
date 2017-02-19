from tsfresh.feature_extraction.settings import FeatureExtractionSettings
from tsfresh.utilities.dataframe_functions import restrict_input_to_index
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from pprint import pprint
from tsfresh.feature_extraction import extract_features
from tsfresh import select_features
from tsfresh.utilities.dataframe_functions import impute
from scipy import stats

from giotto.ml.relevant_feature_augmenter import RelevantFeatureAugmenter


class CrossDomainFeatureSelection(BaseEstimator, TransformerMixin):
    def __init__(self, column_id, source_df, target_df):
        self.column_id = column_id
        self.augmenter = RelevantFeatureAugmenter(column_id=column_id)
        self.source_df = source_df
        self.target_df = target_df

    def fit(self, X, y):
        settings = FeatureExtractionSettings()
        settings.show_warnings = False

        source_extracted = extract_features(
                self.source_df,
                column_id=self.column_id,
                feature_extraction_settings=settings)
        impute(source_extracted)
        source_features_filtered = select_features(source_extracted, y)
        source_features = source_features_filtered.keys()

        settings = FeatureExtractionSettings.from_columns(source_features)
        settings.show_warnings = False

        target_extracted = extract_features(
                self.target_df,
                column_id=self.column_id,
                feature_extraction_settings=settings)

        feature_pvalues = []
        for feature in source_features:
            source = source_extracted[feature].tolist()
            target = target_extracted[feature].tolist()

            feature_pvalues.append([
                feature,
                stats.ttest_ind(source, target).pvalue
            ])

        feature_pvalues = [c for c in feature_pvalues if c[1] > 0.05]
        common_features = list(map(lambda c: c[0], feature_pvalues))
        self.common_features = common_features

        pprint('Using ' + str(len(self.common_features)) + ' features.')

        return self

    def transform(self, X):
        df = restrict_input_to_index(self.target_df, self.column_id, X.index)

        settings = FeatureExtractionSettings.from_columns(self.common_features)
        settings.show_warnings = False
        target_extracted = extract_features(
                df,
                column_id=self.column_id,
                feature_extraction_settings=settings)[self.common_features]
        X_augmented = pd.merge(
                X, target_extracted,
                left_index=True, right_index=True, how="left")

        return X_augmented

    def set_source_df(self, source_df):
        self.source_df = source_df

    def set_target_df(self, target_df):
        self.target_df = target_df
