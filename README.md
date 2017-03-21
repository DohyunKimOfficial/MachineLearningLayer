Machine Learning Layer for GIoTTO
=================================

The Machine Learning Layer is a part of the GIoTTO stack that transforms
raw sensor readings to more semantically meaningful information.

## Installation

1. Install Redis: https://redis.io/topics/quickstart
   - enter the configuration for Redis into the file `giotto/connect_to_redis.py`
2. Install packages: `pip install -r requirements.txt`

## Usage

1. Run the scheduler script which every N seconds retrieves the current virtual
   sensors from BD and creates job to update each of them
   - `python giotto/scheduler.py`
2. Run one or more workers that take the jobs created by the scheduler and executes
   them
   - `rq worker`

## Adding new virtual sensors

Virtual sensors have to be added as sensors in BD with the following tags:

- `Type`
  - Has to equal: `VirtualSensor`
- `Name`
  - Name of the sensor as string (optional for the ML part)
- `Inputs`
  - JSON list of UUIDs of sensors to be used when predicting new values
  - e.g.,  ["13403c8a-8de5-47ae-19589111", ...]
- `Labels`
  - Labels recognized by the sensor in JSON
  - E.g., `["Day", "Night"]`
- `Samples`
  - Serialized JSON as string
  - List of samples, where each contains the following info:
    - 'inputs' - list of UUIDs of sensors to be used
    - 'start' - timestamp of the start of the sample
    - 'end' - timestamp of the end of the sample
    - 'label' - label of the sample
  - E.g., `[{"inputs": ["13403c8a-8de5-47ae-8593212593"], "end": 1487346199.731, "start": 1487346189.291, "label": "Day"}, ...]`
