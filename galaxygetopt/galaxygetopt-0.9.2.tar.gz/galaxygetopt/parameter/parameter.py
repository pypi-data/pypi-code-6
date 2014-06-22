#!/usr/bin/env python
import xml.etree.cElementTree as ET
from ..exceptions import RepeatRequestedFromNonMultiple


class Parameter(object):

    def __init__(self, name=None, short=None, multiple=False, description=None,
                 default=None, required=False, hidden=False, errors=[],
                 value=[], _galaxy_specific=False, _show_in_galaxy=True,
                 _cheetah_var=False, **kwargs):
        self.name = name
        self.short = short
        self.multiple = multiple
        self.description = description

        # TODO: Not under test
        # Coerce non list values passed to this function into lists
        if self.multiple:
            if default is not None:
                if isinstance(default, list):
                    self.default = default
                else:
                    self.default = [default]
            else:
                self.default = []
        else:
            self.default = default
        self.required = required
        self.hidden = hidden
        self.errors = errors
        self.value = value

        self._galaxy_specific = _galaxy_specific
        self._show_in_galaxy = _show_in_galaxy
        self._cheetah_var = _cheetah_var
        # Some children will have other parameters, store them here
        self.child_params = {}
        for key in kwargs.keys():
            self.child_params[key] = kwargs[key]

    def galaxy_command(self):
        value = self.get_galaxy_command_identifier()
        # If it's specific to galaxy AND hidden from the user, then we should
        # set the value as the default. I cannot imagine a _galaxy_specific
        # !hidden situation, but we'll leave as-is in case
        if self.hidden and self._galaxy_specific:
            if self._cheetah_var:
                value = '"${%s}"' % (self.get_default(), )
            else:
                value = '"' + str(self.get_default()) + '"'
        else:
            value = '"${%s}"' % (value, )

        # If a repeat, handle
        string = self.handle_possible_galaxy_command_repeat_start()
        # If it's required we set it to a value IF we have one. Otherwise value
        # will be the galaxy_identifier.
        if self.required  or self._galaxy_specific:
            string += '--%s %s\n' % (self.get_galaxy_cli_identifier(),
                                          value)
        else:
            if not self.multiple:
                string += '#if $%s and $%s is not "None":\n' % \
                    (self.get_galaxy_cli_identifier(),
                     self.get_galaxy_cli_identifier())
            string += '--%s %s\n' % (self.get_galaxy_cli_identifier(),
                                          value)


            if not self.multiple:
                string += '#end if\n'
        string += self.handle_possible_galaxy_command_repeat_end()
        return string

    def get_galaxy_command_identifier(self):
        if self.multiple:
            return "%s.%s" % (self.get_repeat_idx_name(),
                              self.get_galaxy_cli_identifier())
        else:
            return self.get_galaxy_cli_identifier()

    def get_galaxy_cli_identifier(self):
        return self.name

    def get_value(self):
        if self.value is not None:
            if self.multiple:
                if len(self.value) > 0:
                    return self.value[0]
                else:
                    return None
            else:
                return self.value
        else:
            return None

    def get_default(self):
        # If there's a value
        if self.default is not None:
            # If it's multiple
            if self.multiple:
                # If there's more than one value, return the first
                if len(self.default) > 0:
                    return self.default[0]
                else:
                    return None
            else:
                # Otherwise just return the value
                return self.default
        else:
            return None

    def validate(self, possible_value):
        self.errors = []
        if self.multiple:
            if possible_value is not None and isinstance(possible_value, list):
                for val in possible_value:
                    self.validate_individual(val)
            elif possible_value is not None:
                self.validate_individual(possible_value)
            else:
                # If possible_value is none AND it's required, then throw an error
                if self.required:
                    self.errors.append("Must specify a value")
        else:
            self.validate_individual(possible_value)

        if len(self.errors) == 0:
            return True
        else:
            for error in self.errors:
                print "ERROR [%s] %s" % (self.get_galaxy_cli_identifier(), error)
            return False

    def get_repeat_idx_name(self):
        return 'item'

    def get_repeat_name(self):
        if self.multiple:
            return "repeat_%s" % (self.get_galaxy_cli_identifier(),)
        else:
            raise RepeatRequestedFromNonMultiple("Tried to get repeat name for non-multiple item")

    def handle_possible_galaxy_input_repeat_start(self, xml_node):
        if self.multiple:
            repeat_node = ET.SubElement(xml_node, 'repeat')
            repeat_node.set('name', self.get_repeat_name())
            # In perl, we converted this to title case?
            # $title =~ s/(\w+)/\u\L$1/g;
            repeat_node.set('title', self.get_galaxy_cli_identifier().title().replace('_',' '))
            return repeat_node
        else:
            return None

    def handle_possible_galaxy_command_repeat_start(self):
        if self.multiple:
            return "#for $%s in $%s:\n" % (self.get_repeat_idx_name(),
                                           self.get_repeat_name())
        else:
            return ''

    def handle_possible_galaxy_command_repeat_end(self):
        if self.multiple:
            return "#end for\n"
        else:
            return ''

    def get_default_input_parameters(self, paramType):
        params = {
            'name': self.get_galaxy_cli_identifier(),
            'optional': self.is_optional_galaxy(),
            'label': self.get_galaxy_cli_identifier(),
            'help': self.get_description(),
            'type': paramType,
        }

        if self.get_default() is not None:
            params['value'] = self.get_default()

            # Make sure it's not None as ET cannot serialize NoneTypes
            if params['value'] is None:
                params['value'] = ""

            if type(params['value']) is not str:
                params['value'] = str(params['value'])

        return params

    def get_description(self):
        if self.description is not None:
            return self.description
        else:
            return "Author failed to supply a description"

    def get_all_keys(self):
        kd = {}
        if self.name is not None:
            kd['name'] = self.name
        if self.short is not None:
            kd['short'] = self.short
        if self.multiple is not None:
            kd['multiple'] = self.multiple
        if self.description is not None:
            kd['description'] = self.description
        if self.default is not None:
            kd['default'] = self.default
        if self.required is not None:
            kd['required'] = self.required
        if self.hidden is not None:
            kd['hidden'] = self.hidden
        if self.errors is not None:
            kd['errors'] = self.errors
        if self.value is not None:
            kd['value'] = self.value
        for p in self.child_params:
            kd[p] = self.child_params[p]
        return kd

    # "requires"
    def is_optional_galaxy(self):
        if self.required:
            return "False"
        else:
            return "True"

    # These all are implemented by children
    def validate_individual(self, value):
        return True

    def galaxy_input(self):
        return None

    def galaxy_output(self):
        return None
