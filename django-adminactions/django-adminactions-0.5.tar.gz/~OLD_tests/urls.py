import django.contrib.auth.models
from django.conf.urls import patterns, include
from django.contrib import admin
import adminactions.actions as actions
import adminactions.urls

if django.contrib.auth.models.User not in admin.site._registry:
    admin.site.register(django.contrib.auth.models.User)

if django.contrib.auth.models.Permission not in admin.site._registry:
    admin.site.register(django.contrib.auth.models.Permission)

actions.add_to_site(admin.site)

urlpatterns = patterns('',
                       (r'^admin/', include(admin.site.urls)),
                       (r'^adminactions/', include(include(adminactions.urls))))
