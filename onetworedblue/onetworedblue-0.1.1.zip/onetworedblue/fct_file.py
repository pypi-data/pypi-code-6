from collections import defaultdict

__author__ = 'Eric'
import csv

from fish_point import FishPoint

fct_file_fields = ['latitude',
                 'longitude',
                 'water_depth',
                 'image_name',
                 'date',
                 'time',
                 'image_area',
                 'image_width',
                 'image_height',
                 'substrate',] + FishPoint.fields + ['comment',]

def read_fct_file(file_name):
    fct_list = []
    with open(file_name, 'r') as fct_file:
        reader = csv.DictReader(fct_file, fct_file_fields, delimiter=',')

        for line in reader:
            fct_list.append(line)

    return fct_list

def _write_fct_file(file_name, fct_list):
     with open(file_name, 'wb') as fct_file:
        writer = csv.DictWriter(fct_file, fct_file_fields, delimiter=',')

        writer.writerows(fct_list)

def _annotation_entry_to_fct_list(telem_dict):
    fct_list = []
    for fish_point in telem_dict['fish_points']:
        fct_line = defaultdict(None)

        # copy all the keys that exist one for one
        for key in fct_file_fields:
            if key in telem_dict.keys():
                fct_line[key] = telem_dict[key]

        # Now add the individual count points (individual fish)
        for key in FishPoint.fields:
            fct_line[key] = fish_point[key]

        # Convert to NaNs.
        _replace_none_with_nan(fct_line)

        fct_list.append(fct_line)

    return fct_list


def save_fct_file(file_name, telem_dict):
    fct_list = _annotation_entry_to_fct_list(telem_dict)
    _write_fct_file(file_name, fct_list)


def _replace_nan_with_none(dict_to_change):
    for (key, value) in dict_to_change.iteritems():
        if str(value).lower() is "nan":
            dict_to_change[key] = None

def _replace_none_with_nan(dict_to_change):
    for (key, value) in dict_to_change.iteritems():
        if value is None:
            dict_to_change[key] = "NaN"

