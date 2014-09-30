from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'example.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^faq/', include('qanda.urls')),
    # Normally we'd do this if DEBUG only, but this is just an example app.
    url(regex  = r'^static/(?P<path>.*)$', 
        view   = 'django.views.static.serve',
        kwargs = {'document_root': settings.MEDIA_ROOT}
    ),
)
