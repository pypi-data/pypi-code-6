#coding:utf-8
'''
Created on 24.08.2010

@author: kir
'''
from django.conf import urls

from m3.ui.actions import ActionController
from m3_checkie import actions
from m3.helpers.users import authenticated_user_required

m3_checkie_controller = ActionController('/unsupported-browser')

def register_urlpatterns():
    return urls.defaults.patterns('',
        (r'^unsupported-browser', 'm3_checkie.app_meta.controller'),
    )

@authenticated_user_required
def controller(request):
    return m3_checkie_controller.process_request(request)

def register_actions():
    m3_checkie_controller.packs.extend([
        actions.CheckBrowserActionsPack,
    ])