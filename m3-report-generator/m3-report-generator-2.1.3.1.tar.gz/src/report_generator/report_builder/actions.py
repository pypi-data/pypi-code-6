#coding: utf-8

import os
import json
from tempfile import gettempdir

from django.http import HttpResponse

from m3.actions.dicts.simple import BaseDictionaryModelActions, DictRowsAction, ListDeleteRowAction
from m3 import actions
from m3.actions import ACD
from m3_ext.ui.results import ExtUIScriptResult

from report_generator.api.api import build_report
from report_generator.exceptions import ReportException, ReportGeneratorError
from report_generator.renderer import ExtPanelRenderer
from report_generator.core.query_components import Param
from report_generator.query_builder.entity_proxy import QueryEntityUIProxy
from report_generator.query_builder.proxy import QueryProxy
from report_generator.report_builder.models import Report
from report_generator.report_builder import ui
from report_generator.report_builder.proxy import ReportProxy
from report_generator.report_builder.api import FieldType, TemplateRenderer
from report_generator.report_builder.enums import MimeTypes

class ReportPack(BaseDictionaryModelActions):
    """
    Экшенпак работы с конструктором отчетов
    """

    shortname = 'report-constructor'

    title = u'Отчеты'
    verbose_name = u'Отчеты'

    list_columns = [('name', u'Наименование')]
    filter_fields = ['name']

    model = Report

    def __init__(self):
        super(ReportPack, self).__init__()
        self.actions.extend([ReportPrintPanelAction(),
                             ReportSaveAction(),
                             GetQueriesAction(),
                             TemplateRenderAction(),
                             TypeOutputWindow(),
                             QueryDataAction(),
                             MatchingWindowAction(),
                             SubstitutionValueWindow(),
                             ReportEditParamsWindowAction(),
                             ReportTypesItemsAction(),
                             GetRowsDataAction(),
                             DeleteRowAction(),
                             TemplateDownloadAction(),
                             ReportBuildWindow(),
                             ReportBuild()])


class GetRowsDataAction(DictRowsAction):
    """
    Переопределен для использования в app_meta
    """
    pass


class DeleteRowAction(ListDeleteRowAction):
    """
    Удаление отчета
    """

    def context_declaration(self):
        return [ACD(name='id', type=str, required=True,
                    verbose_name=u'Идентификатор отчета')]

    def run(self, request, context):
        list_ids = context.id.split(',')
        ReportProxy.delete(list_ids)
        return actions.PreJsonResult({'success': True})


class ReceiveReportForm(actions.Action):
    """
    Формирование отчета
    """


class ReportPrintPanelAction(actions.Action):
    """
    Окно создания/редактирования отчетов
    """

    url = '/edit-window'
    shortname = 'm3-print-report-edit-window'

    def context_declaration(self):
        return [ACD(name='id', type=str, required=False,
                verbose_name=u'Идентификатор отчета')]

    def run(self, request, context):

        params = {
            'template_load_url': TemplateRenderAction.absolute_url(),
            'type_output_url': TypeOutputWindow.absolute_url(),
            'query_data_url': QueryDataAction.absolute_url(),
            'matching_url': MatchingWindowAction.absolute_url(),
            'subst_url': SubstitutionValueWindow.absolute_url(),
            'condition_url': ReportEditParamsWindowAction.absolute_url(),
            'download_url': TemplateDownloadAction.absolute_url()
        }

        panel = ui.PrintReportPanel(params=params)

        if hasattr(context, 'id') and getattr(context, 'id'):
            query = ReportProxy.load(context.id) # ReportProxy instance
            panel.configure_panel(query)

        panel.renderer = ExtPanelRenderer(component=panel)

        return ExtUIScriptResult(data=panel.renderer)


class TemplateDownloadAction(actions.Action):
    """
    Скачивание шаблона
    """

    url = '/template-download'
    shortname = 'template_download'

    def context_declaration(self):
        return [ACD(name='file_name', required=True, type=str),
                ACD(name='report_id', required=True, type=str)]

    def run(self, request, context):
        """
        """

        file_name = context.file_name
        full_file_name = os.path.join(gettempdir(), file_name)
        file_extension = file_name.split('.')[-1]

        response = HttpResponse(mimetype=MimeTypes.values[file_extension])
        response['Content-Disposition'] = 'attachment; filename=%s' % file_name

        with open(full_file_name, 'r') as f:
            response.write(f.read())

        return response


class SubstitutionValueWindow(actions.Action):
    """
    Окно подстановки значений
    """

    url = '/subst-window'
    shortname = 'report-generator-substitution-value'

    def run(self, request, context):
        win = ui.SubstitutionWindow()
        return ExtUIScriptResult(win)


class TypeOutputWindow(actions.Action):
    """
    Окно выбора типа вывода секции
    """

    url = '/get-type-output-window'
    shortname = 'report-type-output-window'

    def run(self, request, context):
        window = ui.TypeOutputWindow()
        return ExtUIScriptResult(window)


class GetQueriesAction(actions.Action):
    """
    Получение существующих запросов
    """

    url = '/get-queries'
    shortname = 'report-generator-get-queries'

    def run(self, request, context):

        queries = QueryEntityUIProxy.get_entities()

        return actions.JsonResult(json.dumps([queries]))


class QueryDataAction(actions.Action):
    """
    Получение запросов с полями и параметрами
    """

    url = '/get-data'
    shortname = 'report-generator-query-data'

    def context_declaration(self):
        return [ACD(name='query_id', type=str, required=True,
                    verbose_name=u'Идентификатор запроса')]

    def run(self, request, context):

        id, name = context.query_id.split('.')
        param_nodes, select_nodes = QueryProxy.get_query_data(id=id)
        res = dict(paramsNodes=param_nodes,
                   selectNodes=select_nodes)
        return actions.JsonResult(json.dumps(dict(data=res, success=True)))

class ReportEditParamsWindowAction(actions.Action):
    """
    Запрос на получнение окна редактирования параметров
    """

    url = '/edit-window-params'
    shortname = 'report-builder-edit-window-params'

    def run(self, request, context):
        params = {
            'type_value_items_url': ReportTypesItemsAction.absolute_url()
        }

        win = ui.PrintReportParamsWindow(
            types = FieldType.get_field_types(),
            params = params,
            type_number = Param.NUMBER,
            type_string = Param.STRING
        )

        return ExtUIScriptResult(win)


class ReportTypesItemsAction(actions.Action):
    """
    """

    url = '/type-items'
    shortname = 'report-builder-type-items'

    def context_declaration(self):
        return [ACD(name='type', type=int, required=True,
            verbose_name=u'Идентификатор типа значения')]

    def run(self, request, context):
        res = FieldType.get_field_type_values(context.type)
        return actions.JsonResult(json.dumps(dict(data=res, success=True)))


class MatchingWindowAction(actions.Action):
    """
    Запрос на получение окна сопоставления секций и полей запроса
    """
    url = '/matching-window'
    shortname = 'report-generator-matching'

    def run(self, request, context):
        win = ui.MatchingWindow()
        return ExtUIScriptResult(win)


class TemplateRenderAction(actions.Action):
    """
    Рендеринг шаблона
    """
    url = '/template-render'
    shortname = 'report-builder-template-render'

    def context_declaration(self):
        return [ACD(name='template', type=unicode, required=True,
            verbose_name=u'Название шаблона')]

    def run(self, request, context):
        file_object = request.FILES['file_template']
        root_nodes = TemplateRenderer(context.template, file_object).get_sections()
        return HttpResponse(json.dumps({'success': True, 'sections': root_nodes}))


class ReportBuildWindow(actions.Action):
    """
    """

    url = '/build-report-win'
    shortname = 'build-report-win'

    def context_declaration(self):
        return [ACD(name='id', type=int, required=True, verbose_name=u'Идентификатор отчета')]

    def run(self, request, context):
        report_proxy = ReportProxy.load(context.id)
        form_fields, _, __ = report_proxy.get_form_fields()
        form_fields = json.loads(form_fields)
        win = ui.ReportForm.build_win(report_proxy, form_fields, ReportBuild.absolute_url())
        return ExtUIScriptResult(win.renderer)


class ReportBuild(actions.Action):

    url = '/build-report'
    shortname = 'build-report'

    def context_declaration(self):
        return [ACD(name='report_key', type=str, required=True, verbose_name=u'Ключ отчета'),
                ACD(name='result_format', type=int, required=True, verbose_name=u'Формат отчета'),
                ACD(name='params', type=object, required=True, verbose_name=u'Параметры')]

    def run(self, request, context):

        content = build_report(context.report_key, context.result_format, context.params)
        file_name = content.split(os.path.sep)[-1]
        file_extension = content.split('.')[-1]

        response = HttpResponse(mimetype=MimeTypes.values[file_extension])
        response['Content-Disposition'] = 'attachment; filename=%s' % file_name

        with open(content, 'rb') as f:
            response.write(f.read())

        return response


class ReportSaveAction(actions.Action):
    """
    Сохранение отчета
    """

    url = '/save'
    shortname = 'report-builder-save'

    def context_declaration(self):
        return [ACD(name='id', type=str, required=False,
                    verbose_name=u'Идентификатор отчета'),
                ACD(name='template', type=unicode, required=True,
                    verbose_name=u'Название шаблона'),
                ACD(name='name', type=unicode, required=True,
                    verbose_name=u'Название отчета'),
                ACD(name='form_params', type=object, required=True,
                    verbose_name=u'Поля формы отчета'),
                ACD(name='queries_params', type=object, required=True,
                    verbose_name=u'Параметры запроса'),
                ACD(name='sections', type=object, required=True,
                    verbose_name=u'Секции'),
                ACD(name='subs_values', type=object, required=True,
                    verbose_name=u'Подстановка значений'),
                ACD(name='report_key', type=unicode, required=False,
                    verbose_name=u'Ключ отчета')]

    def run(self, request, context):
        template_file = request.FILES.get('file_template')

        try:
            id = ReportProxy.save(context, template_file)
        except (ReportException, ReportGeneratorError), msg:
            return actions.OperationResult(success=False,
                                           message=u'Не удалось сохранить объект: %s' % unicode(msg))

        if hasattr(context, 'id'):
            return actions.OperationResult()
        else:
            #Посылаем айдишник только что сохраненного объекта
            result = json.JSONEncoder().encode(dict(success=True, id=str(id)))
            return HttpResponse(content=result)