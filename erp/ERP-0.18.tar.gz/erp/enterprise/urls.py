__author__ = 'cltanuki'
from django.conf.urls import patterns, url
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from . import views
from . import api_views, models

urlpatterns = patterns('',
    url(r'^objs/$', ListView.as_view(model=models.CorpObject), name='obj-list'),
    url(r'^register/$', views.Register.as_view(), name='register'),
    url(r'^objs/$', ListView.as_view(model=models.CorpObject), name='obj-list'),
    url(r'^units/$', ListView.as_view(model=models.CorpUnit), name='unit-list'),
    url(r'^users/$', ListView.as_view(model=models.CorpUser), name='user-list'),
    url(r'^obj/(?P<pk>[0-9]+)$', DetailView.as_view(model=models.CorpObject), name='obj-detail'),
    url(r'^unit/(?P<pk>[0-9]+)$', DetailView.as_view(model=models.CorpUnit), name='unit-detail'),
    url(r'^user/(?P<pk>[0-9]+)$', DetailView.as_view(model=models.CorpUser), name='user-detail'),
    url(r'^api/units/$', api_views.GroupViewSet.as_view()),
    url(r'^api/units/(?P<pk>\d+)/$', api_views.GroupView.as_view()),
    url(r'^api/users/$', api_views.UserViewSet.as_view()),
    url(r'^api/users/(?P<pk>\d+)/$', api_views.UserView.as_view()),
    url(r'^api/objs/$', api_views.ObjViewSet.as_view()),
    url(r'^api/objs/(?P<pk>\d+)/$', api_views.ObjView.as_view()),
)