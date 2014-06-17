from .. import api_app
from .fixtures import food_data, biosphere_data
from bw2data.backends import JSONDatabase
from bw2data.tests import BW2DataTest


class RestAPITestCase(BW2DataTest):
    def extra_setup(self):
        self.biosphere = JSONDatabase("biosphere")
        self.biosphere.register()
        self.biosphere.write(biosphere_data)
        self.food = JSONDatabase("food")
        self.food.register()
        self.food.write(food_data)
        self.app = api_app.test_client()
