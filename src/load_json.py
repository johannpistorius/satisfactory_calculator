"""
@author johannpistorius
"""

import json
import os


class JSON:
    def __init__(self):
        parent = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        filename = os.path.join(parent, 'res', 'data', 'data.json')
        try:
            with open(filename, 'r') as json_file:
                self.data = json.load(json_file)
        except FileNotFoundError:
            print("JSON filed does not exist")

    def get_json_object(self):
        return self.data

    def get_json_object_recipes(self):
        return self.data["recipes"]

    def get_json_object_items(self):
        return self.data["items"]

    def get_json_object_miners(self):
        return self.data["miners"]

    def get_json_object_buildings(self):
        return self.data["buildings"]
