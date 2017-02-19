from giotto.helper.buildingdepot_helper import BuildingDepotHelper
from sklearn.preprocessing import Imputer
from sklearn.preprocessing import StandardScaler
from giotto.helper.dataset_fetcher import DatasetFetcher
from giotto.helper.sensor_helper import average_sample_length
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from joblib import Memory
from pprint import pprint

cachedir = './tmp'
memory = Memory(cachedir=cachedir, verbose=0)

bd_helper = BuildingDepotHelper('worker')


@memory.cache
def create_pipeline(sensor):
    print 'Creating new pipeline for ' + sensor['name']
    samples = sensor['samples']
    labels = sensor['labels']

    training = DatasetFetcher(bd_helper).fetch(samples)
    if training is None:
        return False

    pipeline = Pipeline([
        ('impute', Imputer(missing_values='NaN', strategy='mean', axis=0)),
        ('standardscaler', StandardScaler(with_mean=True, with_std=True)),
        ('clf', RandomForestClassifier())
    ])

    X_train = training.to_features().to_1d()
    y_train = training.to_y_series(labels)
    pipeline.fit(X_train, y_train)

    return pipeline


def update_sensor(sensor, end_time):
    print 'Updating ' + sensor['name']
    pipeline = create_pipeline(sensor)
    print 'Pipeline created'

    sample_length = average_sample_length(sensor)

    start_time = end_time - sample_length

    sample = {
        'inputs': sensor['inputs'],
        'start': start_time,
        'end': end_time
    }

    dataset = DatasetFetcher(bd_helper).fetch([sample])
    if dataset is None:
        return

    X = dataset.to_features().to_1d()

    pred = pipeline.predict(X)
    bd_helper.post_sensor_value(sensor['id'], pred[0])
    value = sensor['labels'][pred[0]]

    print(sensor['name'] + ' = ' + value)
