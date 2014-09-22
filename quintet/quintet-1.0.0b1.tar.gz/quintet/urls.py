from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^quintet/', include('quintet.backend.urls')),
    url(r'^', include('quintet.blog.urls')),
)
