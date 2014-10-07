from parameter import Parameter
import xml.etree.cElementTree as ET


class FileInput(Parameter):

    # has 'format'      => ( is => 'rw', isa => 'Str' );
    # has 'file_format' => ( is => 'rw', isa => 'ArrayRef' );

    # options
    def galaxy_input(self, xml_node):
        node_of_interest = None
        possible_repeat_node = self.handle_possible_galaxy_input_repeat_start(xml_node)
        if possible_repeat_node is not None:
            node_of_interest = ET.SubElement(possible_repeat_node, 'param')
        else:
            node_of_interest = ET.SubElement(xml_node, 'param')

        params = self.get_default_input_parameters('data')

        if 'file_format' in self.child_params and self.child_params['file_format'] is not None:
            params['format'] = ','.join(self.child_params['file_format'])

        # Copy params over
        for key in params:
            node_of_interest.set(key, params[key])

    def galaxy_output(self, xml_node):
        return None

    def validate_individual(self, val):
        return True
