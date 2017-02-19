import json
import os


class BuildingDepotSetting:
    def __init__(self, env):
        fp = os.path.dirname(__file__) + '/buildingdepot_setting.json'
        self.setting = json.loads(open(fp, 'r').read())
        self.env = env

    def get(self, settingName):
        return self.setting[settingName]

    def oauth(self):
        return self.setting[self.env]['oauth']
