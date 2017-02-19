from giotto.helper.buildingdepot_helper import BuildingDepotHelper
from giotto.helper.sensor_helper import average_sample_length
from sklearn.feature_selection import VarianceThreshold
from giotto.ml.pipeline_debug import PipelineDebug
from sklearn.preprocessing import Imputer
from giotto.helper.dataset_fetcher import DatasetFetcher
from sklearn.pipeline import Pipeline
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from tsfresh.transformers import FeatureAugmenter
import pandas as pd
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
        ('fresh',
            FeatureAugmenter(column_id='id')),
        ('impute',
            Imputer(missing_values='NaN', strategy='mean', axis=0)),
        # ('var_thresh', VarianceThreshold()),
        ('pca', PCA()),
        ('standardscaler',
            StandardScaler(with_mean=True, with_std=True)),
        # ('debug', PipelineDebug()),
        ('clf',
            RandomForestClassifier())
    ])

    df_train = training.to_x_data_frame()
    y_train = training.to_y_series(labels)
    X_train = pd.DataFrame(index=y_train.index)

    pipeline.set_params(fresh__timeseries_container=df_train)
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

    df = dataset.to_x_data_frame()
    X = pd.DataFrame(index=[0])

    pipeline.set_params(fresh__timeseries_container=df)
    pred = pipeline.predict(X)
    bd_helper.post_sensor_value(sensor['id'], pred[0])
    value = sensor['labels'][pred[0]]

    print(sensor['name'] + ' = ' + value)
