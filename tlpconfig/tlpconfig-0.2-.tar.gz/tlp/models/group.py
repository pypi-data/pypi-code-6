class Group:
    def __init__(self, name, parameters):
        self.name = name
        self.parameters = parameters

    @property
    def is_active(self):
        return not any(p for p in self.parameters.values()
                       if not p or not p.active)
    
    @is_active.setter
    def is_active(self, value):
        for parameter in self.parameters.values():
            parameter.active = value
