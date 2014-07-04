# -*- coding: utf-8 -*-

from radish.scenario import Scenario
from radish.config import Config
from radish.colorful import colorful
from radish.outlinestep import OutlineStep
from radish.exceptions import FeatureFileNotValidError


class ScenarioOutlineExample(Scenario):
    def __init__(self, id, feature, sentence, filename, line_no, headers, scenario_outline):
        Scenario.__init__(self, id, feature, sentence, filename, line_no)
        self._headers = headers
        self._data = [x.strip() for x in sentence.split("|") if x.strip()]
        self._scenario_outline = scenario_outline
        scenario_outline.is_max_example_data_len(len(max(self._data, key=len)))

    def create_steps_from_outline(self):
        steps = self._scenario_outline.get_steps()
        if len(self._headers) != len(self._data):
            raise FeatureFileNotValidError(self._filename, "Scenario Outline Example on line %d has another count of fields as the header does (data:%d/header:%d)" % (self._line_no, len(self._data), len(self._headers)))

        data = dict(zip(self._headers, self._data))
        for step in steps:
            outline_step = OutlineStep(step.get_id(), step.get_scenario(), step.get_sentence(), step.get_filename(), step.get_line_no())
            outline_step.replace_data_in_sentence(data)
            self.append_step(outline_step)

    def get_indentation(self):
        return "  " + " " * len(str(Config().highest_feature_id)) + "  " + "   "

    def get_representation(self, ran):
        output = ""
        if ran:
            pass
            if not Config().no_line_jump and not Config().no_overwrite:
                output += "\033[A\033[K"

            passed = self.has_passed()
            if passed is None and Config().no_skipped_steps:
                return

            if passed:
                color_fn = colorful.bold_green
            elif passed is False:
                color_fn = colorful.bold_red
            elif passed is None:
                color_fn = colorful.cyan

            if not Config().no_overwrite:
                if not Config().no_indentation:
                    output += self.get_indentation()
                if not Config().no_numbers:
                    output += color_fn("%*d. " % (0 if Config().no_indentation else len(str(Config().highest_step_id)), self._id))
                max_example_data_len = self._scenario_outline.get_max_example_data_len()
                output += colorful.bold_white("| ") + colorful.bold_white(" | ").join([(color_fn(d) + " " * (max_example_data_len - len(d))) for d in self._data]) + colorful.bold_white("|") + "\n"

            if passed is False:
                first_failed_step = [s for s in self._steps if s.has_passed() == False][0]
                fail_reason = first_failed_step.get_fail_reason()
                indent = ""
                if not Config().no_indentation:
                    indent = self.get_indentation()
                    if not Config().no_numbers:
                        indent += "   "

                output += indent + colorful.red("Step '") + colorful.bold_red(first_failed_step.get_sentence()) + colorful.red("' failed:\n")
                if Config().with_traceback:
                    for l in fail_reason.get_traceback().splitlines():
                        output += indent + colorful.red(l) + "\n"
                else:
                    output += indent + colorful.red(fail_reason.get_name() + ": ") + colorful.bold_red(fail_reason.get_reason()) + "\n"

            # make ending newline
            scenarios = self._feature.get_scenarios()
            idx = scenarios.index(self)
            if idx == len(scenarios) - 1:
                output += "\n"
        else:
            if not Config().no_indentation:
                output += self.get_indentation()
            if not Config().no_numbers:
                output += colorful.bold_brown("%*d. " % (0 if Config().no_indentation else len(str(Config().highest_step_id)), self._id))
            max_example_data_len = self._scenario_outline.get_max_example_data_len()
            output += colorful.bold_white("| ") + colorful.bold_white(" | ").join([(colorful.bold_brown(d) + " " * (max_example_data_len - len(d))) for d in self._data]) + colorful.bold_white("|") + "\n"

        return output
