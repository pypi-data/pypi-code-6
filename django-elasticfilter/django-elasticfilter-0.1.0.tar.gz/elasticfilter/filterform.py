import six

from django import forms
from elasticutils import S

from .fields import BaseField


class FilterFormOptions(object):
    def __init__(self, name, options):

        self.s = options.pop('s', S())

        if options != {}:
            raise NameError("Unknown option {0} in {1}.FilterFormMeta".format(
                ', '.join(options.keys()), name))


class FilterFormMetaclass(type(forms.Form)):
    def __new__(mcs, name, bases, attrs):
        if 'FilterFormMeta' in attrs:
            options_attr = attrs.pop('FilterFormMeta')
            options = dict((key, value)
                           for key, value in options_attr.__dict__.items()
                           if key[0] != '_')
            attrs['_filterformmeta'] = FilterFormOptions(name, options)

        return super(FilterFormMetaclass, mcs).__new__(mcs, name, bases, attrs)


class FilterFormBase(forms.Form):

    def __init__(self, data=None, files=None, s=None, **kwargs):
        super(FilterFormBase, self).__init__(data=data, files=files, **kwargs)

        self.s = s or self._filterformmeta.s

    def search(self):
        if not self.is_valid():
            raise ValueError('Can not search with invalid data')

        s = self.s
        cleaned_data = self.cleaned_data

        for name, field in self.get_filter_fields():
            s = field.search(s, name, cleaned_data)

        return s

    def get_filter_fields(self):
        for (name, field) in self.fields.items():
            if isinstance(field, BaseField):
                yield (name, field)


class FilterForm(six.with_metaclass(FilterFormMetaclass, FilterFormBase)):
    pass
