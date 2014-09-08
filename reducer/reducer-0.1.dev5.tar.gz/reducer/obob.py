def obo(self):
    return ": ".join([str(self.description), str(self.value)])


def gobber(cls):
    from copy import copy
    new_instance = copy(cls)
    cls_type = type(cls)
    new_cls = type(cls_type.__name__, (cls_type,), {'__str__': obo})
    new_instance.__class__ = new_cls
    return new_instance
