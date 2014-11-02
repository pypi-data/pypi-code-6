# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *
from rgallery.views import Photos, Videos, PhotosFolder, PhotoDelete, PhotoAdd

urlpatterns = patterns('',
    url(r'^$', Photos.as_view(), name='app_gallery-gallery'),
    url(r'^page/(?P<page>\d+)/$', Photos.as_view(), name='app_gallery-gallery-page'),
    url(r'^photo/del/$', PhotoDelete.as_view(), name='app_gallery-photo-del'),
    url(r'^photo/add/$', PhotoAdd.as_view(), name='app_gallery-photo-add'),
    url(r'^videos/$', Videos.as_view(), name='app_gallery-videos'),
    url(r'^videos/page/(?P<page>\d+)/$', Videos.as_view(), name='app_gallery-videos-page'),
    url(r'^(?P<folder>[-_A-Za-z0-9]+)/$', PhotosFolder.as_view(), name='app_gallery-folder'),
)
