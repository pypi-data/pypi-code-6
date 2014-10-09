#!/usr/bin/env python
import sys
import xml.etree.cElementTree as ET


class Galaxy(object):

    def __init__(self, argv=['script.py']):
        self.argv = argv
        self.executable = self.argv[0]

    def gen(self, param_collection=None, options=[], defaults=[], outputs=[],
            appinfo={}, tests=[], docstring=None, argv=[]):
        #opt_spec = pC.params()

        tool = ET.Element("tool")
        tool.set("id", appinfo['id'])
        tool.set("name", appinfo['name'])
        tool.set("version", appinfo['vers'])

        # Add all of our sections, passing a single xml_writer around.
        self.description_section(tool, appinfo['desc'])
        self.version_section(tool)
        self.stdio_section(tool)

        if docstring is not None:
            self.docstring = docstring
        else:
            self.docstring = "TODO: Write docstring for " + self.executable

        opt_spec = param_collection.params
        self.command_section(tool, opt_spec)
        self.input_section(tool, opt_spec)
        self.output_section(tool, opt_spec)
        self.help_section(tool, self.docstring)
        self.test_section(tool, tests)
        return ET.tostring(tool)

    def description_section(self, parent, appdesc):
        desc = ET.SubElement(parent, 'description')
        desc.text = appdesc

    def version_section(self, parent):
        vers = ET.SubElement(parent, 'version_command')
        vers.text = "python %s --version" % (self.executable, )

    def stdio_section(self, parent):
        stdio = ET.SubElement(parent, 'stdio')
        exit_code = ET.SubElement(stdio, 'exit_code')
        exit_code.set('range', '1:')
        exit_code.set('level', 'fatal')

    def command_section(self, parent, options):
        cmd = ET.SubElement(parent, 'command')
        cmd.set("interpreter", "python")

        command_string = '\n'.join([self.executable, '--galaxy',
                                   '--outfile_supporting $__new_file_path__']) + "\n"

        for command in options:
            addition = command.galaxy_command()
            if (not command._galaxy_specific and command._show_in_galaxy) or \
                (command._galaxy_specific and command._show_in_galaxy):
                if addition:
                    command_string += addition + "\n"

        cmd.text = command_string

    def input_section(self, parent, options):
        inputs = ET.SubElement(parent, 'inputs')
        for option in options:
            if not option.hidden:
                option.galaxy_input(inputs)

    def output_section(self, parent, options):
        outputs = ET.SubElement(parent, 'outputs')
        for option in options:
            option.galaxy_output(outputs)

    def help_section(self, parent, docstring):
        help_sec = ET.SubElement(parent, 'help')
        help_sec.text = docstring.lstrip()

    def test_section(self, parent, test_cases):
        tests = ET.SubElement(parent, 'tests')
        for test in test_cases:
            test_elem = ET.SubElement(tests, 'test')

            # Set parameters
            for param in test['params']:
                param_elem = ET.SubElement(test_elem, 'param')
                param_elem.set('name', param)
                param_elem.set('value', test['params'][param])

            # Files
            for output in test['outputs']:
                output_cmp = test['outputs'][output]
                output_elem = ET.SubElement(test_elem, 'output')
                output_elem.set('name', output)
                output_elem.set('file', output_cmp[1])

