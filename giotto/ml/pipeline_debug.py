from sklearn.base import BaseEstimator, TransformerMixin
from pprint import pprint


class PipelineDebug(BaseEstimator, TransformerMixin):
    def fit(self, X, y):
        pprint(X)
        pprint(y)
        return self

    def transform(self, X):
        pprint(X)
        return X
