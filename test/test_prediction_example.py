from giotto.ml.classifier.random_forest import MLRandomForest

def test_prediction():
    random_forest = MLRandomForest()

    random_forest.train({
        'data': [
            {
                'timeseries': [
                    [ 1.2, 3.0 ],
                    [ 2.4, 5.1 ]
                ],
                'label': 'A'
            },
            {
                'timeseries': [
                    [ 300, 430 ],
                    [ 123, 100 ]
                ],
                'label': 'B'
            },
        ],
        'labels': [ 'A', 'B' ],
        'sampling_period': 1
    })

    label = random_forest.predict([
        [ 312, 400 ],
        [ 120, 101 ]
    ])

    assert label == 'B'
