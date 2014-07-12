import datetime
import astral

from eyes_on_me.config import config
from eyes_on_me.strategy import LightningStrategy


class TimedStrategy(LightningStrategy):
    def __init__(self):
        self.light_table = config['timed-strategy']['light-table']

    def _get_city_lights(self, date):
        astra = astral.Astral()
        city = astra[config['timed-strategy']['city']]
        sun = city.sun(date)
        return [(k, sun[k]) for k in
                self.light_table.keys()]

    def _lightning_for_time(self, date):
        # get lights
        lights = self._get_city_lights(date)
        # get two closer lights from table
        sorted_lights = sorted(lights, key=lambda light: light[1] - date)
        left_light = sorted_lights[1]
        right_light = sorted_lights[0]
        # approximate current level of light
        left_delta = float((date - left_light[1]).seconds)
        right_delta = float((right_light[1] - date).seconds)
        overall_delta = float((right_light[1] - left_light[1]).seconds)
        left_light_level = self.light_table[left_light[0]]
        right_light_level = self.light_table[right_light[0]]
        return (left_light_level * right_delta +
                right_light_level * left_delta) / overall_delta

    def get_lightning(self):
        astra = astral.Astral()
        city = astra[config['timed-strategy']['city']]
        return self._lightning_for_time(datetime.datetime.now(city.tz))
