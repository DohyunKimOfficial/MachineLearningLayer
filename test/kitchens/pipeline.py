import pandas as pd
from giotto.ml.dataset import Dataset
from test.kitchens.create_dataset import create_dataset
# from giotto.ml.cross_domain_feature_selection import \
#         CrossDomainFeatureSelection
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.preprocessing import StandardScaler

from tsfresh.feature_extraction import ReasonableFeatureExtractionSettings
from tsfresh.transformers import RelevantFeatureAugmenter

dataset = create_dataset('tag1_input.json')
dataset.generate_sliding_windows(length=50)
dataset.shuffle()
split = int(round(len(dataset.samples) * 0.7))
training = Dataset(dataset.samples[:split])
testing = Dataset(dataset.samples[split:])

df_train = training.to_x_data_frame()
y_train = training.to_y_series()

df_test = testing.to_x_data_frame()
y_test = testing.to_y_series()

X_train = pd.DataFrame(index=y_train.index)
X_test = pd.DataFrame(index=y_test.index)

settings = ReasonableFeatureExtractionSettings()
ppl = Pipeline([
    ('fresh', RelevantFeatureAugmenter(column_id='id')),
    ('standardscaler', StandardScaler(with_mean=True, with_std=True)),
    ('clf', RandomForestClassifier())
])

ppl.set_params(fresh__timeseries_container=df_train)

ppl.set_params(fresh__timeseries_container=df_test)
y_pred = ppl.predict(X_test)

print(classification_report(y_test, y_pred))
