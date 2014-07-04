# -*- coding: utf-8 -*-

from radish.step import Step
from radish.config import Config
from radish.colorful import colorful


class OutlinedStep(Step):
    def run(self):
        return True

    def get_representation(self, ran):
        output = ""
        if not ran:
            splitted = self.get_sentence_splitted()
            if not Config().no_indentation:
                output += self.get_indentation()
            if not Config().no_numbers:
                output += colorful.cyan("%*d. " % (0 if Config().no_indentation else len(str(Config().highest_step_id)), self._id))
            output += colorful.cyan(self.get_sentence_splitted()[1]) + "\n"
        return output
