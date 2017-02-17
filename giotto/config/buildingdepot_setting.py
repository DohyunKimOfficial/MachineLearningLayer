import json
import os

class BuildingDepotSetting:
    def __init__(self):
        fp = os.path.dirname(__file__) + '/buildingdepot_setting.json'
        self.setting = json.loads(open(fp, 'r').read())

    def get(self, settingName):
        return self.setting[settingName]
