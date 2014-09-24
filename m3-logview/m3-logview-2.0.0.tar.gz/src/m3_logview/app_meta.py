#coding:utf-8
'''
Created on 24.08.2010

@author: kir
'''
from django.conf import urls

from m3 import authenticated_user_required
from m3.actions import ActionController
from m3_logview import actions


m3_logview_controller = ActionController('/m3/logview')

def register_urlpatterns():
    return urls.defaults.patterns('',
        (r'^m3/logview/logs', 'm3_logview.app_meta.controller'),
        (r'^m3/logview/get-logs-file', 'm3_logview.app_meta.controller'),
    )

@authenticated_user_required
def controller(request):
    return m3_logview_controller.process_request(request)

def register_actions():
    m3_logview_controller.packs.extend([
        actions.Mis_Admin_ActionsPack
    ])
