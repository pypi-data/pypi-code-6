from django.conf.urls import patterns, url

from .views import flatpage, edit

urlpatterns = patterns('',
    url(r'^new/$', edit, name='new_flatpage'),
    url(r'^(?P<url>.*)edit/$', edit, name='edit_flatpage'),
    url(r'^(?P<url>.*)$', flatpage, name='flatpage'),
)
