import requests
import json
from random import randint
from giotto.config.buildingdepot_setting import BuildingDepotSetting
from time import time


class BuildingDepotHelper:
    def __init__(self, env):
        setting = BuildingDepotSetting(env)
        self.bd_rest_api = setting.get('buildingdepot_rest_api')
        self.oauth = setting.oauth()
        self.access_token = self.get_oauth_token()

    def get_oauth_token(self):
        headers = {'content-type': 'application/json'}
        url = self.bd_rest_api['server']
        url += ':81/oauth/access_token/client_id='
        url += self.oauth['id']
        url += '/client_secret='
        url += self.oauth['key']

        result = requests.get(url, headers=headers)

        if result.status_code == 200:
            dic = result.json()
            return dic['access_token']
        else:
            return ''

    def get_all_sensors(self):
        url = self._api_uri() + '/search'
        data = {
            'data': {
                'Tags': ['Type:Sensor']
            }
        }
        result = requests.post(url, headers=self._headers(),
                               data=json.dumps(data))
        if result.status_code == 200:
            info = result.json()
            sensors = []
            if 'result' in info:
                result = info['result']
                for sensor_def in result:
                    tags = sensor_def['tags']
                    names = [tag for tag in tags if tag['name'] == 'Name']
                    min_value = [tag for tag in tags if tag['name'] == 'MinValue']
                    max_value = [tag for tag in tags if tag['name'] == 'MaxValue']
                    increment_size = [tag for tag in tags if tag['name'] == 'IncrementSize']
                    fuzzy_set = [tag for tag in tags if tag['name'] == 'FuzzySet']
                    fuzzy_set_updated_at = [tag for tag in tags if tag['name'] == 'FuzzySetUpdatedAt']
                    ss_sensor_id = [tag for tag in tags if tag['name'] == 'SensorID']

                    sensor = {
                        'id': sensor_def['name']
                    }

                    if len(names):
                        sensor['name'] = names[0]['value']
                    if len(min_value):
                        sensor['min'] = float(min_value[0]['value'])
                    if len(max_value):
                        sensor['max'] = float(max_value[0]['value'])
                    if len(increment_size):
                        sensor['increment_size'] = increment_size[0]['value']
                    if len(fuzzy_set):
                        sensor['fuzzy_set'] = json.loads(fuzzy_set[0]['value'])
                    if len(fuzzy_set_updated_at):
                        sensor['fuzzy_set_updated_at'] = float(fuzzy_set_updated_at[0]['value'])
                    if len(ss_sensor_id):
                        sensor['ss_sensor_id'] = float(ss_sensor_id[0]['value'])

                    sensors.append(sensor)

            return sensors
        else:
            print result.content

        return []

    def get_all_virtual_sensors(self):
        url = self._api_uri() + '/search'
        data = {
            'data': {
                'Tags': ['Type:VirtualSensor']
            }
        }
        result = requests.post(url, headers=self._headers(),
                               data=json.dumps(data))
        if result.status_code == 200:
            info = result.json()
            sensors = []
            if 'result' in info:
                result = info['result']
                for sensor_def in result:
                    tags = sensor_def['tags']
                    names = [tag for tag in tags if tag['name'] == 'Name']
                    programming_type = [tag for tag in tags if tag['name'] == 'ProgrammingType']
                    conditions = [tag for tag in tags if tag['name'] == 'Conditions']
                    labels = [tag for tag in tags if tag['name'] == 'Labels']
                    samples = [tag for tag in tags if tag['name'] == 'Samples']
                    inputs = [tag for tag in tags if tag['name'] == 'Inputs']
                    ignores = [tag for tag in tags if tag['name'] == 'Ignore']

                    if len(ignores):
                        continue

                    sensor = {
                        'id': sensor_def['name'],
                        'name': names[0]['value'],
                        'labels': json.loads(labels[0]['value']),
                        'inputs': json.loads(inputs[0]['value']),
                        'samples': json.loads(samples[0]['value'])
                    }

                    if len(programming_type):
                        sensor['programming_type'] = programming_type[0]['value']
                    else:
                        sensor['programming_type'] = 'Demonstrated'

                    if len(conditions):
                        sensor['conditions'] = json.loads(conditions[0]['value'])

                    sensors.append(sensor)

            return sensors
        else:
            print result.content

        return []

    def post_sensor(self, sensor):
        url = self._api_uri() + '/sensor'

        data = {
            'data': {
                'name': sensor.name,
                'building': sensor.building,
                'identifier': sensor.name + str(randint(0, 1000))
            }
        }

        result = requests.post(url, headers=self._headers(),
                               data=json.dumps(data))
        if result.status_code == 200:
            info = result.json()
            sensor.id = info['uuid']
            tags = [
                {
                    'name': 'Type',
                    'value': 'VirtualSensor'
                },
                {
                    'name': 'Name',
                    'value': sensor.name
                },
                {
                    'name': 'Samples',
                    'value': json.dumps(sensor.samples)
                },
                {
                    'name': 'Inputs',
                    'value': json.dumps(sensor.inputs)
                },
                {
                    'name': 'Labels',
                    'value': json.dumps(sensor.labels)
                }
            ]
            return self.post_sensor_tags(sensor.id, tags)
        else:
            print result.content

        return False

    def post_sensor_tags(self, sensor_id, tags):
        url = self._api_uri() + '/sensor/'
        url += sensor_id + '/tags'

        data = {
            'data': tags
        }

        result = requests.post(url, headers=self._headers(),
                               data=json.dumps(data))

        if result.status_code != 200:
            print result.content
            return False

        return True

    def remove_sensor(self, sensor):
        return self.post_sensor_tags(sensor.id, [
            {
                'name': 'Ignore',
                'value': True
            }
        ])

    def post_sensor_value(self, sensor_id, value, timestamp):
        url = self._api_uri(False) + '/sensor/timeseries'

        data = [
            {
                'sensor_id': sensor_id,
                'samples': [
                    {
                        'time': timestamp,
                        'value': float(value)
                    }
                ]
            }
        ]

        result = requests.post(url, headers=self._headers(),
                               data=json.dumps(data))

        if result.status_code != 200:
            print result.content
            return False

        return True

    def get_timeseries_data(self, uuid, start_time, end_time):
        url = self._api_uri(False) + '/sensor/'
        url += uuid + '/timeseries?'
        url += 'start_time=' + str(start_time)
        url += '&end_time=' + str(end_time)

        result = requests.get(url, headers=self._headers())
        json = result.json()

        data = []
        if 'series' in json['data']:
            readings = json['data']['series'][0]
            columns = readings['columns']
            values = readings['values']
            index = columns.index('value')

            for value in values:
                data.append(value[index])
        else:
            print 'No data found for ' + uuid + ' from ' + str(start_time) + \
                ' until ' + str(end_time)
            return None

        return data

    def _api_uri(self, cs=True):
        url = self.bd_rest_api['server']
        if cs:
            url += ':81'
        else:
            url += ':82'
        url += self.bd_rest_api['api_prefix']
        return url

    def _headers(self):
        return {
            'content-type': 'application/json',
            'Authorization': 'Bearer ' + self.access_token
        }
