from django.conf.urls import include, url
from django.contrib import admin

from django.contrib.sitemaps.views import sitemap
from demoapp.sitemaps import DemoSitemap

sitemaps = {
    'demos': DemoSitemap,
    }

urlpatterns = [
    # Examples:
    # url(r'^$', 'example.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^demoapp/', include('demoapp.urls')),

    url(r'^sitemap\.xml', sitemap, {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'),

    ]
