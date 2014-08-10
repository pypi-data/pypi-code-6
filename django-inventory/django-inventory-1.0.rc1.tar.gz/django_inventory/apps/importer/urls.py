from __future__ import absolute_import

from django.conf.urls import patterns, url

from .forms import PreviewForm, ExpressionForm, ImportWizard

urlpatterns = patterns('importer.views',
    url(r'^upload/$', 'import_file', name='import_wizard'),
    url(r'^wizard/$', 'import_wizard', name='import_next_steps'),
    url(r'^download_last_settings/$', 'download_last_settings', name='download_last_settings'),
)


