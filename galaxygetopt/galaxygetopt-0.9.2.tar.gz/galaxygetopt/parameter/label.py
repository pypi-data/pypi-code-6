from parameter import Parameter


class Label(Parameter):

    def galaxy_input(self, xml_node):
        return None

    def galaxy_output(self, xml_node):
        return None

    def validate_individual(self, value):
        return True
