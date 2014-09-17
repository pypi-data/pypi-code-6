from itertools import groupby

from django import template

from .. import settings


register = template.Library()


@register.assignment_tag
def organize_settings_formset(formset, *args):
    '''
    Group the settings form into groups and re-order them according to what is
    defined at SETMAGIC_SCHEMA.
    '''
    form_map = dict((f.instance.name, f) for f in formset.forms)
    return [
        (group_label, [form_map[d['name']] for d in defs])
        for group_label, defs in groupby(
            settings.defs.values(), lambda d: d['group_label'])
    ]
