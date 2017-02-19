import pandas as pd
from test.movement.create_dataset import create_dataset
from giotto.ml.cross_domain_feature_selection import \
        CrossDomainFeatureSelection
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.preprocessing import StandardScaler


from tempfile import mkdtemp
from joblib import Memory

cachedir = mkdtemp()

memory = Memory(cachedir=cachedir, verbose=0)


@memory.cache
def get_pipeline(args):
    print 'Recreating the pipeline'

    training = create_dataset(args['training']).generate_sliding_windows()
    testing = create_dataset(args['testing']).generate_sliding_windows()

    df_train = training.to_x_data_frame()
    y_train = training.to_y_series()

    df_test = testing.to_x_data_frame()
    y_test = testing.to_y_series()

    X_train = pd.DataFrame(index=y_train.index)
    X_test = pd.DataFrame(index=y_test.index)

    ppl = Pipeline([
        ('crossfeature', CrossDomainFeatureSelection(column_id='id',
                                                     source_df=df_train,
                                                     target_df=df_test)),
        # ('fresh', RelevantFeatureAugmenter(column_id='id')),
        ('standardscaler', StandardScaler(with_mean=True, with_std=True)),
        ('clf', RandomForestClassifier())
    ])

    # ppl.set_params(fresh__timeseries_container=df_train)
    ppl.fit(X_train, y_train)
    return ppl, X_test, y_test


for i in range(2):
    print 'Try #' + str(i)
    ppl, X_test, y_test = get_pipeline({
        'training': 'data-0.json',
        'testing': 'data-1.json'
    })

    # ppl.set_params(fresh__timeseries_container=df_test)
    y_pred = ppl.predict(X_test)

    print(classification_report(y_test, y_pred))
