from django.conf.urls import patterns, url
from .views import *

urlpatterns = patterns(
    "prototyper.urls",
    url(r'^awesomesauce/$', Awesomesauce.as_view(), name='awesomesauce'),
    url(r'^awesomesauce/$', Awesomesauce.as_view(), name='awesomesauce'),
    url(r'^awesomesauce/$', Awesomesauce.as_view(), name='awesomesauce'),
)
