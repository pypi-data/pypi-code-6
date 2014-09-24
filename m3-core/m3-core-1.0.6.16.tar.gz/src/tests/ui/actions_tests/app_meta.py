#coding:utf-8
'''
Created on 18.11.11
@author: akvarats
'''

from django.conf import urls
from controller import actions_controller
from actions import ActionsTestsPack

def register_actions():
    actions_controller.packs.extend([ActionsTestsPack, ])

def register_urlpatterns():
    return urls.defaults.patterns('',(r'^actions-tests/', actions_tests_view) )

def actions_tests_view(request):
    return actions_controller.process_request(request)