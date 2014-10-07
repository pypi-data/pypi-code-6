from parameter import Parameter
import xml.etree.cElementTree as ET
from galaxygetopt.outputfiles import OutputFiles


class FileOutput(Parameter):

    # # The format of the internal data structure that we're pushing to output
    # See CPT.pm for a list of these (under %acceptable)
    # has 'data_format' => ( is => 'rw', isa => 'Str' );
    # has 'default_format' => ( is => 'rw', isa => 'Str' );
    def __init__(self, name=None, short=None, multiple=False, description=None,
                 default=None, required=False, hidden=False, errors=[],
                 value=[], _galaxy_specific=False, _show_in_galaxy=True,
                 **kwargs):
        super( FileOutput, self ).__init__(name=name, short=short,
                                           multiple=multiple, description=description,
                                           default=default, required=required,
                                           hidden=hidden, errors=errors, value=value,
                                           _galaxy_specific=_galaxy_specific,
                                           _show_in_galaxy=_show_in_galaxy,
                 **kwargs)
        self._outputfile_data_access = OutputFiles()

    def data_format(self):
        if 'data_format' in self.child_params and self.child_params['data_format'] is not None:
            return self.child_params['data_format']
        else:
            return None

    def default_format(self):
        if 'default_format' in self.child_params and self.child_params['default_format'] is not None:
            return self.child_params['default_format']
        else:
            return None

    # options
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

        params = self.get_default_input_parameters('select')
        params['label'] = 'Format of %s' % (self.get_galaxy_cli_identifier())
        params['name'] = '%s_%s' % (self.get_galaxy_cli_identifier(), 'format')

        # Remove the value, if it is there
        try:
            del params['value']
        except KeyError:
            pass

        # Copy params over
        for key in params:
            node_of_interest.set(key, params[key])

        ## If we have a data format
        if self.data_format() is not None:
            # Get the list of output writers associated with that internal format
            for format_str in sorted(self._outputfile_data_access.valid_formats(self.data_format())):
                # And present them as options to the user
                option_node = ET.SubElement(node_of_interest, 'option')
                option_node.text = format_str
                option_node.set('value', format_str)
                if format_str == self.default_format():
                    option_node.set('selected', "True")

    def galaxy_output(self, xml_node):
        format_str = None
        if self.data_format() is not None:
            format_str = self.default_format()
        else:
            format_str = "data"

        node = ET.SubElement(xml_node, 'data')
        node.set('name', self.get_galaxy_cli_identifier())
        node.set('format', format_str)

        change_format = ET.SubElement(node, 'change_format')
        if self.data_format() is not None:
            for format_str in sorted(self._outputfile_data_access.valid_formats(self.data_format())):
                # And present them as options to the user
                option_node = ET.SubElement(change_format, 'when')
                option_node.set('input', '%s_%s' % (self.get_galaxy_cli_identifier(), 'format')),
                option_node.set('value', format_str)
                try:
                    option_node.set('format', self._outputfile_data_access.get_format_mapping(format_str))
                except:
                    option_node.set('format', 'data')

    def validate_individual(self, val):
        return True
