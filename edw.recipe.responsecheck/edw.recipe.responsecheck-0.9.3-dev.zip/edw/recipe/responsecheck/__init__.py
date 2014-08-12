# -*- coding: utf-8 -*-
"""Recipe responsecheck"""
import logging

import os

import zc.buildout


class Recipe(object):
    """Recipe class"""

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options
        self.logger = logging.getLogger(self.name)

        if 'start-port' not in options or not options['start-port'].isdigit():
            self.logger.error(
                'Parameter start-port not specified or not a number.')
            raise zc.buildout.UserError(
                'Parameter start-port not specified or not a number.')

        if 'end-port' not in options or not options['end-port'].isdigit():
            self.logger.error(
                'Parameter end-port not specified or not a number.')
            raise zc.buildout.UserError(
                'Parameter end-port not specified or not a number.')

        if 'step' not in options or not options['step'].isdigit():
            self.logger.error('Parameter step not specified or not a number.')
            raise zc.buildout.UserError(
                'Parameter step not specified or not a number.')

        if 'backends' not in options:
            self.logger.error('Parameter backends not specified.')
            raise zc.buildout.UserError('Parameter backends not specified.')

        if 'path' not in options or not os.path.isdir(options['path']):
            self.logger.error(
                'Parameter path not specified or directory does not exists.')
            raise zc.buildout.UserError(
                'Parameter path not specified or directory does not exists.')

        self.start_port = options['start-port']
        self.end_port = options['end-port']
        self.step = options['step']
        self.backends = options['backends'].split(' ')
        self.path = options['path'] + '/responsecheck.sh'

    def write_script(self):
        """Method for writing a bash script in a specified file"""
        script = open(self.path, 'w')

        script.write('#!/bin/bash\n')
        script.write('echo "*** Check instances have no errors ***";\n')
        script.write('for i in `seq %s %s %s`;\n' % (
        self.start_port, self.step, self.end_port))
        script.write('do\n')

        script.write('\techo "Checking instance $i"\n')

        backends_list = ""
        for backend in self.backends:
            backends_list += '"%s" ' % backend

        script.write('\tfor backend in %s;\n' % backends_list)
        script.write('\tdo\n')
        curl = 'curl --write-out %{http_code} --connect-timeout 5 --silent' +\
               ' --output /dev/null http://$backend:$i/www'
        script.write('\t\tresponse=$(%s)\n' % curl)
        script.write('\t\tresult="SUCCESS"\n')
        script.write('\t\tif [ $response -ne 200 ]\n')
        script.write('\t\tthen\n')
        script.write('\t\t\tresult="FAILED"\n')
        script.write('\t\tfi\n')
        script.write('\t\techo backend = $backend port = $i $result\n')
        script.write('\tdone\n')
        script.write('done')
        script.close()

        os.chmod(self.path, 0755)

    def install(self):
        """Method that install this recipe"""
        self.write_script()
        self.options.created(self.path)
        return self.options.created()

    def update(self):
        """Method that update this recipe"""
        self.write_script()
