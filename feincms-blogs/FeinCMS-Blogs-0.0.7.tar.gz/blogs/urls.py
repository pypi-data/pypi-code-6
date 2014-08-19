from django.conf.urls import patterns, url

from djapps.blogs.views import PostListView
from djapps.blogs.views import PostView
from djapps.blogs.views import PostPermalinkView

urlpatterns = patterns(
    '',
    url(r'^permalink/(?P<pk>[1-9][0-9]*)/$',
        PostPermalinkView.as_view(),
        name='post_permalink'),
    url(r'^all/all/$',
        PostListView.as_view(),
        name='post_list'),
    url(r'^all'
        r'/(?P<date__year>[1-9][0-9]{3})/$',
        PostListView.as_view(),
        name='post_list'),
    url(r'^all'
        r'/(?P<date__year>[1-9][0-9]{3})'
        r'/(?P<date__month>[1-9][0-9]?)/$',
        PostListView.as_view(),
        name='post_list'),
    url(r'^all'
        r'/(?P<date__year>[1-9][0-9]{3})'
        r'/(?P<date__month>[1-9][0-9]?)'
        r'/(?P<date__day>[1-9][0-9]?)/$',
        PostListView.as_view(),
        name='post_list'),
    url(r'^(?P<blog__slug>[^/]+)/all/$',
        PostListView.as_view(),
        name='post_list'),
    url(r'^(?P<blog__slug>[^/]+)'
        r'/(?P<date__year>[1-9][0-9]{3})/$',
        PostListView.as_view(),
        name='post_list'),
    url(r'^(?P<blog__slug>[^/]+)'
        r'/(?P<date__year>[1-9][0-9]{3})'
        r'/(?P<date__month>[1-9][0-9]?)/$',
        PostListView.as_view(),
        name='post_list'),
    url(r'^(?P<blog__slug>[^/]+)'
        r'/(?P<date__year>[1-9][0-9]{3})'
        r'/(?P<date__month>[1-9][0-9]?)'
        r'/(?P<date__day>[1-9][0-9]?)/$',
        PostListView.as_view(),
        name='post_list'),
    url(r'^(?P<blog__slug>[^/]+)'
        r'/(?P<date__year>[1-9][0-9]{3})'
        r'/(?P<date__month>[1-9][0-9]?)'
        r'/(?P<date__day>[1-9][0-9]?)'
        r'/(?P<slug>[^/]+)/$',
        PostView.as_view(),
        name='post'),
)
