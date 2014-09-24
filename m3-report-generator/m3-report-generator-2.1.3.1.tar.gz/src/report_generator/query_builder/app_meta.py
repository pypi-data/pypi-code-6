#coding: utf-8
from django.conf import urls

from m3.actions import ActionController

from report_generator.query_builder import actions

controller = ActionController(url = '/queries-constructor')

def register_actions():
    controller.packs.extend([
        actions.QueryConstructorPack
    ])

def queries_constructor_view(request):
    return controller.process_request(request)

def register_urlpatterns():

    return urls.defaults.patterns('',
        (r'^queries-constructor/', queries_constructor_view))