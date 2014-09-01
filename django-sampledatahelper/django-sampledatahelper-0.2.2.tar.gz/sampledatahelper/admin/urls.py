from django.conf.urls import url, patterns

urlpatterns = patterns('',
    url(r'^add_sample/(?P<app_label>[a-z0-9_]+)/(?P<model>[a-z0-9_]+)/$', 'sampledatahelper.admin.views.add_sample', 'sampledatahelper-add-sample'),
)
