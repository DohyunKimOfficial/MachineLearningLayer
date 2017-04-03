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

## Architecture

The ML layer is designed to be headless – it has no external API. It retrieves all the information it needs from BuildingDepot. It pushes new virtual sensors values as timeseries values to BuildingDepot.

It consists of two parts that communicate with each other using Redis:

1. Scheduler
   - it retrieves the current virtual sensors from BD every N seconds and creates jobs to update each of them
2. Workers
   - they take the jobs created by the scheduler, produce new virtual sensor values and push them to BD
   - there may be any number of workers
   - they can run on the same machine as the scheduler or they can be distributed on multiple machines to provide better scalability

## Usage

You can start a scheduler and 5 worker processes by running: `python run.py`

Alternatively, you can start them independently:

1. Run the scheduler script:
   - `python giotto/scheduler.py`
2. Run one or more workers:
   - `rq worker`

## Adding new virtual sensors

Virtual sensors have to be added as sensors in BD. To enable the ML layer to recognize them, they have to follow a certain format of tags.

[The conventions for the tags are described here.](https://github.com/IoT-Expedition/node-actuation-engine/wiki/Representation-of-entities-in-BuildingDepot)
