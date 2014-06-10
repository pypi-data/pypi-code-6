"""
"""
__version__ = '0.3.1'

__all__ = [
    'NOT_SET',
    'NONE',
    'ERROR',
    'IGNORE',
    'source',
    'Source',
    'SourceError',
    'DefaultPath',
    'DefaultSource',
    'fields',
    'Field',
    'FieldError',
    'Form',
]

import inspect


class _Constant(object):

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '{0}("{1}")'.format(type(self).__name__, self.name)


NOT_SET = _Constant('NOT_SET')

NONE = _Constant('NONE')

ERROR = _Constant('ERROR')

IGNORE = (NONE, ERROR, NOT_SET)


class Types(dict):
    """
    """

    @classmethod
    def map(cls, field):

        def _map(form_cls):
            if not inspect.isabstract(object):
                try:
                    value = getattr(form_cls(), field.name)
                    identities[value] = form_cls
                except AttributeError:
                    pass
            for sub_cls in form_cls.__subclasses__():
                _map(sub_cls)

        if not isinstance(field, Field):
            raise TypeError('Excepted field')

        if not field.is_attached:
            raise ValueError('{0} is not attached'.format(field))

        identities = cls.for_field(field)
        _map(field.parent)
        return identities

    @classmethod
    def for_field(cls, type_field):
        fields = {}
        for field in type_field.parent.fields:
            fields[field.name] = type(field)(field.src, default=None)
            if field is type_field:
                break
        else:
            raise ValueError(
                'No {0} in {1}'.format(type_field, type_field.parent)
            )
        type_form = type('TypeProbe', (Form,), fields)
        return cls(type_form, type_field)

    def __init__(self, type_form, type_field):
        self.type_form = type_form
        self.type_field = type_field

    def __getitem__(self, key):
        return dict.__getitem__(self, key)

    def probe(self, src, default=NONE):
        probe = self.type_form()
        errors = probe.map(src)
        if not errors:
            return getattr(probe, self.type_field.name)
        if default in IGNORE:
            raise errors[0]
        return default


from . import source
from .source import Source, SourceError, DefaultPath, DefaultSource
from .context import ctx, ContextMixin, Close
from . import fields
from .fields import Field, FieldError, Form
