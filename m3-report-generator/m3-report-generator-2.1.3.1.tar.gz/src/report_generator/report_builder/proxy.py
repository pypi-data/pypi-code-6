#coding: utf-8

import json
import uuid

from django.db import transaction

from report_generator.exceptions import ReportGeneratorError
from report_generator.core.helpers import action_on_tree, serialize_result
from report_generator.core.proxy import (ReportComponentOneToOneProxy,
                                    ReportComponentManyToOneProxy)
from report_generator.query_builder.proxy import QueryProxy
from report_generator.report_builder.models import (Report, ReportQuery, Template,
                                               FormField, SubstValues)
from report_generator.report_builder.api import TemplateRenderer
from report_generator.report_builder.enums import ReportType


class ReportProxy(object):
    """
    Прокси для работы с отчетами
    """

    def __init__(self, report_id, report=None):

        self.id = report_id
        self.report = report # constructor.report_builder.models.Report

        # При работе часто обращаемся с запросами данного отчета.
        # Поэтому сделаем это один раз в конструкторе
        # Идентификаторы запросов, которые задействованы в отчете
        queries_ids = self.report.queries.values_list('query_id', flat=True)
        self.queries_proxy = QueryProxy.get_queries(queries_ids)

    @classmethod
    @transaction.commit_on_success
    def save(cls, context, file):
        """
        Сохранение
        :param: context - контекст запроса на сохранение
        :param: template_file - имя файла шаблона
        """

        report_id = getattr(context, 'id') if hasattr(context, 'id') else None
        name = context.name
        file_name = context.template
        form_params = context.form_params
        queries_params = context.queries_params
        sections = context.sections
        subs_values = context.subs_values

        report, created = Report.objects.get_or_create(id=report_id)

        report.name = name
        # Ключ может отсутствовать в контексте
        if hasattr(context, 'report_key'):
            # Проверка уникальности ключа для нового отчета
            unique = False if Report.objects.filter(report_key=context.report_key).exists() else True
            if unique:
                # Если уникален, то записываем его.
                report.report_key = context.report_key
        report.save()

        QueriesParamsProxy.save(report, queries_params)
        FormFieldsProxy.save(report, form_params)
        SubstitutionValuesProxy.save(report, subs_values)
        TemplateProxy.save(report, file, file_name, sections)

        return report.id

    @classmethod
    @transaction.commit_on_success
    def delete(cls, ids):
        """
        Удаление отчетов
        :param ids: - список ID-шников
        """

        Report.objects.filter(id__in=ids).delete()

    @classmethod
    def load(cls, id):
        """
        Загрузка заместителя отчета по ID
        """

        try:
            report = Report.objects.select_related('template', 'queries',
                    'form_fields', 'subst_values').all().get(id=id)
        except Report.DoesNotExist:
            raise ReportGeneratorError(u'Отчет не найден')

        return ReportProxy(report_id=report.id, report=report)

    def get_name(self):
        """Получение имени отчета"""
        return self.report.name

    def get_document_type(self):
        """Получение типа документа"""
        return self.report.get_document_type()

    def get_report_key(self):
        """Получение ключа отчета"""
        return self.report.report_key

    def get_template_name(self):
        """Получение имени шаблона"""
        return self.report.get_template_name()

    def get_template_file(self):
        """Получение файла с шаблоном"""
        return self.report.get_template_file()

    @serialize_result
    def get_all_sections(self):
        """Получение всех секций"""
        template_name = self.get_template_name()
        template_file = self.get_template_file()

        return TemplateProxy.get_sections(template_name, template_file)

    @serialize_result
    def get_used_sections(self):
        """Получение используемых секций"""
        return self.report.get_sections()

    @serialize_result
    def get_select_data(self):
        """Получение данных"""
        return [QueryProxy.get_select_data(proxy) for proxy in self.queries_proxy]

    @serialize_result
    def get_all_report_params(self):
        """
        Параметры отчета
        """

        params = []
        for proxy in self.queries_proxy:
            param = QueryProxy.get_params_data(proxy)
            # Удаляем детей, т.к. они добавлены в отчет и в дереве всех параметров отображаться не должны
            # Если конечно в запросе есть параметры.
            if 'children' in param:
                del param['children']
            params.append(param)

        return params

    @serialize_result
    def get_matching_fields(self):
        """
        Поля сопоставления
        """

        sections = self.report.get_sections()

        res = []
        for section in sections:

            def action(section, kwargs):
                d = dict(expanded=True,
                         leaf=False,
                         name=section.get('name'),
                         query_id=section.get('query_id'),
                         template_field=section.get('section'))

                query = section.get('query')
                if query:
                    for param in query.get('params'):
                        d.setdefault('children', []).append(
                            dict(leaf=True, name=param.get('name'),
                                 query_id=param.get('query_id'),
                                 template_field=param.get('template_field')))

                kwargs.get('res').append(d)

            action_on_tree(element=section, sub_element_key='sub_sections',
                           action=action, res=res)

        return res

    def get_form_fields(self):
        """
        Получение полей формы
        """

        form_fields = self.report.form_fields.values_list('json_fields', flat=True)

        fields = []
        form_parameters = {}
        query_parameters = {}
        for form_field in form_fields:
            field = json.loads(form_field)

            root_id = str(uuid.uuid4())[:8]
            field['id'] = root_id
            field['expanded'] = True
            field['leaf'] = False

            query_parameters.update(self._get_query_params(field.get('params')))

            # Параметры формы
            form_parameters[root_id] = field

            # Парметры как дочерные узлы к полям формы
            field['children'] = [dict(name=param.get('name'), query_id=param.get('query_id'), leaf=True)
                                 for param in field.get('params')]

            fields.append(field)

        return json.dumps(fields), json.dumps(form_parameters), json.dumps(query_parameters)

    def _get_query_params(self, params):
        res = {}
        for param in params:
            res.setdefault(param.get('query_id'), []).append(param.get('name'))
        return res

    @serialize_result
    def get_subst_fields(self):

        return self.report.get_subst_values()

    @classmethod
    def get_queries_ids(cls, report):
        report_queries = report.queries.all()

        return [report_query.query_id for report_query in report_queries]


class TemplateProxy(ReportComponentOneToOneProxy):
    """
    Прокси для работы с шаблонами
    """

    model_cls = Template

    @classmethod
    def get_sections(cls, template, file_obj, renderer=TemplateRenderer):
        """Получение секций"""
        return renderer(template, file_obj).get_sections()

    @classmethod
    def _prepare_instance(cls, report, template, file, file_name, sections):

        cls._sort_section(sections)

        if not isinstance(sections, basestring):
            sections = json.dumps(sections)

        document_type = ReportType.get_type(file_name.split('.')[-1])

        if file:
            template.file = file

        template.file_name = file_name
        template.document_type = document_type
        template.report = report
        template.json_sections = sections

        return template

    @classmethod
    def get_json_sections(cls, template):
        """
        Получение секций в формате json
        :param template:
        """
        return json.loads(template.json_sections)

    @staticmethod
    def _sort_key(section):
        return int(section.get('priority_output'))

    @classmethod
    def _sort_section(cls, sections):

        sections.sort(key=cls._sort_key)

        for section in sections:
            cls._sort_section(section.get('sub_sections'))


class SubstitutionValuesProxy(ReportComponentOneToOneProxy):
    """
    """

    model_cls = SubstValues

    @classmethod
    def _prepare_instance(cls, report, instance, subs_values):

        if not isinstance(subs_values, basestring):
            subs_values = json.dumps(subs_values)

        instance.report = report
        instance.json_subst_values = subs_values

        return instance


class QueriesParamsProxy(ReportComponentManyToOneProxy):

    model_cls = ReportQuery

    @classmethod
    def _prepare_instance(cls, report, instance, param):

        instance.query_id = param.get('query_id')

        return instance


class FormFieldsProxy(ReportComponentManyToOneProxy):

    model_cls = FormField

    @classmethod
    def _prepare_instance(cls, report, instance, param):

        if not isinstance(param, basestring):
            param = json.dumps(param)

        instance.json_fields = param

        return instance
