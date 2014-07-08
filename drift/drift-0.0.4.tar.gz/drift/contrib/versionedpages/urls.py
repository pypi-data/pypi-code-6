from django.conf.urls import patterns, include, url

from .views import page, edit_page, auto_save, publish


urlpatterns = patterns('',
    url(r'^\+new/$', edit_page, name="new_versioned_page"),
    url(r'^(.+)/edit/$', edit_page, name="edit_versioned_page"),
    url(r'^(.+)/auto_save/$', auto_save, name="auto_save_versioned_page"),
    url(r'^(.+)/publish/$', publish, name="publish_versioned_page"),
    url(r'^(.+)/v/(\d+)/$', page, name="versioned_page_version"),
    url(r'^(.*)/$', page, name="versioned_page"),
)
