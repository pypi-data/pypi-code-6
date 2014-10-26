from django.conf.urls import patterns, url


urlpatterns = patterns('quintet.blog.views',
    url(r'^$', 'list_posts'),
    url(r'^page/(?P<slug>[-\w]+)/$', 'view_page'),
    url(r'^contributor/(?P<contributor>[-\w]+)/$', 'list_posts'),
    url(r'^date/(?:(?P<day>\d{1,2})-)?(?P<month>[a-z]{3})-(?P<year>\d{4})/$', 'list_posts'),
    url(r'^date/(?:(?P<month>[a-z]{3})|(?P<year>\d{4}))/$', 'list_posts'),
    url(r'^tag/(?P<tag>[-\w]+)/$', 'list_posts'),
    url(r'^(?P<section>[-\w]+)/$', 'list_posts'),
    url(r'^(?P<section>[-\w]+)/(?P<post>[-\w]+)/$', 'view_post')
)
