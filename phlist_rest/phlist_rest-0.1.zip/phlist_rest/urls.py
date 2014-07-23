from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

from rest_framework import routers
from addresses import views as addresses_views
router = routers.DefaultRouter()
router.register(r'provinces', addresses_views.ProvinceViewSet)
router.register(r'cities', addresses_views.CityViewSet)


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'phlist.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^', include(router.urls)),
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^accounts/', include('userena.urls')),
    url(r'^api-token-auth/', 'rest_framework.authtoken.views.obtain_auth_token'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
)
