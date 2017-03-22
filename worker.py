from giotto.connect_to_redis import connect_to_redis
from rq import Worker

redis = connect_to_redis()

print('Starting a worker')

worker = Worker('default', connection=redis)
worker.work(logging_level='WARNING')
