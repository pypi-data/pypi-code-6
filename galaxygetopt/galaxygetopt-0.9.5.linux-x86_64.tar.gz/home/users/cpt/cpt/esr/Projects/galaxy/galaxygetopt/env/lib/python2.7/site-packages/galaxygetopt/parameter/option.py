from parameter import Parameter
import xml.etree.cElementTree as ET


class Option(Parameter):

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

        if 'min' in self.child_params and self.child_params['min'] is not None:
            params['min'] = str(self.child_params['min'])
        if 'max' in self.child_params and self.child_params['max'] is not None:
            params['max'] = str(self.child_params['max'])

        # Copy params over
        for key in params:
            node_of_interest.set(key, params[key])

        for key in sorted(self.child_params['options']):
            subnode = ET.SubElement(node_of_interest, 'option')
            subnode.set('value', key)
            if self.default == key:
                subnode.set('selected', 'True')
            subnode.text = self.child_params['options'][key]

    def galaxy_output(self, xml_node):
        return None

    def validate_individual(self, val):
        if self.required:
            if val in self.child_params['options']:
                return True
            else:
                self.errors.append("Unknown value [%s] applied to option %s" %
                                (val, self.name))
                return False
        else:
            if val is not None and val not in self.child_params['options']:
                return False
            else:
                return True
