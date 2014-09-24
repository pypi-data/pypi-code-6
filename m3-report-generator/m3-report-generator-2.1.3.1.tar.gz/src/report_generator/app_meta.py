#coding: utf-8

import os

from django.http import HttpResponse
from django.conf import urls
from django import template as django_template

from m3_ext.ui import app_ui
from m3_ext.ui.results import ExtUIScriptResult
from m3.actions import urls as m3_urls

from m3_users.metaroles import get_metarole

from report_generator.constructor_settings import (OPENOFFICE_SERVER_PORT,
                                                   ICON_PLACES)
from report_generator.ui import ConstructorWindow
from report_generator.query_builder import actions as query_actions
from report_generator.report_builder import actions as report_actions

def register_desktop_menu():
    """
    Добавляем иконку на рабочий стол
    """

    url = '/constructor'
    name = u'Конструктор запросов и отчетов'
    admin_metarole = get_metarole('admin')

    app_ui.add_desktop_launcher(name=name,
                                url=url,
                                metaroles=admin_metarole,
                                places=ICON_PLACES,
                                icon='icon-report-generator')

def register_urlpatterns():
    """
    Регистрация URL приложения
    """

    return urls.defaults.patterns('',

        (r'^report_static/(?P<path>.*)$', 'django.views.static.serve',
             {'document_root': os.path.join(os.path.dirname(__file__), 'static')}),

        (r'^constructor', main_frame),
        (r'^workspace$', workspace),

        (r'^queries_constructor_ui$', queries_constructor_ui),
        (r'^reports_constructor_ui$', reports_constructor_ui))

def main_frame(request):
    """
    Возвращает главное окно приложения с фреймом внутри.
    """

    win = ConstructorWindow(src='/workspace')
    return ExtUIScriptResult(data=win).get_http_response()

def workspace(request):
    """
    То, что будет загружено во фрейм главного окна конструктора
    """

    context = django_template.Context({
        'title': 'КЗиО',
        'user': request.user
    })

    template = django_template.loader.get_template('constructor_menu.html')
    return HttpResponse(template.render(context))

def queries_constructor_ui(request):
    """
    Генерация вкладки запросы
    """

    context = django_template.Context({
        'row_data_url': m3_urls.get_url(query_actions.GetRowsDataAction),
        'new_row_url': m3_urls.get_url(query_actions.QueryConstructorPanelAction),
        'edit_row_url': m3_urls.get_url(query_actions.QueryConstructorPanelAction),
        'delete_row_url': m3_urls.get_url(query_actions.DeleteRowAction)
    })

    template = django_template.loader.get_template('constructor_workspace.html')

    return HttpResponse(template.render(context))

def reports_constructor_ui(request):
    """
    Генерация вкладки отчеты
    """

    context = django_template.Context({
        'row_data_url': m3_urls.get_url(report_actions.GetRowsDataAction),
        'new_row_url': m3_urls.get_url(report_actions.ReportPrintPanelAction),
        'edit_row_url': m3_urls.get_url(report_actions.ReportPrintPanelAction),
        'delete_row_url': m3_urls.get_url(report_actions.DeleteRowAction),
        'build_report_url': m3_urls.get_url(report_actions.ReportBuildWindow)
    })

    template = django_template.loader.get_template('constructor_workspace.html')

    return HttpResponse(template.render(context))