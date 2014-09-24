#coding:utf-8
'''
Created on 22.07.2011

@author: akvarats
'''

from django.conf import urls as django_urls

from controller import test_controller
from actions import CoreActionPack

def register_actions():
    test_controller.packs.extend([CoreActionPack, ])

def register_urlpatterns():
    return django_urls.defaults.patterns('',(r'^m3-tests/', tests_view) )

def tests_view(request):
    return test_controller.process_request(request)