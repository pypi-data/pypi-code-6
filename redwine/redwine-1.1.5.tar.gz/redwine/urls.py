from django.conf.urls import patterns, include, url
from redwine.views import redwine_home, redwine_com
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^(\w+)/$', redwine_com),
	url(r'^$', redwine_home),
    (r'^admin/', include(admin.site.urls)),
    #(r'accounts/login/',include(admin.site.urls)),
    #url (r'^/$', redwine_home),
)