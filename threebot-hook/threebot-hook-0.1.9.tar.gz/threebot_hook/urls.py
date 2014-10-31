from django.conf.urls import patterns, url, include

from .views import HookView, create, edit, hooks_list

urlpatterns = patterns('',
    url(r'^list/(?P<wf_slug>[\w-]+)/$', hooks_list, name='hook_list'),
    url(r'^create/(?P<wf_slug>[\w-]+)/$', create, name='hook_create'),
    url(r'^edit/(?P<wf_slug>[\w-]+)/(?P<hook_slug>[\w-]+)/$', edit, name='hook_edit'),
    url(r'^(?P<token>[\w-]+)/(?P<identifier>[\w-]+)/$', HookView.as_view()),
)
