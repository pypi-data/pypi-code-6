# -*- coding: utf-8 -*-

from radish.step import Step


class OutlineStep(Step):
    def replace_data_in_sentence(self, data):
        for k, v in data.iteritems():
            self._sentence = self._sentence.replace("<%s>" % k, v)

    def get_representation(self, ran):
        return ""
