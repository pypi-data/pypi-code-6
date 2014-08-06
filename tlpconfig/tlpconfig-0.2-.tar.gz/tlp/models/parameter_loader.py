from .parameter import (TextParameter, BooleanParameter,
                        ListParameter, NumericParameter)
from .group import Group
from json import loads


class ParameterLoader():
    def load_categories(self, categories_file):
        with open(categories_file) as config:
            categories = loads(config.read())

        return {category['category']: self._load_groups(category['groups'])
                for category in categories}

    def _load_groups(self, groups):
        return [Group(group['name'], self._load_params(group['parameters']))
                for group in groups]

    def _load_params(self, parameters):
        factory = ParameterFactory()
        return {param['name']: factory.create(param) for param in parameters}


class ParameterFactory():
    def __init__(self):
        self.types = {"text": self._create_text_parameter,
                      "numeric": self._create_numeric_parameter,
                      "list": self._create_list_parameter,
                      "boolean": self._create_boolean_parameter}

    def create(self, data):
        create_parameter = self.types[data['type']]
        return create_parameter(data)
            
    def _create_text_parameter(self, data):
        if data.get('quotes'):
            return TextParameter(data['name'], quotes=data['quotes'])

        return TextParameter(data['name'])

    def _create_boolean_parameter(self, data):
        if data.get('yes') and data.get('no'):
            return BooleanParameter(data['name'],
                                    yes=data['yes'],
                                    no=data['no'])

        return BooleanParameter(data['name'])

    def _create_list_parameter(self, data):
        return ListParameter(data['name'])

    def _create_numeric_parameter(self, data):
        return NumericParameter(data['name'])
