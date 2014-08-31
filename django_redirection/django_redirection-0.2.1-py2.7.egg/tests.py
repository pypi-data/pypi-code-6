# -*- coding: utf-8 -*-

""" Test for django_redirection
"""

from django.test import TestCase

from django.conf.urls import patterns, include, url
from django.contrib.auth.models import User,AnonymousUser, Group
from django.conf import settings

from django.core.exceptions import PermissionDenied

import django_redirection
import django_redirection.views

class DummyRequest:
    def __init__(self,user,GET={}):
        self.user=user
        self.GET=GET
        self.POST={}

class URLconfGeneratorTest(TestCase):
    """To generate url patterns based on settings.
    """

    def test_all(self):
        """All of DJANGO_REDIRECCTER_* are set.
        """
        settings.DJANGO_REDIRECTER_SUPERUSER={"test/":"protected_test/","test_super/":"protected_test_super/"}
        settings.DJANGO_REDIRECTER_STAFF={"test_staff/":"protected_test_staff/","test_staff2/":"protected_test_staff2/"}
        settings.DJANGO_REDIRECTER_LOGIN={"test_login/":"/rotected_test_login/","test_login2/":"protected_test_login2/"}
        settings.DJANGO_REDIRECTER_GROUP={"test_groupa/":("protected_test_groupa/","groupa"),"test_groupb/":("protected_test_groupb/","groupb")}
        settings.DJANGO_REDIRECTER_EXCEPT={"test/except/":"protected_test/except/","test_staff/except/":"protected_test_staff/except/","test_login/except/":"rotected_test_login/except/","test_groupa/except/":"protected_test_groupa/except/"}


        urlpatterns = patterns("",
                               url(r'^test_groupa/except/(?P<suburl>.*)', 'django_redirection.views.redirect_for_exceptions',{"tag":"test_groupa/except/"}),
                               url(r'^test_login/except/(?P<suburl>.*)', 'django_redirection.views.redirect_for_exceptions',{"tag":"test_login/except/"}),
                               url(r'^test_staff/except/(?P<suburl>.*)', 'django_redirection.views.redirect_for_exceptions',{"tag":"test_staff/except/"}),
                               url(r'^test/except/(?P<suburl>.*)', 'django_redirection.views.redirect_for_exceptions',{"tag":"test/except/"}),
                               url(r'^test_staff2/(?P<suburl>.*)', 'django_redirection.views.redirect_with_auth_staff',{"tag":"test_staff2/"}),
                               url(r'^test_login2/(?P<suburl>.*)', 'django_redirection.views.redirect_with_auth_login',{"tag":"test_login2/"}),
                               url(r'^test_groupa/(?P<suburl>.*)', 'django_redirection.views.redirect_with_auth_group',{"tag":"test_groupa/"}),
                               url(r'^test_groupb/(?P<suburl>.*)', 'django_redirection.views.redirect_with_auth_group',{"tag":"test_groupb/"}),
                               url(r'^test_super/(?P<suburl>.*)', 'django_redirection.views.redirect_with_auth_superuser',{"tag":"test_super/"}),
                               url(r'^test_login/(?P<suburl>.*)', 'django_redirection.views.redirect_with_auth_login',{"tag":"test_login/"}),
                               url(r'^test_staff/(?P<suburl>.*)', 'django_redirection.views.redirect_with_auth_staff',{"tag":"test_staff/"}),
                               url(r'^test/(?P<suburl>.*)', 'django_redirection.views.redirect_with_auth_superuser',{"tag":"test/"}),
                               )
        generated_urlpatterns = django_redirection.generate_url()

        self.assertEquals(len(urlpatterns),len(generated_urlpatterns))
        for ind in range(0,len(urlpatterns)):
            self.assertEquals(urlpatterns[ind].regex.pattern,generated_urlpatterns[ind].regex.pattern)

    def test_superuser(self):
        """DJANGO_REDIRECCTER_SUPERUSER is set.
        """
        settings.DJANGO_REDIRECTER_SUPERUSER={"test/":"protected_test/","test_super/":"protected_test_super/"}
        if(hasattr(settings,"DJANGO_REDIRECTER_STAFF")):
            del settings.DJANGO_REDIRECTER_STAFF
        if(hasattr(settings,"DJANGO_REDIRECTER_LOGIN")):
            del settings.DJANGO_REDIRECTER_LOGIN
        if(hasattr(settings,"DJANGO_REDIRECTER_GROUP")):
            del settings.DJANGO_REDIRECTER_GROUP
        if(hasattr(settings,"DJANGO_REDIRECTER_EXCEPT")):
            del settings.DJANGO_REDIRECTER_EXCEPT


        urlpatterns = patterns("",
                               url(r'^test_super/(?P<suburl>.*)', 'django_redirection.redirect_with_auth_superuser',{"tag":"test_super"}),
                               url(r'^test/(?P<suburl>.*)', 'django_redirection.redirect_with_auth_superuser',{"tag":"test"}),
                               )
        generated_urlpatterns = django_redirection.generate_url()

        self.assertEquals(len(urlpatterns),len(generated_urlpatterns))
        for ind in range(0,len(urlpatterns)):
            self.assertEquals(urlpatterns[ind].regex.pattern,generated_urlpatterns[ind].regex.pattern)

    def test_staff(self):
        """DJANGO_REDIRECCTER_STAFF is set.
        """
        settings.DJANGO_REDIRECTER_STAFF={"test_staff/":"protected_test_staff/","test_staff2/":"protected_test_staff2/"}
        if(hasattr(settings,"DJANGO_REDIRECTER_SUPERUSER")):
            del settings.DJANGO_REDIRECTER_SUPERUSER
        if(hasattr(settings,"DJANGO_REDIRECTER_LOGIN")):
            del settings.DJANGO_REDIRECTER_LOGIN
        if(hasattr(settings,"DJANGO_REDIRECTER_GROUP")):
            del settings.DJANGO_REDIRECTER_GROUP
        if(hasattr(settings,"DJANGO_REDIRECTER_EXCEPT")):
            del settings.DJANGO_REDIRECTER_EXCEPT


        urlpatterns = patterns("",
                               url(r'^test_staff2/(?P<suburl>.*)', 'django_redirection.redirect_with_auth_staff',{"tag":"test_staff2"}),
                               url(r'^test_staff/(?P<suburl>.*)', 'django_redirection.redirect_with_auth_staff',{"tag":"test_staff"}),
                               )
        generated_urlpatterns = django_redirection.generate_url()

        self.assertEquals(len(urlpatterns),len(generated_urlpatterns))
        for ind in range(0,len(urlpatterns)):
            self.assertEquals(urlpatterns[ind].regex.pattern,generated_urlpatterns[ind].regex.pattern)

    def test_login(self):
        """DJANGO_REDIRECCTER_LOGIN is set.
        """

        settings.DJANGO_REDIRECTER_LOGIN={"test_login/":"protected_test_login/","test_login2/":"protected_test_login2/"}
        if(hasattr(settings,"DJANGO_REDIRECTER_STAFF")):
            del settings.DJANGO_REDIRECTER_STAFF
        if(hasattr(settings,"DJANGO_REDIRECTER_SUPERUSER")):
            del settings.DJANGO_REDIRECTER_SUPERUSER
        if(hasattr(settings,"DJANGO_REDIRECTER_GROUP")):
            del settings.DJANGO_REDIRECTER_GROUP
        if(hasattr(settings,"DJANGO_REDIRECTER_EXCEPT")):
            del settings.DJANGO_REDIRECTER_EXCEPT


        urlpatterns = patterns("",
                               url(r'^test_login2/(?P<suburl>.*)', 'django_redirection.redirect_with_auth_login',{"tag":"test_login2"}),
                               url(r'^test_login/(?P<suburl>.*)', 'django_redirection.redirect_with_auth_login',{"tag":"test_login"}),
                               )
        generated_urlpatterns = django_redirection.generate_url()

        self.assertEquals(len(urlpatterns),len(generated_urlpatterns))
        for ind in range(0,len(urlpatterns)):
            self.assertEquals(urlpatterns[ind].regex.pattern,generated_urlpatterns[ind].regex.pattern)

    def test_group(self):
        """DJANGO_REDIRECCTER_GROUP is set.
        """

        settings.DJANGO_REDIRECTER_GROUP={"test_groupa/":("protected_test_groupa/","groupa"),"test_groupb/":("protected_test_groupb/","groupb")}
        if(hasattr(settings,"DJANGO_REDIRECTER_STAFF")):
            del settings.DJANGO_REDIRECTER_STAFF
        if(hasattr(settings,"DJANGO_REDIRECTER_SUPERUSER")):
            del settings.DJANGO_REDIRECTER_SUPERUSER
        if(hasattr(settings,"DJANGO_REDIRECTER_LOGIN")):
            del settings.DJANGO_REDIRECTER_LOGIN
        if(hasattr(settings,"DJANGO_REDIRECTER_EXCEPT")):
            del settings.DJANGO_REDIRECTER_EXCEPT


        urlpatterns = patterns("",
                               url(r'^test_groupa/(?P<suburl>.*)', 'django_redirection.redirect_with_auth_group',{"tag":"test_groupa"}),
                               url(r'^test_groupb/(?P<suburl>.*)', 'django_redirection.redirect_with_auth_group',{"tag":"test_groupb"}),
                               )
        generated_urlpatterns = django_redirection.generate_url()

        self.assertEquals(len(urlpatterns),len(generated_urlpatterns))
        for ind in range(0,len(urlpatterns)):
            self.assertEquals(urlpatterns[ind].regex.pattern,generated_urlpatterns[ind].regex.pattern)


class RedirectTest(TestCase):
    """Redirect tests for superusers.
    """
    def test_superuser(self):
        settings.DJANGO_REDIRECTER_SUPERUSER={"test/":"/protected_test/","test_super/":"protected_test_super/"}
        settings.DJANGO_REDIRECTER_STAFF={"test_staff/":"protected_test_staff/","test_staff2/":"protected_test_staff2/"}
        settings.DJANGO_REDIRECTER_LOGIN={"test_login/":"rotected_test_login/","test_login2/":"protected_test_login2/"}
        settings.DJANGO_REDIRECTER_GROUP={"test_groupa/":("protected_test_groupa/","groupa"),"test_groupb/":("protected_test_groupb/","groupb")}
        settings.DJANGO_REDIRECTER_EXCEPT={"test/except/":"protected_test/except/","test_staff/except/":"protected_test_staff/except/","test_login/except/":"rotected_test_login/except/","test_groupa/except/":"protected_test_groupa/except/"}
#        settings.DJANGO_REDIRECTER_EXCEPT=[{"tag":"test/","suburl":"except"},{"tag":"test_staff/","suburl":"except"},{"tag":"test_login/","suburl":"except"},{"tag":"test_groupa/","suburl":"except"}]

        #user = User.objects.create_user(username='test', email='test@example.co', password='secret')
        user = User.objects.create_superuser(username='test', email='test@example.co', password='secret')
        user.save()

        normal_user = User.objects.create_user(username='test2', email='test2@example.co', password='secret')
        normal_user.save()

        result = django_redirection.views.redirect_with_auth_superuser(DummyRequest(user),tag="test/",suburl="")
        self.assertEquals(result['X-Accel-Redirect'],"/protected_test/")

        result = django_redirection.views.redirect_with_auth_superuser(DummyRequest(user),tag="test/",suburl="aaaa")
        self.assertEquals(result['X-Accel-Redirect'],"/protected_test/aaaa")

        result = django_redirection.views.redirect_with_auth_superuser(DummyRequest(user),tag="test/",suburl="aaaa/bbbb/")
        self.assertEquals(result['X-Accel-Redirect'],"/protected_test/aaaa/bbbb/")

        self.assertRaises(PermissionDenied, lambda: django_redirection.views.redirect_with_auth_superuser(DummyRequest(normal_user),tag="test/",suburl="aaaa/bbbb/"))

        #result = django_redirection.views.redirect_with_auth_superuser(DummyRequest(normal_user),tag="test/except/",suburl="except")
        #self.assertEquals(result['X-Accel-Redirect'],"/protected_test/except")

    def test_except(self):
        settings.DJANGO_REDIRECTER_EXCEPT={"test/except/":"protected_test/except/","test_staff/except/":"protected_test_staff/except/","test_login/except/":"rotected_test_login/except/","test_groupa/except/":"protected_test_groupa/except/"}
        user = User.objects.create_superuser(username='test', email='test@example.co', password='secret')
        user.save()

        normal_user = User.objects.create_user(username='test2', email='test2@example.co', password='secret')
        normal_user.save()

        result = django_redirection.views.redirect_for_exceptions(DummyRequest(normal_user),tag="test/except/",suburl="except")
        self.assertEquals(result['X-Accel-Redirect'],"/protected_test/except/except")

    def test_staff(self):
        settings.DJANGO_REDIRECTER_STAFF={"test_staff/":"protected_test_staff/","test_staff2/":"protected_test_staff2/"}
        settings.DJANGO_REDIRECTER_EXCEPT={"test/except/":"protected_test/except/","test_staff/except/":"protected_test_staff/except/","test_login/except/":"rotected_test_login/except/","test_groupa/except/":"protected_test_groupa/except/"}
#        settings.DJANGO_REDIRECTER_EXCEPT=[{"tag":"test/","suburl":"except"},{"tag":"test_staff/","suburl":"except"},{"tag":"test_login/","suburl":"except"},{"tag":"test_groupa/","suburl":"except"}]

        #user = User.objects.create_user(username='test', email='test@example.co', password='secret')
        user = User.objects.create_user(username='test', email='test@example.co', password='secret')
        user.is_staff=True
        user.save()

        normal_user = User.objects.create_user(username='test2', email='test2@example.co', password='secret')
        normal_user.save()

        result = django_redirection.views.redirect_with_auth_staff(DummyRequest(user),tag="test_staff/",suburl="")
        self.assertEquals(result['X-Accel-Redirect'],"/protected_test_staff/")

        result = django_redirection.views.redirect_with_auth_staff(DummyRequest(user),tag="test_staff/",suburl="aaaa")
        self.assertEquals(result['X-Accel-Redirect'],"/protected_test_staff/aaaa")

        result = django_redirection.views.redirect_with_auth_staff(DummyRequest(user),tag="test_staff/",suburl="aaaa/bbbb/")
        self.assertEquals(result['X-Accel-Redirect'],"/protected_test_staff/aaaa/bbbb/")

        self.assertRaises(PermissionDenied, lambda: django_redirection.views.redirect_with_auth_staff(DummyRequest(normal_user),tag="test_staff/",suburl="aaaa/bbbb/"))

        #result = django_redirection.views.redirect_with_auth_staff(DummyRequest(normal_user),tag="test_staff/",suburl="except")
        #self.assertEquals(result['X-Accel-Redirect'],"/protected_test_staff/except")

    def test_login(self):
        settings.DJANGO_REDIRECTER_LOGIN={"test_login/":"protected_test_login/","test_login2/":"protected_test_login2/"}
        settings.DJANGO_REDIRECTER_EXCEPT={"test/except/":"protected_test/except/","test_staff/except/":"protected_test_staff/except/","test_login/except/":"rotected_test_login/except/","test_groupa/except/":"protected_test_groupa/except/"}
#        settings.DJANGO_REDIRECTER_EXCEPT=[{"tag":"test/","suburl":"except"},{"tag":"test_staff/","suburl":"except"},{"tag":"test_login/","suburl":"except"},{"tag":"test_groupa/","suburl":"except"}]

        #user = User.objects.create_user(username='test', email='test@example.co', password='secret')
        user = User.objects.create_user(username='test', email='test@example.co', password='secret')
        user.is_staff=True
        user.save()

        a_user = AnonymousUser()

        result = django_redirection.views.redirect_with_auth_login(DummyRequest(user),tag="test_login/",suburl="")
        self.assertEquals(result['X-Accel-Redirect'],"/protected_test_login/")

        result = django_redirection.views.redirect_with_auth_login(DummyRequest(user),tag="test_login/",suburl="aaaa")
        self.assertEquals(result['X-Accel-Redirect'],"/protected_test_login/aaaa")

        result = django_redirection.views.redirect_with_auth_login(DummyRequest(user),tag="test_login/",suburl="aaaa/bbbb/")
        self.assertEquals(result['X-Accel-Redirect'],"/protected_test_login/aaaa/bbbb/")

        self.assertRaises(PermissionDenied, lambda: django_redirection.views.redirect_with_auth_login(DummyRequest(a_user),tag="test_login/",suburl="aaaa/bbbb/"))

        #result = django_redirection.views.redirect_with_auth_staff(DummyRequest(a_user),tag="test",suburl="except")
        #self.assertEquals(result['X-Accel-Redirect'],"/protected_test/except")

    def test_group(self):
        settings.DJANGO_REDIRECTER_GROUP={"test_groupa/":("protected_test_groupa/","groupa"),"test_groupb/":("protected_test_groupb/","groupb")}

        groupa = Group(name="groupa")
        groupa.save()

        userA = User.objects.create_user(username='test', email='test@example.co', password='secret')
        userA.groups.add(groupa)
        userA.save()

        normal_user = User.objects.create_user(username='test2', email='test2@example.co', password='secret')
        normal_user.save()

        result = django_redirection.views.redirect_with_auth_group(DummyRequest(userA),tag="test_groupa/",suburl="")
        self.assertEquals(result['X-Accel-Redirect'],"/protected_test_groupa/")

        result = django_redirection.views.redirect_with_auth_group(DummyRequest(userA),tag="test_groupa/",suburl="aaaa")
        self.assertEquals(result['X-Accel-Redirect'],"/protected_test_groupa/aaaa")

        result = django_redirection.views.redirect_with_auth_group(DummyRequest(userA),tag="test_groupa/",suburl="aaaa/bbbb/")
        self.assertEquals(result['X-Accel-Redirect'],"/protected_test_groupa/aaaa/bbbb/")

        self.assertRaises(PermissionDenied, lambda: django_redirection.views.redirect_with_auth_group(DummyRequest(normal_user),tag="test_groupa/",suburl="aaaa/bbbb/"))

