from django.conf.urls import patterns, url


urlpatterns = patterns('rb_oauth.views',
                       url(r'^$', 'oauth', name='rb-oauth'),
                       )
