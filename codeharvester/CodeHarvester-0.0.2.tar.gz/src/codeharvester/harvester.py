# -*- coding: utf-8 -*-
#
# CodeHarvester - harvester.py
#
# Copyright (c) 2014 Denis Gonsiorovsky
# Licensed under the MIT license

import logging
import os
import tempfile
import sys


VERSION = "0.0.2"

logging.basicConfig(format='%(levelname)s: %(message)s')


class Harvester(object):
    flags = None
    req_parents = None
    req_paths = None
    req_linenos = None

    def __init__(self, flags=None, *args, **kwargs):
        self.flags = {
            'cleanup': True,
            'verbose': False,
        }

        if flags:
            self.flags.update(flags)

        self.req_parents = []
        self.req_paths = []
        self.req_linenos = []


    def skip_unresolved_requirement(self, filename, i):
        self.req_parents.append(filename)
        self.req_paths.append(None)
        self.req_linenos.append(i)

    def extract_requirement(self, line):
        """
        A requirement detection algorithm should be implemented here.
        """
        raise NotImplementedError

    def insert_requirement(self, output_file, requirement_file, requirement_filename):
        """
        A requirement insertion algorithm should be implemented here.
        """
        raise NotImplementedError

    def parse_requirements(self, filename):
        """
        Recursively find all the requirements needed
        storing them in req_parents, req_paths, req_linenos
        """

        cwd = os.path.dirname(filename)

        try:
            fd = open(filename, 'r')
            for i, line in enumerate(fd.readlines(), 0):
                req = self.extract_requirement(line)

                # if the line is not a requirement statement
                if not req:
                    continue

                req_path = req

                if not os.path.isabs(req_path):
                    req_path = os.path.normpath(os.path.join(cwd, req_path))

                if not os.path.exists(req_path):
                    logging.warning("Requirement '{0}' could not be resolved: '{1}' does not exist.".format(req, req_path))
                    if self.flags['cleanup']:
                        self.skip_unresolved_requirement(filename, i)
                    continue

                # if the requirement is already added to the database, skip it
                if req_path in self.req_paths:
                    logging.warning("Skipping duplicate requirement '{0}' at '{2}:{3}' [file '{1}'].".format(
                        req,
                        req_path,
                        filename,
                        i+1  # human-recognizable line number
                    ))
                    if self.flags['cleanup']:
                        self.skip_unresolved_requirement(filename, i)
                    continue

                # store requirements to the global database
                self.req_parents.append(filename)
                self.req_paths.append(req_path)
                self.req_linenos.append(i)

                # recursion
                self.parse_requirements(req_path)
            fd.close()
        except IOError as err:
            logging.warning("I/O error: {0}".format(err))

    def replace_requirements(self, infilename, outfile_initial=None):
        """
        Recursively replaces the requirements in the files with the content of the requirements.
        Returns final temporary file opened for reading.
        """

        infile = open(infilename, 'r')

        # extract the requirements for this file that were not skipped from the global database
        _indexes = tuple(z[0] for z in filter(lambda x: x[1] == infilename, enumerate(self.req_parents)))
        req_paths = tuple(z[1] for z in filter(lambda x: x[0] in _indexes, enumerate(self.req_paths)))
        req_linenos = tuple(z[1] for z in filter(lambda x: x[0] in _indexes, enumerate(self.req_linenos)))

        if outfile_initial:
            outfile = outfile_initial
        else:
            outfile = tempfile.TemporaryFile('w+')

        # write the input file to the output, replacing
        # the requirement statements with the requirements themselves
        for i, line in enumerate(infile.readlines()):
            if i in req_linenos:
                req_path = req_paths[req_linenos.index(i)]

                # skip unresolved requirement
                if not req_path:
                    continue

                # recursion
                req_file = self.replace_requirements(req_path)

                # insert something at cursor position
                self.insert_requirement(outfile, req_file, req_path)

                req_file.close()
            else:
                outfile.write(line)

        infile.close()

        if not outfile_initial:
            outfile.seek(0)

        return outfile

    def harvest_file(self, infilepath, outfilepath=None):
        if not os.path.exists(infilepath):
            logging.error("Input file '{0}' does exists!".format(infilepath))
            return

        self.req_parents.append(None)
        self.req_paths.append(infilepath)
        self.req_linenos.append(None)

        self.parse_requirements(infilepath)

        try:
            if outfilepath:
                outfile = open(outfilepath, 'w+')
            else:
                outfile = sys.stdout
            self.replace_requirements(infilepath, outfile)
            outfile.close()
        except IOError as err:
            logging.error("I/O while writing output to '{0}': {1}".format(outfilepath, err))
            return


class JSHarvester(Harvester):
    """
    Simple implementation of the Harvester for JS files
    """
    require_template = '//= require'

    def __init__(self, *args, **kwargs):
        super(JSHarvester, self).__init__(*args, **kwargs)
        self._require_template_length = len(self.require_template)

    def extract_requirement(self, line):
        if not line.startswith(self.require_template):
            return None

        req = line[self._require_template_length:].strip()
        return req

    def insert_requirement(self, output_file, requirement_file, requirement_filename):
        if self.flags['verbose']:
            output_file.write("\n// ----- BEGIN REQUIREMENT '{0}' -----\n".format(requirement_filename))

        output_file.write(requirement_file.read())
        output_file.write('\n')  # needed for requirements that does not contain a newline at the end of file

        if self.flags['verbose']:
            output_file.write("// ----- END REQUIREMENT '{0}' -----\n\n".format(requirement_filename))



