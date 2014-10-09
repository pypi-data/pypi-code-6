# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import SnippetPlugin
from .forms import SnippetForm


class Snippet(CMSPluginBase):
    name = _('Snippet')
    model = SnippetPlugin
    form = SnippetForm
    change_form_template = 'aldryn_snippet/admin/snippet_change_form.html'
    render_template = 'aldryn_snippet/snippet.html'

plugin_pool.register_plugin(Snippet)
