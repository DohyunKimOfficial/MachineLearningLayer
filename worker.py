from giotto.connect_to_redis import connect_to_redis
from rq import Worker

redis = connect_to_redis()
QUEUES = ['high', 'normal', 'low']

print('Starting a worker')

worker = Worker(QUEUES, connection=redis)
worker.work(logging_level='WARNING')
