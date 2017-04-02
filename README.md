Machine Learning Layer for GIoTTO
=================================

The Machine Learning Layer is a part of the [GIoTTO stack](http://iotexpedition.org) that transforms
raw sensor readings to more semantically meaningful information.

## Installation

1. Install Redis: https://redis.io/topics/quickstart
   - Enter the configuration for Redis into the file giotto/connect_to_redis.py
2. Configure BD access keys and hostname
   - In giotto/config/buildingdepot_setting.json
4. Install dependencies: `sudo apt-get install libblas-dev liblapack-dev libatlas-base-dev gfortran`
3. Install python packages from the requirements.txt file
   - `sudo pip install -r requirements.txt`
4. Start scheduler and worker processes: python run.py

## Usage

1. Run the scheduler script which every N seconds retrieves the current virtual
   sensors from BD and creates job to update each of them
   - `python giotto/scheduler.py`
2. Run one or more workers that take the jobs created by the scheduler and executes
   them
   - `rq worker`

## Adding new virtual sensors

Virtual sensors have to be added as sensors in BD. To enable the ML layer to recognize them, they have to follow a certain format of tags.

[The conventions for the tags are described here.](https://github.com/IoT-Expedition/node-actuation-engine/wiki/Representation-of-entities-in-BuildingDepot)
