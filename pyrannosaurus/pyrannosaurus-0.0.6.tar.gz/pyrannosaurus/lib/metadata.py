class Metadata(object):

    def __init__(self, name=None, obj_type=None):
        if name is not None:
            self.name = name.split(".", 1)[0]
            #self.obj_type = name.split(".", 1)[1]

    def __eq__(self, comp):
        return self.__dict__ == comp.__dict__

    def add_child(self, name, value=None):
        if value is None:
            value = []
        setattr(self, name, value)

    def add_property(self, name, value):
        setattr(self, name, value)
