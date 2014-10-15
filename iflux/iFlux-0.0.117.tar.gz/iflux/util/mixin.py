""" This code is based on:
http://code.activestate.com/recipes/577824-mixins-by-inheritance-vs-by-decoratorlets-try-deco/
"""


def add_mixin(cls, mixin, force=False):
    """Adds public attributes from a mixin to a class.
    """
    for name, value in mixin.__dict__.items():
        if name.startswith("_"):
            continue
        if not force and hasattr(cls, name):
            raise TypeError("name collision ({})".format(name))
        setattr(cls, name, value)
    try:
        mixin.register(cls)
    except AttributeError:
        pass


def mixes_in(*mixins, **parameters):
    """Decorator that receives a list of mixins and adds each mixin to the
    provided decorated class using add_mixin function.
    """
    def wrapper(cls):
        force = parameters.get('force') if parameters.has_key('force') \
            else False
        for mixin in mixins:
            add_mixin(cls, mixin, force)
        return cls
    return wrapper

