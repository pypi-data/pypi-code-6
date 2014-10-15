# vim: set expandtab tabstop=4 shiftwidth=4 softtabstop=4:
#
# Copyright 2013-2014 Flavio Garcia
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import iflux.conf
import os
import sys

command_categories = dict()


def run_from_command_line():
    try:
        command = sys.argv[1]
        if not command_exists(command):
            show_command_line_usage()
        else:
            run_command(command)
    except IndexError:
        show_command_line_usage()

def show_command_line_usage():
    print "iFlux Tornado Framework"
    print "\nUsage: %s <command>" % os.path.split(sys.argv[0])[1]
    print "\nCommands are:\n"
    command_template = "  {0.name:10}{0.description:40}"
    for category, commands in command_categories.iteritems():
        print "%s:\n" % category
        for command in commands:
            print command_template.format(command)
    print ""
    print "    --name=value    whatever"
    print "    --help          display help"


def command_exists(command):
    for category, commands in command_categories.iteritems():
        for existing_command in commands:
            if command == existing_command.name:
                return True
    return False

def run_command(command):
    for category, commands in command_categories.iteritems():
        for existing_command in commands:
            if command == existing_command.name:
                print existing_command.tasks
                task = existing_command.tasks(existing_command)
                task.run()

class ScaffoldingCommand():

    def __init__(self, category, name, description, help, parameters=None, tasks=None):
        self.category = category
        self.name = name
        self.description = description
        self.help = help
        self.parameters = parameters
        self.tasks = tasks
        if category not in sys.modules[__name__].command_categories:
            sys.modules[__name__].command_categories[category] = []
        sys.modules[__name__].command_categories[category].append(self)

    def get_help(self):
        return self.help 


class ScaffoldingTask():

    def __init__(self, action):
        self.action = action

    def run(self):
        pass

    def get_help(self):
        pass


class CheckIfProjectExistsScaffoldingTask(ScaffoldingTask):

    def run(self):
        #TODO: Check if project exists
        print os.getcwd()


class CreateProjectScaffoldingTask(ScaffoldingTask):
    
    def run(self):
        #TODO: Check if project exists
        #TODO: If dosn't exists create project
        #TODO: If exists throw an error
        pass


class AddModuleToProjectScaffoldingTask(ScaffoldingTask):

    def run(self):
        #TODO: Check if module exists by name
        #TODO: If doesn't exists create module
        #TODO: If Exists throw an error
        pass


class RunProjectTask(ScaffoldingTask):

    def run(self):
        import tornado.ioloop
        import tornado.httpserver
        import iflux.conf
        import iflux.core

        http_server = tornado.httpserver.HTTPServer(iflux.core.Application())
        http_server.listen(iflux.conf.application['port'])
        tornado.ioloop.IOLoop.instance().start()

class InstallProjectTask(ScaffoldingTask):

    def run(self):
        import iflux.core
        application = iflux.core.Application()
        for key, module in application.modules.iteritems():
            module.install()

ScaffoldingCommand('iFlux', 'init', 'Create a new project in the given directory', '')

ScaffoldingCommand('iFlux', 'install', 'Install the application', '', [], InstallProjectTask)

ScaffoldingCommand('iFlux', 'run', 'Run the application', '', [], RunProjectTask)
