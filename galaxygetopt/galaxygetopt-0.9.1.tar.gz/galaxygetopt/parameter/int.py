from parameter import Parameter
import xml.etree.cElementTree as ET


class Int(Parameter):

    # Min, Max
    def galaxy_input(self, xml_node):
        node_of_interest = None
        # Due to differences between python/perl, what we do here is figure out
        # which node we actually want to be talking to (main node or the repeat
        # node within it). We can then work with a generic xml_node
        possible_repeat_node = \
            self.handle_possible_galaxy_input_repeat_start(xml_node)
        if possible_repeat_node is not None:
            node_of_interest = ET.SubElement(possible_repeat_node, 'param')
        else:
            node_of_interest = ET.SubElement(xml_node, 'param')

        params = self.get_default_input_parameters('integer')
        if 'min' in self.child_params and self.child_params['min'] is not None:
            params['min'] = str(self.child_params['min'])
        if 'max' in self.child_params and self.child_params['max'] is not None:
            params['max'] = str(self.child_params['max'])

        # Copy params over
        for key in params:
            node_of_interest.set(key, params[key])

    def galaxy_output(self, xml_node):
        return None

    def validate_individual(self, val):
        try:
            int(val)

            if 'max' in self.child_params and self.child_params['max'] \
                    is not None:
                if val > self.child_params['max']:
                    self.errors.append('Value passed with %s was greater' +
                                       'than the allowable upper bound. ' +
                                       '[%s > %s]'
                                       % (self.name, val,
                                          self.child_params['max']))
                    return False
            if 'min' in self.child_params and self.child_params['min'] \
                    is not None:
                if val < self.child_params['min']:
                    self.errors.append('Value passed with %s was less' +
                                       'than the allowable minimum bound.'
                                       + '[%s > %s]'
                                       % (self.name, val,
                                          self.child_params['min']))
                    return False
        except ValueError:
            self.errors.append("Not an int")
            return False
        return True
