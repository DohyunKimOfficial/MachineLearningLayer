'''
This module implements REST APIs for the GIoTTO machine learning layer
'''
from flask import Flask
from flask import request
from pprint import pprint
from pymongo import MongoClient
from influxdb import InfluxDBClient
import json
import time
from datetime import timedelta
from flask import make_response, current_app

from giotto.helper.buildingdepot_helper import BuildingDepotHelper

from giotto.sensors.sensor import Sensor
from giotto.sensors.sensor_manager import SensorManager

bd_helper = BuildingDepotHelper()
sensor_manager = SensorManager()
sensor_manager.initialize_from_bd(bd_helper)

app = Flask(__name__)


def jsonString(obj,pretty=False):
    if pretty == True:
        return json.dumps(obj, sort_keys=True, indent=4, separators=(',', ': ')) + '\n'
    else:
        return json.dumps(obj)

def sensor_to_dict(sensor):
    return {
        id: sensor.id,
        name: sensor.name,
        inputs: sensor.inputs,
        samples: sensor.samples
    }

@app.route("/")
def message():
    return "Building Depot Flask Server for the GIoTTO Machine Learning Layer"


@app.route('/time', methods=['GET'])
def get_time():
    '''Returns a current unix timestamp

    Returns a server timestamp. The timestamp is used to mark traning samples for
    machine learning. A sample is recorded in Mongo DB using start time, end time, label,
    and related sensor uuids. Because we cannot guarantee that time is sychronized between
    GIoTTO server and other devices. Use this API to obtain unix timestamps for adding
    training samples.

    Returns:
        {
            "url": A URL of the HTTP call
            "method": "GET"
            "result": "ok"
            "ret": A curernt unix timesamp
        }
    '''
    timestamp = time.time()
    dic = {
        'url':request.url,
        'method':request.method,
        'result':'ok',
        'ret':timestamp
    }

    return jsonString(dic)


@app.route('/sensor', methods=['POST'])
def create_sensor():
    '''Creates a virtual sensor

    Creates a virtual sensor using a JSON passed as data, and returns its object ID.

    Args as data:
        {
            "name": name of a virtual sensor
            "labels": An array of strings denoting labels
            "inputs": An array of UUIDs of real sensors used as inputs for a classifier
            "description": A description of this virtual sensor
              "samples": [
                {
                    "inputs": An array of UUIDs of real sensors
                    "label": String label
                    "start": 1199191.128,
                    "end": 1199199.128
                }
            ]
        }

    Returns:
        {
            "id": The virtual sensor's ID
        }

    '''
    json = request.get_json()
    pprint(json)

    sensor = Sensor(name=json['name'],
            building=json['building'],
            labels=json['labels'],
            inputs=json['inputs'],
            samples=json['samples'])

    sensor_manager.create_sensor(sensor)

    return jsonString({
        'id': sensor.id
    })


@app.route('/sensors/', methods=['GET'])
def getAllSensors():
    '''Returns a list of all virtual sensors.

    Returns a list of all virtual sensors in the ML layer as an array of objects.

    Returns:
        {
            "sensors":[
                {
                    "id": A virtual sensor's object ID
                    "name": A sensor name
                    "sensor_uuid": A UUID of a sensor if it's registerd in BD
                    "user_id": An ID of a user who created this sensor
                    "labels": An array of labels
                    "inputs": An array of sensor UUIDs in BD used as inputs for a classifier
                    "description": A description of a sensor
                },
                { More sensor objects if there are }
            ]
        }
    '''

    sensors = list(map(sensor_to_dict, sensor_manager.sensors))

    return jsonString({
        'sensors': sensors
    })


@app.route('/sensor/<sensor_id>', methods=['GET'])
def get_sensor(sensor_id):
    '''Returns informatoin about a virtual sensor

    Returns an object containing information about a virtual sensor.

    Args as a part of URL:
        <sensor_id>: A sensor's object ID.

    Returns:
        {
            "id": A virtual sensor's object ID
            "name": A sensor name
            "sensor_uuid": A UUID of a sensor if it's registerd in BD
            "user_id": An ID of a user who created this sensor
            "labels": An array of labels
            "inputs": An array of sensor UUIDs in BD used as inputs for a classifier
            "description": A description of a sensor
        }
    '''
    user_id = 'default'

    sensors = sensor_manager.sensor_with_id(sensor_id)

    return jsonString(sensor_to_dict(sensor))


@app.route('/sensor/<sensor_id>', methods=['DELETE'])
def delete_sensor(sensor_id):
    '''Deletes a virtual sensor

    Deletes a virtual sensor, corresponding classifier, and samples from ML Layer's database.

    Args as a part of URL:
        <sensor_id>: An object ID of the virtual sensor

    Returns:
        {
            "url": A URL of the HTTP call
            "method": "DELETE"
            "result": error when deletion failed, otherwise ok
        }
    '''

    sensor = sensor_manager.sensor_with_id(sensor_id)
    sensor_manager.remove_sensor(sensor)

    return 'OK'

@app.route('/sensor/<sensor_id>/classifier/predict', methods=['GET'])
def predict(sensor_id):
    '''Makes a prediction using a classifier

    Makes a prediction using a pre-trained classifier with timeseries data in a range
    [end time - sampling period, end time]. sampling period is an average of sampling
    durations in a training set, which is stored as a part of a classifier.
    When end_time is not specific, current time is used as end_time.

    Args as a part of URL:
    <sensor_id>: An object ID of a virtual sensor_id

    Args as data:
    end_time: A unix timestamp. When omitted, current time is used as end_time.

    Returns:
        {
            "url": A URL of the HTTP call
            "method": "GET"
            "result": Error when prediction failed, otherwise ok
            "message": A human readable message from classifier.manager.train
            "ret": A predicted label
        }
    '''
    user_id = 'default'
    end_time = request.args.get('time')

    clf_result = classifier_manager.predict(sensor_id, user_id, end_time)
    dic = {
        'url':request.url,
        'method':request.method,
        'result': clf_result.result,
        'message': clf_result.message,
        'ret': clf_result.prediction
    }

    return jsonString(dic)


if __name__=="__main__":
    app.run(host='0.0.0.0', debug=True)
