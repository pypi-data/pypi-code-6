from parameter import Parameter
import xml.etree.cElementTree as ET


class Flag(Parameter):

    # Method is overriden here ONLY because of the !required&&!not multiple
    # case,
    def galaxy_command(self):
        value = self.get_galaxy_command_identifier()
        if self.hidden and self._galaxy_specific:
            value = self.default

        # If a repeat, handle
        string = self.handle_possible_galaxy_command_repeat_start()
        # If it's required we set it to a value IF we have one. Otherwise value
        # will be the galaxy_identifier.
        if self.required:
            string += '--%s\n' % (self.get_galaxy_cli_identifier(), )
        else:
            if not self.multiple:
                string += '#if $%s:\n' % (self.get_galaxy_cli_identifier(),)

            string += '--%s\n' % (self.get_galaxy_cli_identifier(),)

            if not self.multiple:
                string += '#end if\n'
        string += self.handle_possible_galaxy_command_repeat_end()
        return string

    def galaxy_input(self, xml_node):
        node_of_interest = None
        # Due to differences between python/perl, what we do here is figure out
        # which node we actually want to be talking to (main node or the repeat
        # node within it). We can then work with a generic xml_node
        possible_repeat_node = self.handle_possible_galaxy_input_repeat_start(xml_node)
        if possible_repeat_node is not None:
            node_of_interest = ET.SubElement(possible_repeat_node, 'param')
        else:
            node_of_interest = ET.SubElement(xml_node, 'param')

        params = self.get_default_input_parameters('boolean')
        params['falsevalue'] = 'False'
        params['truevalue'] = 'True'
        if self.default:
            params['checked'] = 'True'
        else:
            params['checked'] = ''

        # Remove the value, if it is there
        try:
            del params['value']
        except KeyError:
            pass

        # Copy params over
        for key in params:
            node_of_interest.set(key, params[key])

    def galaxy_output(self, xml_node):
        return None

    def validate_individual(self, value):
        return True
