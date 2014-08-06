from .parameter_loader import ParameterLoader
from .parameter import Parameter
from functools import reduce
from itertools import chain
from .. import DATA_PATH
import re


class Configuration:
    def __init__(self, file_path):
        self.file_path = file_path
    
    def load(self):
        configs = self._get_parameters_from_config()
        categories = ParameterLoader().load_categories(DATA_PATH + 'categories.json')
        parameters = chain.from_iterable(group.parameters.values()
                                         for groups in categories.values()
                                         for group in groups)

        for parameter in parameters:
            self._set_param_state(parameter, configs.get(parameter.name)) 
        
        return categories

    def _get_parameters_from_config(self):
        regex = re.compile('^([A-Z]|_|[0-9]|#)*=.*')
        with open(self.file_path) as config_file:
            self.text = config_file.read()
            get_name = lambda text: text.split('=')[0].replace('#', '')
            return {get_name(row): row 
                    for row in self.text.splitlines() 
                    if regex.match(row)}

    def _set_param_state(self, parameter, text):
        values = text.split('=')
        initial_state = {'active' : not text.startswith('#'),
                         'value' : values[1].replace('"', '')}

        parameter.initial_state = initial_state
        parameter.active = initial_state['active']
        parameter._value = initial_state['value']

    def save_as(self, parameters, file_path):
        self.file_path = file_path
        self.save(parameters)

    def save(self, parameters):
        with open(self.file_path, 'w') as config_file:
            text = reduce(lambda text, param: param.write(text),
                          [param for param in parameters if param.is_changed()],
                          self.text)
            config_file.write(text)

        self.load()
