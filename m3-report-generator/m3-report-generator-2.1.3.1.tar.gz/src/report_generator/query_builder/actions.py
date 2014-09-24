#coding: utf-8
import json

from django.core.exceptions import ValidationError
from django.conf import settings

from m3.actions.results import OperationResult, PreJsonResult
from m3.actions import ACD
from m3.actions.dicts.simple import BaseDictionaryModelActions, DictRowsAction, ListDeleteRowAction
from m3 import actions
from m3_legacy import logger
from m3_ext.ui.results import ExtUIScriptResult

from report_generator.exceptions import ReportGeneratorError
from report_generator.core.builder import EntityTypes, AlchemyQueryBuilder
from report_generator.core.query_components import SortOrder
from report_generator.report_builder.models import Report, FormField
from report_generator.query_builder.entity_proxy import ModelEntityUIProxy, QueryEntityUIProxy
from report_generator.renderer import ExtPanelRenderer
from report_generator.query_builder.proxy import QueryProxy

import ui
import models

class QueryConstructorPack(BaseDictionaryModelActions):
    """
    Пак работы с конструктором запросов
    """

    url = '/qc-pack'

    shortname = 'query-constructor'
    title = u'Запросы'
    verbose_name = u'Коструктор запросов'
    edit_window = ui.QueryBuilderPanel

    model = models.Query

    list_columns = [('name', u'Наименование')]
    filter_fields = ['name']

    def __init__(self):
        super(QueryConstructorPack, self).__init__()
        self.actions.extend([QueryConstructorPanelAction(),
                             EntitiesListAction(),
                             EntityItemsListAction(),
                             SelectConnectionWindowAction(),
                             ConditionWindowAction(),
                             ShowQueryTextAction(),
                             SaveQueryAction(),
                             DeleteParamsAction(),
                             GetRowsDataAction(),
                             DeleteRowAction()
                            ])


class GetRowsDataAction(DictRowsAction):
    """
    Переопределен для использования в app_meta
    """
    pass


class DeleteRowAction(ListDeleteRowAction):
    """
    Переопределенный экшен удаления запросов
    """

    def context_declaration(self):
        return [ACD(name='id', type=str, required=True,
            verbose_name=u'Идентификаторы запроса')]

    def run(self, request, context):
        list_ids =  context.id.split(',')
        try:
            QueryProxy.delete_query(list_ids)
        except ReportGeneratorError, e:
            return OperationResult(success=False, message=unicode(e))

        return PreJsonResult({'success': True})


class QueryConstructorPanelAction(actions.Action):
    """
    Получение окна конструктора запросов
    """

    url = '/edit-window'
    shortname = 'report-generator-edit-window'

    def context_declaration(self):
        return [ACD(name='id', type=str, verbose_name=u'Идентификатор запросов')]

    def run(self, request, context):

        params = {'select_connections_url': SelectConnectionWindowAction.absolute_url(),
                  'entity_items_url': EntityItemsListAction.absolute_url(),
                  'condition_url': ConditionWindowAction.absolute_url(),
                  'query_text_url': ShowQueryTextAction.absolute_url(),
                  'save_query_url': SaveQueryAction.absolute_url(),
                  'check_and_del_params_url': DeleteParamsAction.absolute_url(),
                  'query_title': EntityTypes.get_entity_type_title(EntityTypes.QUERY),
                  'model_title': EntityTypes.get_entity_type_title(EntityTypes.MODEL),
                  'query_type': EntityTypes.QUERY,
                  'model_type': EntityTypes.MODEL}

        panel = ui.QueryBuilderPanel(params= params)

        panel.set_data_to_store_combo_sort([(order_code, order_title) for (order_code, order_title) in SortOrder.VALUES])

        if hasattr(context, 'id') and getattr(context, 'id'):
            query = QueryProxy.load_query(context.id) # QueryProxy instance
            panel.configure_panel(query)

        panel.rendered = ExtPanelRenderer(component=panel)

        return ExtUIScriptResult(data=panel.rendered)


class EntitiesListAction(actions.Action):
    """
    Загрузка всех сущностей.
    """
    url = '/entities-list'
    shortname = 'report-generator-entities-list'

    def run(self, request, context):

        entities = ModelEntityUIProxy.get_entities()
        queries = QueryEntityUIProxy.get_entities()
        return actions.JsonResult(json.dumps([entities, queries]))


class EntityItemsListAction(actions.Action):
    """
    Загрузка полей сущностей.
    """
    url = '/entity-items-list'
    shortname = 'report-generator-entity-items-list'

    def context_declaration(self):
        return [ACD(name='models', type=object, required=True),
                ACD(name='queries', type=object, required=True)]

    def run(self, request, context):
        res = []
        res.extend(ModelEntityUIProxy.get_entities_fields(context.models))
        res.extend(QueryEntityUIProxy.get_entities_fields(context.queries))
        return actions.JsonResult(json.dumps(res))


class SelectConnectionWindowAction(actions.Action):
    """
    Запрос на получение окна выбора связи
    """
    url = '/select-connection-window'
    shortname = 'report-generator-select-connection'

    def run(self, request, context):
        win = ui.SelectConnectionsWindow()
        return ExtUIScriptResult(win)


class ConditionWindowAction(actions.Action):
    """
    Запрос на получение окна задания условий
    """
    url = '/condition-window'
    shortname = 'report-generator-condition'

    def run(self, request, context):
        win = ui.ConditionWindow()
        return ExtUIScriptResult(win)


class ShowQueryTextAction(actions.Action):
    """
    Возвращает sql текст запроса
    """
    url = '/sql-query'
    shortname = 'report-generator-sql-query'

    def context_declaration(self):
        return [ACD(name='objects', type=object, required=True)]


    def run(self, request, context):
        #def _inner(self, request, context):
        entity_cache = {}
        query = AlchemyQueryBuilder(
            name='',
            json_query=context.objects,
            join_removal=getattr(settings, 'REPORT_GENERATOR_JOIN_REMOVAL', False),
            entity_cache=entity_cache
        ).build()

        win = ui.SqlWindow()
        win.set_source(query.get_raw_sql())
        del entity_cache

        return ExtUIScriptResult(win)
        #cProfile.runctx('_inner(self, request, context)', globals(), locals(),
        #                filename='/home/khalikov/wp.txt')
        #return _inner(self, request, context)


class SaveQueryAction(actions.Action):
    """
    Сохранение полученного запроса
    """

    url = '/save'
    shortname = 'report-generator-save'

    def context_declaration(self):
        return [ACD(name='objects', type=object, required=True,
                    verbose_name=u'Тело запроса'),
                ACD(name='query_name', type=str, required=True,
                    verbose_name=u'Наименование запроса'),
                ACD(name='id', type=str, verbose_name=u'Идентификатор запроса'),
                ]

    def run(self, request, context):

        query = context.objects
        query_id = getattr(context, 'id', None)

        try:
            query_id = QueryProxy(query_id=query_id, query_name=context.query_name, json_query=query).save_query()
        except ValidationError:
            logger.exception()
            return OperationResult(success=False,
                message=u'Не удалось сохранить запрос')
        except ReportGeneratorError, e:
            return OperationResult(success=False,
                message=u'Не удалось сохранить запрос: %s' %unicode(e))

        if hasattr(context, 'id'):
            return OperationResult()
        else:
            return actions.JsonResult(json.dumps(dict(success=True, id=str(query_id))))


class DeleteParamsAction(actions.Action):
    """
    Проверяет присутствуют ли удаляемые параметры в отчетах
    """

    url = '/delete'
    shortname = 'report-generator-check'

    # Определяет поведение в случае валидации
    CHECK = 'check'

    # Определяет поведение в случае удаления
    DELETE = 'delete'

    def context_declaration(self):
        return [
            ACD(name='params_names', type=object, required=True,
                verbose_name=u'Идентификатор удаляемого параметра'),
            ACD(name='query_id', type=int, required=True,
                verbose_name=u'Идентификатор запроса'),
            ACD(name='operation', type=str, required=True,
                verbose_name=u'Операция'),
            ]

    def run(self, request, context):

#        # Список идентификаторов и имен отчетов, которые используют данный запрос
#        reports = Report.objects.select_related('queries').filter(queries__query_id=context.query_id).values('id', 'name')
#        reports_ids = [report.get('id') for report in reports]
#        # Поля с параметрами привязанные, к данным отчетам.
#        form_fields = FormField.objects.filter(report__in=reports_ids).values_list('json_fields', flat=True)
#        # Перекодируем в JSON формат, т.к. в БД хранится строка
#        form_fields = [json.loads(form_field) for form_field in form_fields]
#        # Имена параметров
#        params = context.params_names
#
#        if context.operation == self.CHECK:
#            return self._check_params(reports, form_fields, params)

        return actions.OperationResult()

#    def _check_params(self, reports, form_fields, params):
#        message_report = []
#
#        reports_ids = []
#        for form_field in form_fields:
#            for param_name in self._get_params_names(form_field):
#                if param_name in params:
#                    reports_ids.append(form_field)
#
#    def _get_params_names(self, form_field):
#        for param in form_field.get('params'):
#            yield param.get('name')