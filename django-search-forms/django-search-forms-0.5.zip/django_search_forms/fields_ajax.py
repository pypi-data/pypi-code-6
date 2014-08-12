"""The fields that depend on bob-ajax-select"""
try:
    from ajax_select.fields import (
        AutoCompleteSelectField,
        AutoCompleteField,
    )
except ImportError:
    raise ImportError("You need to install bob-ajax-select package")

from django.db.models import Q


class RelatedAjaxSearchField(AutoCompleteSelectField):
    """A field that enables lookup by related objects."""

    def __init__(self, *args, **kwargs):
        kwargs['required'] = False
        super(RelatedAjaxSearchField, self).__init__(*args, **kwargs)

    def clean(self, value):
        if value:
            return Q(**{self.name + '_id': value})
        else:
            return Q()


class AjaxTextSearch(AutoCompleteField):
    """
    A field that enables both:
        - search by text typed in,
        - search by value picked from lookup.
    """

    def __init__(self, filter_field='', *args, **kwargs):
        """
        :param filter_field: used to point fields' children (in model's
        relations)
        """
        kwargs['required'] = False
        self.filter_field = filter_field
        super(AjaxTextSearch, self).__init__(*args, **kwargs)

    def clean(self, value):
        if value:
            full_filter_field = self.name + self.filter_field
            exact = value.startswith('"') and value.endswith('"')
            if exact:
                value = value.replace('"', '')
            else:
                full_filter_field += '__icontains'
            query = Q(**{full_filter_field: value})
        else:
            query = Q()
        return query
