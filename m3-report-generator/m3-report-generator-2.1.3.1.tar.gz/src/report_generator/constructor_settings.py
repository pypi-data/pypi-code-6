#coding: utf-8

from django.db.backends import settings as applied_project_settings

from m3_ext.ui.app_ui import DesktopLoader

from report_generator.exceptions import SettingsException

# Подбираем настройки прикладного проекта. Проверяем наличие необходимы настроек и
# выставление значений по-умолчанию. Это необходимо для того, чтобы эти проверки были
# собраны в одном уютном месте, а не разбросаны по всему коду конструктора

if not hasattr(applied_project_settings, 'REPORT_GENERATOR_SETTINGS'):
    raise SettingsException(u'Отсутствуют настройки конструктора. Задайте словарь REPORT_GENERATOR_SETTINGS')

def error_msg(param_name):
    return u'Необходимо задать пару ключ-значение %s в словаре REPORT_GENERATOR_SETTINGS' % param_name

ICON_PLACES = []
if 'ICON_PLACES' in applied_project_settings.REPORT_GENERATOR_SETTINGS:
    ICON_PLACES = applied_project_settings.REPORT_GENERATOR_SETTINGS['ICON_PLACES']
else:
    # Значение по умолчанию - рабочий стол
    ICON_PLACES = [DesktopLoader.DESKTOP]


if 'OPENOFFICE_SERVER_PORT' not in applied_project_settings.REPORT_GENERATOR_SETTINGS:
    raise SettingsException(' '.join([u'На каком порту запускать сервер OPENOFFICE?', error_msg('OPENOFFICE_SERVER_PORT')]))
OPENOFFICE_SERVER_PORT = applied_project_settings.REPORT_GENERATOR_SETTINGS['OPENOFFICE_SERVER_PORT']


if 'TEMPLATE_DIR' not in applied_project_settings.REPORT_GENERATOR_SETTINGS:
    raise SettingsException(' '.join([u'Куда сохранять шаблоны?', error_msg('TEMPLATE_DIR')]))
TEMPLATE_DIR = applied_project_settings.REPORT_GENERATOR_SETTINGS['TEMPLATE_DIR']


if 'REPORT_DIR' not in applied_project_settings.REPORT_GENERATOR_SETTINGS:
    raise SettingsException(' '.join([u'Куда сохранять отчеты?', error_msg('REPORT_DIR')]))
REPORT_DIR = applied_project_settings.REPORT_GENERATOR_SETTINGS['REPORT_DIR']


if 'MODELS' in applied_project_settings.REPORT_GENERATOR_SETTINGS:
    MODELS = applied_project_settings.REPORT_GENERATOR_SETTINGS['MODELS']
else:
    MODELS = []


if 'EXCLUDE_MODELS' in applied_project_settings.REPORT_GENERATOR_SETTINGS:
    EXCLUDE_MODELS = applied_project_settings.REPORT_GENERATOR_SETTINGS['EXCLUDE_LIST']
else:
    EXCLUDE_MODELS = []