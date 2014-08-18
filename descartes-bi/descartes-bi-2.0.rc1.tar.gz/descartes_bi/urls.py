from django.conf.urls import include, patterns, url
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

handler500 = 'common.views.error500'
urlpatterns = patterns('',
    (r'^', include('common.urls', namespace='common')),
    (r'^admin/', include(admin.site.urls)),
    (r'^dashboards/', include('dashboards.urls', namespace='dashboards')),
    (r'^widgets/', include('widgets.urls', namespace='widgets')),
)

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    if 'rosetta' in settings.INSTALLED_APPS:
        urlpatterns += patterns('',
            url(r'^rosetta/', include('rosetta.urls'), name='rosetta'),
        )
