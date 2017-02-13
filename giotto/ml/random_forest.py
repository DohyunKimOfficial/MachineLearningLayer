'''Randome Forest Classifer Module'''

from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import cross_val_score
from sklearn import preprocessing
from sklearn import feature_selection
from pprint import pprint

import numpy as np


class RandomForest:
    '''Random Forest classifier class

    This class train a Random Forest classifier using a dataset passed to the
    train function. Then, it makes a prediction using timeseries data given to
    the "predict" function.
    If you want to implement a classifier class using other models, replicate
    this class. The class have to implement two functions at least, train and predict.
    '''
    def __init__(self, dictionary=None, serialized=False):
        self.labels = []

        self.model = RandomForestClassifier()

    def train(self, dataset):
        '''Trains a random forest classifier'''

        dataset = dataset.to_features()

        # Prescale
        self.scaler = dataset.scaler()
        dataset.scale(self.scaler)

        # Generate a training set
        features_data = dataset.to_1d()
        labels = dataset.sample_labels()

        # Select features  Random Forest does not require feature selection
        # For other classifier uncomment the next 2 lines and do feature selection
        #self.selector =
        # feature_selection.SelectKBest(feature_selection.f_regression).fit(scaled_features, data.labels)
        #selectedFeatures = self.selector.transform(scaled_features)

        # Train a classifier
        self.classifier = self.model.fit(features_data, labels)
        # self.sampling_period = data['sampling_period']
        self.labels = dataset.labels()

    def predict(self, timeseries):
        '''Makes a prediction using a pre-trained random forest classifier'''

        features = timeseries.to_features()
        features.scale(self.scaler)
        features_values = features.to_1d()

        # Feture selection
        #selectedFeatures = selector.transform(scaled_features)

        # Prediction
        predictions = self.classifier.predict(features_values)

        return predictions[0]
