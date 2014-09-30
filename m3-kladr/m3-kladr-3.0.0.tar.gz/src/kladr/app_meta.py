#coding:utf-8

from django.conf import urls

from actions import kladr_controller, KLADRPack
from m3 import authenticated_user_required


def register_actions():
    kladr_controller.packs.append(KLADRPack())


def register_urlpatterns():
    """
    Регистрация конфигурации урлов для приложения kladr
    """
    return urls.patterns('',
                         (r'^m3-kladr', 'kladr.app_meta.kladr_view'), )


#===============================================================================
# Представления
#===============================================================================
@authenticated_user_required
def kladr_view(request):
    return kladr_controller.process_request(request) 
