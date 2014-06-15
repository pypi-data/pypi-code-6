from django.conf.urls import patterns, url
from lisa.plugins.TestPlugin.web import views

urlpatterns = patterns('',
    url(r'^$',views.index),
)
