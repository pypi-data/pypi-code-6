from django.forms.forms import Form
from django.forms.models import ModelForm


class OptionsBase(object):
    def __init__(self, options):
        if options != {}:
            raise TypeError('Unknown options for {0}: {1}'.format(
                self.__class__.__name__, ', '.join(options.keys())))


def options_factory(options_processor, options_class_name=None,
                    options_attr_name=None, metaclass=type):

    if options_class_name is None:
        options_class_name = options_processor.__name__
    if options_attr_name is None:
        options_attr_name = '_' + options_class_name.lower()

    class OptionsMetaclass(metaclass):
        def __new__(mc, name, bases, attrs):
            if options_class_name in attrs:
                options_attr = attrs.pop(options_class_name)
                options = dict(
                    (key, value)
                    for key, value in options_attr.__dict__.items()
                    if key[0] != '_')
                attrs[options_attr_name] = options_processor(options)

            # print 'Calling super({0}, {1}).__new__({1}, {2}, {3}, {4})'.format(
                # new_metaclass, mc, name, bases, attrs)
            return super(OptionsMetaclass, mc).__new__(mc, name, bases, attrs)

    OptionsMetaclass.__name__ = options_class_name + 'Metaclass'
    return OptionsMetaclass


def form_options_factory(*args, **kwargs):
    return options_factory(*args, metaclass=type(Form), **kwargs)


def modelform_options_factory(*args, **kwargs):
    return options_factory(*args, metaclass=type(ModelForm), **kwargs)
