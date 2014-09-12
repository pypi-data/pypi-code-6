# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.contrib.admin.views.decorators import staff_member_required
from mailto.views import EditHTML, OptoutView


urlpatterns = patterns('',
    url(r'edit/html/$', staff_member_required(EditHTML.as_view()), name='new-html'),
    url(r'edit/html/(?P<pk>\d+)/$', staff_member_required(EditHTML.as_view()), name='edit-html'),
    url(r'optout/(?P<hash>[abcdef0-9]{32})/$', OptoutView.as_view(), name='optout'),
)