from giotto.helper.buildingdepot_helper import BuildingDepotHelper
from giotto.pipelines.publish_value import publish_value


bd_helper = BuildingDepotHelper('worker')


def check_condition(subject, operator, attr):
    subject = float(subject)
    attr = float(attr)
    if operator == 'EQ':
        return subject == attr
    if operator == 'LT':
        return subject < attr
    if operator == 'LTE':
        return subject <= attr
    if operator == 'GT':
        return subject > attr
    if operator == 'GTE':
        return subject >= attr

    return False


def check_conditions(value, conditions):
    for condition in conditions:
        res = check_condition(value, condition['operator'], condition['value'])
        if res:
            return condition['label']

    return None


def update_programmed_sensor(sensor, end_time):
    print 'Updating ' + sensor['name']

    start_time = end_time - 10

    data = bd_helper.get_timeseries_data(
            uuid=sensor['inputs'][0],
            start_time=start_time,
            end_time=end_time)

    if data and len(data):
        value = data[-1]
        conditions = sensor['conditions']
        label = check_conditions(value, conditions)

        if label:
            label_i = sensor['labels'].index(label)
            print(sensor['name'] + ' = ' + label)
            publish_value(bd_helper, sensor['id'], label_i, label,
                          end_time)
