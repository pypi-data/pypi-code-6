from jinja2 import Template
import sys


class Parameters:
    def __init__(self, parameters=None):
        """ @type parameters: dict """
        self._parameters = parameters if parameters else {}

    def set(self, key, value):
        self._parameters[key] = value

    def parse_text(self, text):
        # python 2-3 compatibility
        try:
            text_type = (str, unicode)
        except NameError:  # pragma: no cover
            text_type = str

        if not isinstance(text, text_type):
            return text
        template = Template(text)
        resolved_text = template.render(self._parameters)
        if resolved_text == text:
            resolved_text = resolved_text.replace("\\{", "{")
            resolved_text = resolved_text.replace("\\}", "}")
            return resolved_text
        else:
            return self.parse_text(resolved_text)

    def get(self, key, default=None):
        """ @type key: str """
        if key not in self._parameters:
            return default

        value = self._parameters[key]

        return self.parse_text(value)

    def has(self, key):
        """ @type key: str """
        return key in self._parameters

    def remove(self, key):
        """ @type key: str """
        del self._parameters[key]

    def add(self, parameters):
        """ @type parameters: dict """
        self._parameters = dict(list(self._parameters.items()) + list(parameters.items()))

    def all(self):
        return self._parameters

    def count(self):
        return len(self._parameters)

    def keys(self):
        return list(self._parameters.keys())





class Services:
    def __init__(self, definitions=None, parameters=None):
        """
        @type definitions: dict
        @type parameters: Parameters
        """
        self._services = {}
        self._definitions = definitions if definitions else {}
        self._parameters = parameters if parameters else Parameters()

    def set(self, key, value):
        self._services[key] = value

    def get(self, name):
        if name in self._services:
            return self._services[name]

        if name not in self._definitions:
            raise ServicesException('Service \'%s\' not found.' % name)

        return self._build_service(name)

    def has(self, key):
        """ @type key: str """
        return key in self._definitions or key in self._services

    def remove(self, key):
        """ @type key: str """
        if key in self._services:
            del self._services[key]
        if key in self._definitions:
            del self._definitions[key]

    def add(self, services):
        """ @type services: dict """
        self._services = dict(list(self._services.items()) + list(services.items()))

    def keys(self):
        definitions_keys = self._definitions.keys()
        services_keys = self._services.keys()
        return set(list(definitions_keys) + list(services_keys))

    def _build_service(self, definition_name):
        definition = self._definitions[definition_name]
        if isinstance(definition, str):
            return self._resolve_container_key(definition)
        if 'class' not in definition:
            raise ServicesException('\'%s\' definition has no attribute \'class\'' % definition_name)

        module_name, class_name = definition['class'].rsplit('.', 1)
        __import__(module_name)
        module = sys.modules[module_name]
        service_class = getattr(module, class_name)
        if 'arguments' in definition:
            arguments = definition['arguments']
            if isinstance(arguments, dict):
                # python 2-3 compatibility
                try:
                    arguments_iteritems = arguments.iteritems()
                except AttributeError:  # pragma: no cover
                    arguments_iteritems = arguments.items()

                for argument_key, argument_value in arguments_iteritems:
                    arguments[argument_key] = self._resolve_container_key(argument_value)
                service_object = service_class(**arguments)
            elif isinstance(arguments, list):
                resolved_arguments = []
                for argument in arguments:
                    resolved_arguments.append(self._resolve_container_key(argument))
                service_object = service_class(*resolved_arguments)
            else:
                raise ServicesException('Invalid arguments type \'%s\', for \'%s\' definition, use dict or tuple.' % (type(definition['arguments']), definition_name))
        else:
            service_object = service_class()

        if 'calls' in definition:
            for call in definition['calls']:
                if isinstance(call, str):
                    resolved_argument = self._resolve_container_key(call)
                    self._validate_call_in_service(service_object, resolved_argument, definition_name)
                    getattr(service_object, call)()
                elif isinstance(call[1], list):
                    resolved_arguments = []
                    for argument in call[1]:
                        resolved_arguments.append(self._resolve_container_key(argument))
                    self._validate_call_in_service(service_object, call[0], definition_name)
                    getattr(service_object, call[0], lambda: None)(*resolved_arguments)
                elif isinstance(call[1], dict):
                    resolved_arguments = {}

                    # python 2-3 compatibility
                    try:
                        call_iteritems = call[1].iteritems()
                    except AttributeError:  # pragma: no cover
                        call_iteritems = call[1].items()

                    for argument_key, argument_value in call_iteritems:
                        resolved_arguments[argument_key] = self._resolve_container_key(argument_value)
                    self._validate_call_in_service(service_object, call[0], definition_name)
                    getattr(service_object, call[0], lambda: None)(**resolved_arguments)
                else:
                    raise ServicesException('Invalid call type \'%s\', for \'%s\' definition, use str (for no args), or list or dict (for args)' % (type(call), definition_name))

        self._services[definition_name] = service_object
        return self._services[definition_name]

    @staticmethod
    def _validate_call_in_service(service_object, function_name, definition_name):
        if not hasattr(service_object, function_name):
            raise ServicesException('Invalid call function \'%s\' for \'%s\' definition' % (function_name, definition_name))

    def _resolve_container_key(self, key):
        key = self._parameters.parse_text(key)

        # python 2-3 compatibility
        try:
            text_type = (str, unicode)
        except NameError:  # pragma: no cover
            text_type = str

        if isinstance(key, text_type) and len(key) >= 2 and key[0] == '@':
            key = key[1:]
            if key[0] == '@':
                return key
            else:
                return self.get(key)
        else:
            return key


class ServicesException(Exception):
    pass