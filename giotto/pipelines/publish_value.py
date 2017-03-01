import json
from giotto.connect_to_redis import connect_to_redis


def publish_value(bd_helper, uuid, bd_value, value, time):
    bd_helper.post_sensor_value(uuid, bd_value, time)

    redis = connect_to_redis()
    redis.publish(uuid, json.dumps({
        'uuid': uuid, 'value': bd_value
    }))

    print(uuid + ' = ' + value)
