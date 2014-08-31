# -*- coding: utf-8 -*-

""" django_redirector  urls

Providing generate_url function.
"""

from django.conf.urls import patterns, include, url
from django.conf import settings
#from views import *


def generate_url():
    """
    """
    target_urls = {}

    #if("DJANGO_REDIRECTER_SUPERUSER" in settings):
    if(hasattr(settings,"DJANGO_REDIRECTER_SUPERUSER")):
        for key,item in settings.DJANGO_REDIRECTER_SUPERUSER.items():
            target_urls[key]="superuser"
    if(hasattr(settings,"DJANGO_REDIRECTER_STAFF")):
        for key,item in settings.DJANGO_REDIRECTER_STAFF.items():
            target_urls[key]="staff"
    if(hasattr(settings,"DJANGO_REDIRECTER_LOGIN")):
        for key,item in settings.DJANGO_REDIRECTER_LOGIN.items():
            target_urls[key]="login"
    if(hasattr(settings,"DJANGO_REDIRECTER_GROUP")):
        for key,item in settings.DJANGO_REDIRECTER_GROUP.items():
            target_urls[key]="group"

    urlpatterns = patterns("")

    if(hasattr(settings,"DJANGO_REDIRECTER_EXCEPT")):
        for key,item in settings.DJANGO_REDIRECTER_EXCEPT.items():
            if(key[-1]!="/"):
                key = key + "/"
            urlpatterns += patterns('',url('^%s(?P<suburl>.*)' % key, 'django_redirector.views.redirect_for_exceptions',{"tag":key}))

    for key in sorted(target_urls, key=len, reverse=True):
        if(key[-1]!="/"):
            key = key + "/"
        urlpatterns += patterns('',url('^%s(?P<suburl>.*)' % key, 'django_redirector.views.redirect_with_auth_%s' % target_urls[key],{"tag":key}))

    return urlpatterns


#        settings.DJANGO_REDIRECTER_SUPERUSER={"/test/":"/protected_test/","/test_super/":"/protected_test_super/"}
#        settings.DJANGO_REDIRECTER_STAFF={"/test_staff/":"/protected_test_staff/","/test_staff2/":"/protected_test_staff2/"}
#        settings.DJANGO_REDIRECTER_LOGIN={"/test_login/":"/protected_test_login/","/test_login2/":"/protected_test_login2/"}
#        settings.DJANGO_REDIRECTER_GROUP={"/test_groupa/":("/protected_test_groupa/","groupa"),"/test_groupb/":("/protected_test_groupb/","groupb")}
