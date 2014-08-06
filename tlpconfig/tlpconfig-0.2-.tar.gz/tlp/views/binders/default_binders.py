class BooleanParameterBinder:
    def __init__(self, parameter):
        self.parameter = parameter

    def get_value_from(self, control):
        return control.get_active()

    def set_value_to(self, control):
        control.set_active(self.parameter.value)

class NumericParameterBinder:
    def __init__(self, parameter):
        self.parameter = parameter

    def get_value_from(self, control):
        return control.get_value()

    def set_value_to(self, control):
        control.set_value(self.parameter.value)

class TextParameterBinder:
    def __init__(self, parameter):
        self.parameter = parameter

    def get_value_from(self, control):
        return control.get_active_id()

    def set_value_to(self, control):
        control.set_active_id(self.parameter.value)

class ListParameterBinder:
    def __init__(self, parameter):
        self.parameter = parameter

    def get_value_from(self, control):
        return [child.get_name() 
                for child in control.get_children() 
                if child.get_active()]

    def set_value_to(self, control):
        values = self.parameter.value
        for child in control.get_children():
            child.set_active(child.get_name() in values)
