from django.conf import settings
from django.conf.urls import include, patterns, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # ----Django
    (r'^admin/', include(admin.site.urls)),

    #(r'^i18n/', include('django.conf.urls.i18n')),

    # ----Project
    (r'^', include('main.urls')),
    (r'^common/', include('common.urls')),
    (r'^inventory/', include('inventory.urls')),
    (r'^assets/', include('assets.urls')),
    (r'^search/', include('dynamic_search.urls')),
    #(r'^import/', include('importer.urls')),
    (r'^movements/', include('movements.urls')),
    (r'^generic_photos/', include('photos.urls')),
)

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    if 'rosetta' in settings.INSTALLED_APPS:
        urlpatterns += patterns('',
            url(r'^rosetta/', include('rosetta.urls'), name='rosetta'),
        )
