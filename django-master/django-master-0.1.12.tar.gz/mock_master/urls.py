import djangomaster

from django.conf import settings
from django.conf.urls import patterns, url, include
from django.conf.urls.static import static


urlpatterns = patterns(
    r'',

    url(r'^master/', include(djangomaster.urls)),

)


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
