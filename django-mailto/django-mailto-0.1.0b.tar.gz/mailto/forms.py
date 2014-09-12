# -*- coding: utf-8 -*-
from django import forms
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from mailto.models import Mail


class MailAdminForm(forms.ModelForm):
    model = Mail

    def __init__(self, *args, **kwargs):
        super(MailAdminForm, self).__init__(*args, **kwargs)

        instance = kwargs.get('instance')
        if instance:
            html_widget = EditHTMLInlineWidget(instance.id)
        else:
            html_widget = EditHTMLInlineWidget()
        self.fields['html'].widget = html_widget


class EditHTMLInlineWidget(forms.Widget):
    url = None

    def __init__(self, pk=None, attrs={}):
        if not pk:
            self.url = reverse('new-html')
        else:
            self.url = reverse('edit-html', kwargs={'pk': pk})
        super(EditHTMLInlineWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        return mark_safe('<input type="hidden" name="%s" /><iframe id="%s" src="%s"></iframe>' % (name, name, self.url))