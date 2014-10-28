from django.conf.urls import patterns, url, include

from .views import HookView

urlpatterns = patterns('',
    url(r'^(?P<token>[\w-]+)/(?P<identifier>[\w-]+)/$', HookView.as_view()),
)
