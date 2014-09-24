#coding: utf-8

from django.conf import urls

from m3.actions import ActionController

from report_generator.report_builder import actions

controller = ActionController('/report-constructor')

def register_actions():
    controller.packs.extend([
        actions.ReportPack
    ])

def report_constructor_view(request):
    return controller.process_request(request)

def register_urlpatterns():

    return urls.defaults.patterns('',
        (r'^report-constructor/', report_constructor_view))