from redis import Redis
from rq import Queue
import schedule
import time
from giotto.helper.buildingdepot_helper import BuildingDepotHelper
from giotto.pipelines.pipeline_with_simple_features import update_sensor


bd_helper = BuildingDepotHelper('scheduler')
q = Queue(connection=Redis())


def plan_updates():
    end_time = time.time() - 5  # 5 seconds ago
    sensors = bd_helper.get_all_sensors()

    for sensor in sensors:
        q.enqueue(update_sensor, sensor, end_time)

    print 'Scheduled ' + str(len(sensors)) + ' updates'


schedule.every(10).seconds.do(plan_updates)

while True:
    schedule.run_pending()
    time.sleep(1)
