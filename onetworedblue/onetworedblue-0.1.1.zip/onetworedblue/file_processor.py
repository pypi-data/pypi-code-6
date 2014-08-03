import glob
import math
import shutil
import datetime

from fish_point import FishPoint
import fct_file
from image_size_data import ImageSizeData


__author__ = 'Eric'

import csv
import os.path


class FileProcessor(object):

    telem_file_fields = ['image',
                         'date',
                         'time',
                         'latitude',
                         'longitude',
                         'water_depth',
                         'altitude',
                         'range1',
                         'range2',
                         'range3',
                         'range4',
                         'heading',
                         'pitch',
                         'roll',
                         'conductivity',
                         'temperature',]

    def __init__(self):
        self.telem_list = None
        self._current_index = None

    @property
    def number_of_images(self):
        return len(self.telem_list)

    @property
    def current_index(self):
        return self._current_index

    @property
    def current_entry(self):
        if self.file_is_loaded:
            return self.telem_list[self._current_index]
        else:
            return None

    @property
    def current_fish_points(self):
        return self.current_entry['fish_points']

    @current_fish_points.setter
    def current_fish_points(self, value):
        self.current_entry['fish_points'] = value

    @property
    def file_is_loaded(self):
        if self.telem_list:
            return (len(self.telem_list) > 0)
        else:
            return False


    def make_fct_backup(self, directory_name):
        backup_dir = os.path.join(directory_name, 'fct_backups', datetime.datetime.now().strftime("%Y%m%dT%H%M%S"))

        try:
            os.makedirs(backup_dir)
        except OSError:
            pass

        for file in glob.glob(directory_name + '/*.fct'):
            shutil.copy(file, backup_dir)

    def read_telem_file(self, file_name):
        telem_list = []
        with open(file_name, 'r') as telem_file:
            reader = csv.DictReader(telem_file, self.telem_file_fields, delimiter=' ')

            for line in reader:
                telem_list.append(line)

        self.image_directory = os.path.dirname(file_name)

        self.make_fct_backup(self.image_directory)

        valid_telem_entries = []

        # Now, scan the directory to make sure we have all these images
        for entry in telem_list:
            # The telemetry file has a weird extension for the images... perhaps preprocessed?
            # Find the equivalent with .jpg at the end instead
            image_filename = ('.').join(entry['image'].split('.')[:-1]) + '.jpg'
            entry['image_name'] = image_filename
            image_pathname = os.path.join(self.image_directory, image_filename)

            # We need to use the altitude as a real number.
            try:
                altitude = float(entry['altitude'])
            except ValueError:
                continue

            # Make sure that we have everything we need
            if os.path.isfile(image_pathname) and not math.isnan(altitude):
                entry['image_path'] = image_pathname
                # Make a "good" list with only entries that have images
                valid_telem_entries.append(entry)

                # Get an object to handle the size conversions
                entry['image_size_data'] = ImageSizeData(image_pathname, altitude)

                # now, set up the count file
                fct_filename = ('.').join(entry['image'].split('.')[:-1]) + '.fct'
                fct_pathname = os.path.join(self.image_directory, fct_filename)
                entry['fct_path'] = fct_pathname

                # make a placeholder for points, comments
                entry['fish_points'] = []
                entry['comment'] = ""
                entry['substrate'] = "not classified"

                # And add some duplicate fields to make it easier to write the FCT file later
                entry['image_area'] = entry['image_size_data'].area_sq_meters
                entry['image_width'] = entry['image_size_data'].image_size_x
                entry['image_height'] = entry['image_size_data'].image_size_y

                # See if an FCT file already exists.  If it does, parse it.
                if os.path.isfile(fct_pathname):
                    fct_list = fct_file.read_fct_file(fct_pathname)
                    if len(fct_list) > 0:
                        try:
                            entry['comment'] = fct_list[0]['comment']
                            entry['substrate'] = fct_list[0]['substrate']

                            for fct_line in fct_list:
                                point = FishPoint()
                                for field in FishPoint.fields:
                                    point[field] = fct_line[field]

                                point['pos_x'] = int(float(point['pos_x']))
                                point['pos_y'] = int(float(point['pos_y']))

                                entry['fish_points'].append(point)
                        except ValueError:
                            pass


        self.telem_list = valid_telem_entries

        if len(valid_telem_entries) > 0:
            self._current_index = 0


    def get_next_image_pathname(self):
        if self._current_index is None:
            return ''

        next_index = self._current_index + 1

        if next_index >= len(self.telem_list):
            return ''

        return self.telem_list[next_index]['image_path']

    def get_prev_image_pathname(self):
        if self._current_index is None:
            return ''

        prev_index = self._current_index - 1

        if prev_index < 0:
            return ''

        return self.telem_list[prev_index]['image_path']

    def get_current_image_pathname(self):
        if self._current_index is None:
            return None

        return self.telem_list[self._current_index]['image_path']


    def go_to_next(self):
        if self._current_index is None:
            return None

        fct_file.save_fct_file(self.current_entry['fct_path'], self.current_entry)

        next_index = self._current_index + 1

        if next_index >= len(self.telem_list):
            return None

        self._current_index = next_index

    def go_to_previous(self):
        if self._current_index is None:
            return None

        fct_file.save_fct_file(self.current_entry['fct_path'], self.current_entry)

        prev_index = self._current_index - 1

        if prev_index < 0:
            return None

        self._current_index = prev_index


