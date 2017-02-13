import sys
import pickle
import json
import pymongo
import time
import datetime

from bson.objectid import ObjectId
from giotto.helper.buildingdepot_helper import BuildingDepotHelper

buildingdepot_helper = BuildingDepotHelper('../../config/buildingdepot_setting.json')

def timeseries_for_inputs(input_uuids, start_time, end_time):
    '''Returns timeseries data for given real sensors

    Returns an array of timeseries data for real sensors between start_time and
    end_time.

    Args:
        sample_id: An object ID of a sample
        user_id: A user ID of a user who perform this operaiton

    Returns:
        An array of timeseris data from multiple real sensors. Note that the lenghts
        of real time data vary among the real sensors because of their differences in
        sampling rates. Thus the return value is one-dimensional array of
        one-dimensional arrays, not a two-dimensional array.
    '''
    samples = []

    for uuid in input_uuids:
        values = buildingdepot_helper.get_timeseries_data(uuid, start_time, end_time)
        samples.append(values)

    return samples

def latest_timeseries_for_inputs(input_uuids, seconds):
    '''Returns timeseries data for given real sensors in the last specified seconds

    Returns an array of timeseries data for real sensors specified by input_uuids
    in the last specified seconds.

    Args:
        input_uuids: An array of real sensors' UUIDs
        seconds: A duration of sampling in seconds

    Returns:
        An array of timeseris data from multiple real sensors. Note that the lenghts
        of real time data vary among the real sensors because of their differences in
        sampling rates. Thus the return value is one-dimensional array of
        one-dimensional arrays, not a two-dimensional array.
    '''
    current_time = time.time()
    time.sleep(2+seconds)

    return timeseries_for_inputs(input_uuids, current_time, current_time+seconds)


def timestamp_to_time_string(t):
    '''Converts a unix timestamp to a string representation of the timestamp

    Args:
        t: A unix timestamp float

    Returns
        A string representation of the timestamp
    '''
    return time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(t)) + str(t-int(t))[1:10]+ 'Z'


def time_string_to_timestamp(string):
    '''Converts a string representation of a timestamp to a unix timestamp

    Args:
        string: A string representation of a timestamp

    Returns
        A unix timestamp
    '''
    s = string[0:19] # Year to second
    t = time.mktime(datetime.datetime.strptime(s, "%Y-%m-%dT%H:%M:%S").timetuple())

    millisec = string[19:-1]    #millisecond
    if millisec[0] == '.':
        millisec = '0' + millisec
        t += float(millisec)

    return t

