import copy

__author__ = 'yarnaid'

import numpy
import utils

conf = utils.load_config()


default_params = dict()
load_params = default_params
dump_params = default_params


class AbstractData:
    time_var = None
    values = None
    errors = None
    n = None

    def __init__(self, file_name):
        self.load(file_name)


    def load(self, file_name):
        print self.__name__ + ' load method stub'


    def dump(self, file_name):
        # TODO: all data to one variable
        # data = None
        # numpy.savetxt(file_name, data, **dump_params)
        print self.__name__ + ' dump method stub'


class TimeRow(AbstractData):
    # stat = {
    #     'sf': None,
    #     'ft': None,
    #     'acf': None,
    #     'pg': None,
    #     'scalogram': None
    #     }
    # mean = copy.copy(stat)
    # std = copy.copy(stat)
    # level = copy.copy(stat)
    # scales = None
    # freqs = None
    # X_q = None
    # centered_values = None

    def load(self, file_name):
        self.raw_data = numpy.loadtxt(file_name, **load_params)
        self.time_var = self.raw_data[:, 0] + self.raw_data[:, 1] / 12.
        self.values = self.raw_data[:, 4]
        self.n = len(self.time_var)


    def __str__(self):
        res = str()
        if self.errors is not None:
            get_line = lambda i: str(self.time_var[i]) + ' ' + str(self.values[i]) + ' ' + str(self.errors[i]) + '\n'
        else:
            get_line = lambda i: str(self.time_var[i]) + ' ' + str(self.values[i]) + '\n'

        for i in xrange(self.n):
            res += get_line(i)

        return res

