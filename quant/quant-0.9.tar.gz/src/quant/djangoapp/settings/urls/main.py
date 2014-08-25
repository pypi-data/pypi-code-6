from django.conf.urls.defaults import *
from quant.soleInstance import application
from quant.dictionarywords import URI_PREFIX

uriPrefix = application.dictionary[URI_PREFIX]

if uriPrefix:
    uriPrefix = uriPrefix.lstrip('/')
    uriPrefix = uriPrefix + '/'

urlpatterns = patterns('',
    (
        r'^%s' % uriPrefix, include('quant.django.settings.urls.eui')
    ),
)

