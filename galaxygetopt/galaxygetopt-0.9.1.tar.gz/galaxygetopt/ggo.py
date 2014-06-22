#!/usr/bin/env python
import sys
from pc import ParameterCollection
from galaxy import Galaxy
from tg import TestGenerator


class GalaxyGetOpt(object):

    def __init__(self, options=[], outputs=[], defaults={}, tests=[],
                 doc=None, argv=None):

        # Allow spec of argv here so we can override it during testing
        if argv is not None:
            self.argv = argv
        else:
            self.argv = sys.argv

        self.appid = defaults['appid']
        self.appvers = defaults['appvers']
        self.appname = defaults['appname']
        self.appdesc = defaults['appdesc']
        self.usage_desc = '%s: %s\n' % (self.appname, self.appdesc)

        parameter_collection = self.convert_opt_arr_to_params(options, outputs)

        if '--generate_galaxy_xml' in self.argv[1:]:
            ggx = Galaxy(argv=self.argv)
            print ggx.gen(param_collection=parameter_collection,
                          appinfo={'id': self.appid, 'name':
                                   self.appname, 'desc': self.appdesc,
                                   'vers': self.appvers},
                          docstring=doc, outputs=outputs,
                          options=options, defaults=defaults,
                          tests=tests)
            sys.exit(1)

        if '--gen_test' in self.argv[1:]:
            tg = TestGenerator()
            print tg.gen(tests)
            sys.exit(1)

        if '--dump_options' in self.argv[1:]:
            print self.serialize_opt_to_yaml(options=options,
                                             outputs=outputs,
                                             defaults=defaults,
                                             tests=tests)
            sys.exit(1)

        # Storing for easy access
        if '--galaxy' in self.argv[1:]:
            self.galaxy = True
        else:
            self.galaxy = False

        # Finally, store the parsed options
        self.opt = self.pC.getarg(argv_override=self.argv[1:])


    def serialize_opt_to_yaml(self, options=[], outputs=[], defaults={}, tests=[]):
        """Dumps options interface to yaml"""
        import yaml
        return yaml.dump({
            'options': options,
            'outputs': outputs,
            'defaults': defaults,
            'tests': tests,
        })

    def convert_opt_arr_to_params(self, options_array, outputs):
        """Returns a completed parameterCollection object

        Internally we add a couple other parameters that should be
        available to the user to our parameterCollection. Inside PC
        the "verbose" option is added, while here we add:

            - generate_galaxy_xml
            - galaxy
            - outfile_supporting

        The outfile_supporting variable is used as the location to
        place generated files (primary_NNNN_blah_visible_txt)

        """
        pC = ParameterCollection(self.usage_desc, vers=self.appvers)

        pC.push_params([[],['Options']])
        for option in options_array:
            pC.push_param(option)

        pC.push_param(['Output Files'])
        for output_file_option in self.fix_outputs(outputs):
            pC.push_param(output_file_option)

        pC.push_param(['generate_galaxy_xml', 'Generate Galaxy XML file',
                            {'hidden': True, 'validate': 'Flag',
                             '_show_in_galaxy': False}])
        pC.push_param(['galaxy', 'Run with galaxy-specific overrides',
                            {'hidden': True, 'validate': 'Flag',
                             '_galaxy_specific': True,
                             '_show_in_galaxy': False}])
        pC.push_param(['outfile_supporting', 'File or folder to output to',
                            {'hidden': True, 'validate': 'String', 'default':
                             '__new_file_path__', '_galaxy_specific': True,
                             '_show_in_galaxy': False}])
        self.pC = pC
        return pC

    def params(self):
        """Returns parameters, or prints help and exits if validation fails"""
        if self.pC.validate():
            return self.opt
        else:
            self.pC.argparser.print_help()
            sys.exit(2)

    def fix_outputs(self, outputs):
        """Internal function to parse specified outputs and munge them into standard options

        From a user perspective, they only specify a single output file and it
        is supposed to be handled magically. This function is a significant
        part of that magic.

        Internally, an output file is taken from being a simple object
        to four separate command line parameters, completely removed
        from the original description of the option. These four
        parameters are as follows for an example output file "of":

            - of: the file location as specified by the user (if
            specified at all, without extension)
            - of_format: the format of this file. Really only applies
            to the top level file, but it's up to the dev how to
            handle this value
            - of_files_path: the "of.files_path" value in the cheetah
            template galaxy uses. This location can be used for
            storing images or other data for use in HTML files.
            - of_id: the "of.id" value in the cheetah template, used
            in generation of the complex filenames that galaxy
            requires to pick up on associated files.

        There should be no need for the user to call this method.
        """
        fixed_outputs = {}

        getopt_formatted = []
        import copy

        for output in outputs:
            name = output[0]
            desc = output[1]
            opts = output[2]

            # Primary output file
            fixed_outputs[name] = {
                'description': desc,
                'options': copy.deepcopy(opts),
            }
            fixed_outputs[name]['options']['required'] = True
            getopt_formatted.append([name, desc, opts])

            # Files path (for varCRR)
            namefp = name + "_files_path"
            namefp_desc = 'Associated HTML files for ' + name
            fixed_outputs[namefp] = {
                'description': namefp_desc,
                'options': copy.deepcopy(opts),
            }

            fixed_outputs[namefp]['options']['hidden'] = True
            fixed_outputs[namefp]['options']['value'] = name + ".files_path"
            fixed_outputs[namefp]['options']['default'] = name + ".files_path"
            fixed_outputs[namefp]['options']['required'] = True
            fixed_outputs[namefp]['options']['_galaxy_specific'] = True
            fixed_outputs[namefp]['options']['_cheetah_var'] = True
            fixed_outputs[namefp]['options']['validate'] = "String"

            getopt_formatted.append([namefp,
                                     fixed_outputs[namefp]['description'],
                                     fixed_outputs[namefp]['options']])

            # Adds the {name}_format special parameter
            namefmt = name + "_format"
            namefmt_desc = 'Associated Format for ' + name
            fixed_outputs[namefmt] = {
                'description': namefmt_desc,
                'options': copy.deepcopy(opts),
            }

            fixed_outputs[namefmt]['options']['default'] = \
                opts['default_format']
            fixed_outputs[namefmt]['options']['required'] = True
            fixed_outputs[namefmt]['options']['validate'] = "File/OutputFormat"

            getopt_formatted.append([namefmt,
                                     fixed_outputs[namefmt]['description'],
                                     fixed_outputs[namefmt]['options']])

            # Adds the {name}_id special parameter
            nameid = name + "_id"
            nameid_desc = 'Associated ID Number for ' + name
            fixed_outputs[nameid] = {
                'description': nameid_desc,
                'options': copy.deepcopy(opts),
            }

            fixed_outputs[nameid]['options']['default'] = "${%s.id}" % (name,)
            fixed_outputs[nameid]['options']['value'] = "${%s.id}" % (name,)
            fixed_outputs[nameid]['options']['required'] = True
            fixed_outputs[nameid]['options']['hidden'] = True
            fixed_outputs[nameid]['options']['validate'] = "String"
            fixed_outputs[nameid]['options']['_galaxy_specific'] = True
            fixed_outputs[namefp]['options']['_cheetah_var'] = True

            getopt_formatted.append([nameid,
                                     fixed_outputs[nameid]['description'],
                                     fixed_outputs[nameid]['options']])
        self.registered_outputs = fixed_outputs
        return getopt_formatted
