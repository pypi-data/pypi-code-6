class FreeTextParameterBinder:
    def __init__(self, parameter):
        self.parameter = parameter

    def get_value_from(self, control):
        return control.get_text()

    def set_value_to(self, control):
        control.set_text(self.parameter.value)
