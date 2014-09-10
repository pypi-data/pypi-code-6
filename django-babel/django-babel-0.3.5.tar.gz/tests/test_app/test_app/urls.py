from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'test_app.views.index', name='index'),
    url(r'^admin/', include(admin.site.urls)),
)
