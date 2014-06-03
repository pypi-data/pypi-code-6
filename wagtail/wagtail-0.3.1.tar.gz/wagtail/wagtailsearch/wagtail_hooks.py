from django.conf.urls import include, url

from wagtail.wagtailadmin import hooks
from wagtail.wagtailsearch.urls import admin as admin_urls


def register_admin_urls():
    return [
        url(r'^search/', include(admin_urls)),
    ]
hooks.register('register_admin_urls', register_admin_urls)
