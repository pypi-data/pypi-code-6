from parameter import Parameter


class Empty(Parameter):

    def galaxy_input(self, xml_node):
        return None

    def galaxy_output(self, xml_node):
        return None

    def validate_individual(self, value):
        return True
