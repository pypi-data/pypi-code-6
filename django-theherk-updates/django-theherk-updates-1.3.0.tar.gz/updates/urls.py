from django.conf.urls import *

urlpatterns = patterns(
    'updates.views',
    url(r'^$', 'index', name='index'),
)
