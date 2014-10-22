from django.conf.urls import patterns, include, url
from oak import Hub

urlpatterns = patterns('', )
urlpatterns += Hub().get_urls()