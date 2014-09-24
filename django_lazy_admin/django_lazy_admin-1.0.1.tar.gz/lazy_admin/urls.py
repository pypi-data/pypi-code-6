from django.conf.urls import patterns, url
from views import lazy_column_view

urlpatterns = patterns('',
	url(r'column/$', lazy_column_view, name='lazy-column-view')
)