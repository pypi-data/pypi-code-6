import copy

from django import forms
from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape, format_html

class ContentEditableTextInput(forms.HiddenInput):
    '''
    Requires content.js
    '''
    def render(self, name, value, attrs=None):
        template_string = u'<span id="id_contenteditable_{name}" class="drift editable textinput" contenteditable="true" data-target="{id}" data-default="{name}">{value}</span>'
        kwargs = copy.deepcopy(attrs)
        kwargs['name'] = name
        kwargs['value'] = value

        return format_html(template_string, **kwargs) + super(ContentEditableTextInput, self).render(name, value, attrs)


class ContentDateInput(forms.DateInput):
    def __init__(self, attrs=None):
        default_attrs = {
            'class': 'content_datefield',
            'data-date-format': 'yyyy-mm-dd',
        }
        if attrs:
            default_attrs.update(attrs)
        super(ContentDateInput, self).__init__(default_attrs)

    def render(self, name, value, attrs=None):
        if 'placeholder' not in attrs:
            attrs['placeholder'] = name
        return super(ContentDateInput, self).render(name, value, attrs)




