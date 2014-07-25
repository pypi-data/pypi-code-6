from django.conf.urls import patterns, url
from trash import views

urlpatterns = patterns('',
	url('', views.index, name='index'),
)