from giotto.helper.buildingdepot_helper import BuildingDepotHelper
import json
import math
import time


bd_helper = BuildingDepotHelper('worker')


def create_fuzzy_set(values, min_val, max_val):
    set_size = 100
    max_val = float(max_val)
    min_val = float(min_val)
    increment_size = (max_val - min_val) / set_size

    distances = []

    for x in range(min_val, max_val, increment_size):
        sum = 0.0

        for y in values:
            distance = math.sqrt(math.pow(x - y, 2))
            exp = math.exp(-1 * math.pow(2 * distance / increment_size, 2))
            sum += exp

        distances.append(sum)

    # normalize the distances
    min_dist = min(distances)
    max_dist = max(distances)
    distances = [
      (dist - min_dist) / (max_dist - min_dist) for dist in distances
    ]

    return distances, increment_size


def update_sensor_data_model(sensor):
    print 'Updating data model of ' + sensor['id']

    end_time = time.time() - 2  # 2 seconds ago
    start_time = end_time - 24 * 60  # 1 day ago

    data = bd_helper.get_timeseries_data(
            uuid=sensor['id'],
            start_time=start_time,
            end_time=end_time)

    if data and len(data):
        min_value, max_value = sensor_min_and_max(sensor)
        if min_value and max_value:
            fuzzy_set, increment_size = create_fuzzy_set(data, min_value,
                                                         max_value)

            bd_helper.post_sensor_tags(sensor['id'], [
                {
                    'name': 'FuzzySet',
                    'value': json.dumps(fuzzy_set)
                },
                {
                    'name': 'FuzzySetUpdatedAt',
                    'value': end_time
                },
                {
                    'name': 'IncrementSize',
                    'value': increment_size
                },
                {
                    'name': 'MinValue',
                    'value': min_value
                },
                {
                    'name': 'MaxValue',
                    'value': max_value
                },
            ])


def sensor_min_and_max(sensor):
    if 'min' in sensor and 'max' in sensor:
        return sensor['min'], sensor['max']

    ss_mins_and_maxs = {
        0: {'min': 0, 'max': 0},  # Accelerometer
        1: {'min': -15000000, 'max': 15000000},  # Microphone
        2: {'min': -15000000, 'max': 15000000},  # EMI
        3: {'min': 0, 'max': 100},  # Geophone - don't know, no data in BD
        4: {'min': 0, 'max': 150},  # Temperature
        5: {'min': 900, 'max': 1000},  # Barometer
        6: {'min': 0, 'max': 50},  # Humidity
        7: {'min': 0, 'max': 100},  # Illumination
        8: {'min': 0, 'max': 200},  # Color
        9: {'min': -100, 'max': 0},  # Magnetometer
        10: {'min': -100, 'max': 100},  # WiFi
        11: {'min': 0, 'max': 4000},  # Motion
        12: {'min': 0, 'max': 300},  # Geye
    }
    if 'ss_sensor_id' in sensor:
        ss_sensor_id = sensor['ss_sensor_id']
        return ss_mins_and_maxs[ss_sensor_id]['min'], ss_mins_and_maxs[ss_mins_and_maxs]['max']
