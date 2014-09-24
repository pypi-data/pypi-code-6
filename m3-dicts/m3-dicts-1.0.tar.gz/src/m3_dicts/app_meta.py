#coding:utf-8

from django.conf import urls as django_urls

from m3_users.metaroles import get_metarole
from m3.ui.actions import ActionController
from m3.ui.app_ui import DesktopLaunchGroup, DesktopLoader, DesktopShortcut
from m3.helpers.users import authenticated_user_required

from actions import DulType_DictPack

m3_dicts_controller = ActionController('/m3-dicts')


def register_urlpatterns():
    '''
    Регистрация конфигурации урлов для приложения
    '''
    return django_urls.defaults.patterns('',(r'^m3-dicts/', m3_dicts_view) )

@authenticated_user_required
def m3_dicts_view(request):
    return m3_dicts_controller.process_request(request)