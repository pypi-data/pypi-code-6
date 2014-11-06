#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Data analyzation metrics

Each algorithm works on a set of handwritings. They have to be applied like
this:

 >>> import data_analyzation_metrics
 >>> a = [{'is_in_testset': 0,
           'formula_id': 31L,
           'handwriting': HandwrittenData(raw_data_id=2953),
           'formula_in_latex': 'A',
           'id': 2953L},
          {'is_in_testset': 0,
           'formula_id': 31L,
           'handwriting': HandwrittenData(raw_data_id=4037),
           'formula_in_latex': 'A',
           'id': 4037L},
          {'is_in_testset': 0,
           'formula_id': 31L,
           'handwriting': HandwrittenData(raw_data_id=4056),
           'formula_in_latex': 'A',
           'id': 4056L}]
 >>> creator_metric = Creator('creator.csv')
 >>> creator_metric(a)
"""
import inspect
import imp
import os
import logging
import sys
import time
from collections import defaultdict

# hwrt modules
from . import HandwrittenData
from . import preprocessing
from . import utils


def get_class(name):
    """Get the class by its name as a string."""
    clsmembers = inspect.getmembers(sys.modules[__name__], inspect.isclass)
    for string_name, act_class in clsmembers:
        if string_name == name:
            return act_class

    # Check if the user has specified a plugin and if the class is in there
    cfg = utils.get_project_configuration()
    if 'data_analyzation_plugins' in cfg:
        basename = os.path.basename(cfg['data_analyzation_plugins'])
        modname = os.path.splitext(basename)[0]
        usermodule = imp.load_source(modname, cfg['data_analyzation_plugins'])
        clsmembers = inspect.getmembers(usermodule, inspect.isclass)
        for string_name, act_class in clsmembers:
            if string_name == name:
                return act_class

    logging.debug("Unknown class '%s'.", name)
    return None


def get_metrics(metrics_description):
    """Get metrics from a list of dictionaries. """
    metric_list = []
    for metric in metrics_description:
        for feat, params in metric.items():
            feat = get_class(feat)
            if params is None:
                metric_list.append(feat())
            else:
                parameters = {}
                for dicts in params:
                    for param_name, param_value in dicts.items():
                        parameters[param_name] = param_value
                metric_list.append(feat(**parameters))
    return metric_list


def prepare_file(filename):
    """Trunkate the file and return the filename."""
    root = utils.get_project_root()
    folder = os.path.join(root, "analyzation/")
    workfilename = os.path.join(folder, filename)
    open(workfilename, 'w').close()  # Truncate the file
    return workfilename


# Only data analyzation calculation classes follow
# Every class must have a __str__, __repr__ and __call__ function where
# __call__ must take exactly one argument of type list of dictionaries
# Every class must have a constructor which takes the filename as a parameter.
# This filename has to be used to write the evaluation results
# (preferably in CSV format) to this file.


class Creator(object):
    """Analyze who created most of the data."""

    def __init__(self, filename="creator.csv"):
        self.filename = filename

    def __repr__(self):
        return "AnalyzeCreator(%s)" % self.filename

    def __str__(self):
        return "AnalyzeCreator(%s)" % self.filename

    def __call__(self, raw_datasets):
        # prepare file
        root = utils.get_project_root()
        folder = os.path.join(root, "analyzation/")
        workfilename = os.path.join(folder, self.filename)
        open(workfilename, 'w').close()  # Truncate the file
        write_file = open(workfilename, "a")
        write_file.write("creatorid,nr of symbols\n")  # heading

        print_data = defaultdict(int)
        start_time = time.time()
        for i, raw_dataset in enumerate(raw_datasets):
            if i % 100 == 0 and i > 0:
                utils.print_status(len(raw_datasets), i, start_time)
            print_data[raw_dataset['handwriting'].user_id] += 1
        print("\r100%"+"\033[K\n")
        # Sort the data by highest value, descending
        print_data = sorted(print_data.items(),
                            key=lambda n: n[1],
                            reverse=True)
        # Write data to file
        write_file.write("total,%i\n" %
                         sum([value for _, value in print_data]))
        for userid, value in print_data:
            write_file.write("%i,%i\n" % (userid, value))
        write_file.close()
