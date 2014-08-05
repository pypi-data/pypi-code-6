from django.conf import settings
from django.conf.urls import patterns, url
from django.conf.urls.static import static

from django_master.views.home import HomeView
from django_master.views.routes import RoutesListView
from django_master.views.settings import SettingsListView


STATIC_ACTIVATED = getattr(settings, 'DJANGO_MASTER_STATIC_ACTIVATED', False)


urlpatterns = patterns(r'',

    url(r'^$', HomeView.as_view(), name='djangomaster_home'),
    url(r'^routes/$', RoutesListView.as_view(), name='djangomaster_routes'),
    url(r'^settings/$', SettingsListView.as_view(),
        name='djangomaster_settings'),

)

if STATIC_ACTIVATED:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
