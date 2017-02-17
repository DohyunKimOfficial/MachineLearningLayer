import requests
import time
import json
import time
import calendar
from random import randint
from giotto.config.buildingdepot_setting import BuildingDepotSetting

class BuildingDepotHelper:
    def __init__(self):
        setting = BuildingDepotSetting()
        self.bd_rest_api = setting.get('buildingdepot_rest_api')
        self.oauth = setting.get('oauth')
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

    def post_sensor(self, sensor):
        url = self._api_uri() + '/sensor'
        print url

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
            return self.post_sensor_tags(sensor)
        else:
            print result.content

        return False

    def post_sensor_tags(self, sensor):
        url = self._api_uri() + '/sensor/'
        url += sensor.id + '/tags'

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

        data = {
            'data': tags
        }

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

        readings = json['data']['series'][0]
        columns = readings['columns']
        values = readings['values']
        index = columns.index('value')

        data = []
        for value in values:
            data.append(value[index])

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
