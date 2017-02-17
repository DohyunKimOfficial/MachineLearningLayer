class SensorManager:
    def __init__(self):
        self.sensors = []
        self.bd_helper = None

    def initialize_from_bd(self, bd_helper):
        self.bd_helper = bd_helper

    def add_sensor(self, sensor):
        self.sensors.append(sensor)

    def create_sensor(self, sensor):
        self.bd_helper.post_sensor(sensor)
        self.add_sensor(sensor)

    def sensor_with_id(self, id):
        return next(s for s in sensors if s.id == sensor_id)

    def remove_sensor(self, sensor):
        self.sensors = [s for s in self.sensors if s.id != sensor.id]
        sensor.remove()
