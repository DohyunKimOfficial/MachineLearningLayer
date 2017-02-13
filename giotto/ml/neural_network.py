import tensorflow as tf
from pprint import pprint
from sklearn import preprocessing
import numpy as np

class NeuralNetwork:
    def test(self, training_dataset, testing_dataset):
        training_dataset = training_dataset.to_features()

        self.scaler = training_dataset.scaler()
        training_dataset.scale(self.scaler)

        features_data = training_dataset.to_1d()
        labels = training_dataset.labels()

        # Specify that all features have real-value data
        feature_columns = [tf.contrib.layers.real_valued_column("", dimension=8)]

        # Build 3 layer DNN with 10, 20, 10 units respectively.
        classifier = tf.contrib.learn.DNNClassifier(feature_columns=feature_columns,
                hidden_units=[10, 20, 10],
                n_classes=len(labels))

        # Fit model.
        classifier.fit(x=features_data,
                y=training_dataset.indexed_labels(labels),
                steps=2000)

        testing_dataset = testing_dataset.to_features()
        testing_dataset.scale(self.scaler)

        testing_features_data = testing_dataset.to_1d()

        # Evaluate accuracy.
        accuracy_score = classifier.evaluate(x=testing_features_data,
                y=testing_dataset.indexed_labels(labels))["accuracy"]
        print('Accuracy: {0:f}'.format(accuracy_score))

    def predict(self):
        # Classify two new flower samples.
        new_samples = np.array(
                [[6.4, 3.2, 4.5, 1.5], [5.8, 3.1, 5.0, 1.7]], dtype=float)
        y = list(classifier.predict(new_samples, as_iterable=True))
        print('Predictions: {}'.format(str(y)))
