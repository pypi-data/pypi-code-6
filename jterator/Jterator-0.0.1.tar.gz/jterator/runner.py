import os
import json
from jterator.error import JteratorError
from jterator.module import Module
from jterator.minify_json import json_minify as clean_json


PIPE_FILENAMES = ['JteratorPipe.json', 'jt.pipe']


class JteratorRunner(object):

    def __init__(self, pipeline_folder_path):
        self.pipeline_folder_path = pipeline_folder_path
        self.modules = list()
        self.__description = None
        self.pipeline_filepath = None

    @property
    def logs_path(self):
        return os.path.join(self.pipeline_folder_path, 'logs')

    def read_json(self, json_filepath):
        json_data = open(json_filepath).read()
        try:
            json_data = clean_json(json_data, strip_space=False)
            return json.loads(json_data)
        except ValueError as json_error:
            linelabeled_json = '\n'.join(['%i: %s' % (index, line)
                                          for index, line
                                          in enumerate(json_data.split('\n'))])
            raise JteratorError('JSON description of the pipeline (%s) '
                                'contains an error:\n%s\n%s\n%s' %
                                (self.pipeline_filepath, str(json_error),
                                 '='*80, linelabeled_json))

    def locate_pipeline_filepath(self):
        '''Detect filepath to pipeline description if found.'''
        # Where is the pipeline description file?
        if not self.pipeline_filepath is None:
            return
        for pipe_filename in PIPE_FILENAMES:
            pipeline_filepath = os.path.join(self.pipeline_folder_path,
                                             pipe_filename)
            if os.path.exists(pipeline_filepath):
                self.pipeline_filepath = pipeline_filepath
                break
        # Still not found?
        if self.pipeline_filepath is None:
            raise JteratorError('Failed to load pipeline description. '
                                'Make sure to put one of the files "%s"'
                                ' into your pipeline path: %s' %
                                (PIPE_FILENAMES, self.pipeline_folder_path))

    @property
    def description(self):
        if self.__description is None:
            self.locate_pipeline_filepath()
            # Read and parse JSON.
            # TODO: perform expected JSON schema validation.
            self.__description = self.read_json(self.pipeline_filepath)

        return self.__description

    def build_pipeline(self):
        '''Build pipeline from JSON description.'''
        for module_description in self.description['pipeline']:
            executable_path = os.path.join(
                self.pipeline_folder_path,
                'modules',
                module_description['module'],
            )
            handles_filepath = os.path.join(
                self.pipeline_folder_path,
                module_description['handles'],
            )
            if not os.path.exists(executable_path):
                raise JteratorError('Missing module executable: %s' %
                                    executable_path)
            module = Module(
                name=module_description['name'],
                executable_path=executable_path,
                handles=open(handles_filepath),
            )
            self.modules.append(module)
        if not self.modules:
            raise JteratorError('Not a single module description was found in:'
                                ' %s' % self.pipeline_filepath)

    def run_pipeline(self):
        '''Run modules one after another, pass handles to each of them'''
        for module in self.modules:
            module.set_error_output(os.path.join(self.logs_path,
                                    '%s.error' % module.name))
            module.set_standard_output(os.path.join(self.logs_path,
                                       '%s.output' % module.name))
            module.run()
