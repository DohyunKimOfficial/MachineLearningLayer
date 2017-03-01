from giotto.connect_to_redis import connect_to_redis
import logging
from rq import Queue
import schedule
import time
from giotto.helper.buildingdepot_helper import BuildingDepotHelper
from giotto.pipelines.pipeline_with_simple_features import update_sensor
from giotto.pipelines.programmed_sensor import update_programmed_sensor
from giotto.pipelines.sensor_data_model import update_sensor_data_model


redis = connect_to_redis()

q = Queue(connection=redis)


def plan_updates():
    try:
        bd_helper = BuildingDepotHelper('scheduler')
        end_time = time.time() - 3  # 5 seconds ago
        sensors = bd_helper.get_all_virtual_sensors()

        for sensor in sensors:
            if sensor['programming_type'] == 'Demonstrated':
                q.enqueue(update_sensor, sensor, end_time)
            else:
                q.enqueue(update_programmed_sensor, sensor, end_time)

        print 'Scheduled ' + str(len(sensors)) + ' updates'
    except Exception as e:
        logging.error('Plan updates error %s', exc_info=e)


def update_sensor_data_models():
    bd_helper = BuildingDepotHelper('scheduler')
    sensors = bd_helper.get_all_sensors()

    for sensor in sensors:
        should_update = False
        if 'fuzzy_set_updated_at' in sensor:
            if time.time() - sensor['fuzzy_set_updated_at'] > 48 * 60:
                should_update = True
        else:
            should_update = True

        if should_update:
            q.enqueue(update_sensor_data_model, sensor)


schedule.every(3).seconds.do(plan_updates)
# schedule.every(15).minutes.do(update_sensor_data_models)

while True:
    schedule.run_pending()
    time.sleep(1)
