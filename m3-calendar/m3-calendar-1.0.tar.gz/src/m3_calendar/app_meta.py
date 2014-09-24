#coding:utf-8
'''
Created on 31.03.2011

@author: akvarats
'''

from django.conf import urls as django_urls

from controller import calendar_controller
from m3_calendar.actions import M3CalendarPack
from m3_users.metaroles import get_metarole
from m3.ui.app_ui import DesktopLaunchGroup, DesktopShortcut, DesktopLoader
from m3.helpers.users import authenticated_user_required

def register_actions():
    calendar_controller.packs.extend([M3CalendarPack,])

def register_urlpatterns():
    '''
    Регистрация конфигурации урлов для приложения
    '''
    return django_urls.defaults.patterns('',
        (r'^m3-calendar/', calendar_view)
    )

def register_desktop_menu():
    '''Регистрирует пункт меню в "Администрировании"'''
    ADMIN_METAROLE = get_metarole('admin')

    admin_root = DesktopLaunchGroup(name = u'Администрирование')
    admin_root.subitems.append(
        DesktopShortcut(name = u'Календарь рабочих и выходных дней',
                        pack = M3CalendarPack)
    )

    DesktopLoader.add(ADMIN_METAROLE, DesktopLoader.START_MENU, admin_root)
    DesktopLoader.add(ADMIN_METAROLE, DesktopLoader.TOPTOOLBAR, admin_root)
    
@authenticated_user_required
def calendar_view(request):
    return calendar_controller.process_request(request)