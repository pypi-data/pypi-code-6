import copy

from django import forms
from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape, format_html


class DriftBootstrapWYSIWYGEditor(object):
    def get_textarea_widget(self):
        return BootstrapWYSIWYGTextArea


class BootstrapWYSIWYGTextArea(forms.Textarea):
    def render(self, name, value, attrs=None):
        template_string = u'''
<div class="btn-toolbar" data-role="editor-toolbar" data-target="#editor">
      <div class="btn-group">
        <a class="btn" data-edit="bold" title="" data-original-title="Bold (Ctrl/Cmd+B)">Bold</a>
        <a class="btn" data-edit="italic" title="" data-original-title="Italic (Ctrl/Cmd+I)">Italics</a>
      </div>
    </div>
<div id="id_contenteditable_{name}" class="drift editable wysiwyg textarea" data-target="{id}" data-default="{name}">{value}</div>
'''

        kwargs = copy.deepcopy(attrs)
        kwargs['name'] = name
        kwargs['value'] = mark_safe(value)

        return format_html(template_string, **kwargs) + super(BootstrapWYSIWYGTextArea, self).render(name, value, attrs)
