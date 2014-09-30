#coding:utf-8

from django.conf import urls

from actions import kladr_controller, KLADRPack
from m3 import authenticated_user_required


def register_actions():
    kladr_controller.packs.append(KLADRPack())
    #kladr_controller.rebuild_patterns()


def register_urlpatterns():
    u"""
    Регистрация конфигурации урлов для приложения kladr
    """
    return urls.defaults.patterns(
        '', (r'^m3-kladr', 'kladr.app_meta.kladr_view'),
    )


#===============================================================================
# Представления
#===============================================================================
@authenticated_user_required
def kladr_view(request):
    return kladr_controller.process_request(request) 
