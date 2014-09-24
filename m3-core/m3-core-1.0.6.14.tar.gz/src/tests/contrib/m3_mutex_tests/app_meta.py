#coding:utf-8
'''
Created on 22.07.2011

@author: akvarats
'''

from django.conf import urls as django_urls

from controller import mutex_controller
from actions import MutexActionPack


def register_actions():
    mutex_controller.packs.extend([MutexActionPack, ])

def register_urlpatterns():
    return django_urls.defaults.patterns('',(r'^mutex/', mutex_view) )

def mutex_view(request):
    return mutex_controller.process_request(request)

