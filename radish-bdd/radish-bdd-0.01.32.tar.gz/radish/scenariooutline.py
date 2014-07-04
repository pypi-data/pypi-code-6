# -*- coding: utf-8 -*-

from radish.scenario import Scenario
from radish.config import Config
from radish.colorful import colorful


class ScenarioOutline(Scenario):
    def __init__(self, id, feature, sentence, filename, line_no):
        Scenario.__init__(self, id, feature, sentence, filename, line_no)
        self._title = "Scenario Outline"
        self._max_example_data_len = 0

    def is_max_example_data_len(self, length):
        if length > self._max_example_data_len:
            self._max_example_data_len = length

    def get_max_example_data_len(self):
        return self._max_example_data_len

    def set_examples_header(self, headers):
        self._headers = headers
        self.is_max_example_data_len(len(max(headers, key=len)))

    def get_representation(self, ran):
        output = ""
        if ran:
            output += "\n"
            indent = ""
            if not Config().no_indentation:
                indent = self.get_indentation()
            output += indent + colorful.bold_white("Examples:\n")
            if indent:
                indent += "   "
                if not Config().no_numbers:
                    indent += "   "
            output += indent + colorful.bold_white("| ") + colorful.bold_white(" | ").join([colorful.cyan(h) for h in self._headers]) + colorful.bold_white(" |") + "\n"
        else:
            if not Config().no_indentation:
                output += self.get_indentation()
            if not Config().no_numbers:
                output += colorful.bold_white("%*d. " % (0 if Config().no_indentation else len(str(Config().highest_scenario_id)), self._id))
            if Config().with_section_names:
                output += colorful.bold_white("%s: " % self._title)
            output += colorful.bold_white(self._sentence) + "\n"
        return output
