from django.conf.urls import patterns, include, url

from SEEmpty import views

urlpatterns = patterns('',
    url(r'^index/$', views.index, name='index'),
)
