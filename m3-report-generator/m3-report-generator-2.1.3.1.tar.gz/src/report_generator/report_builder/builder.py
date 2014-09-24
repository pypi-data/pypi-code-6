#coding: utf-8

import os
import uuid
from tempfile import gettempdir

from django.db.backends import settings as django_settings

from sqlalchemy.exc import DataError

from simple_report.report import SpreadsheetReport, DocumentReport
from simple_report.converter.open_office import OpenOfficeConverter

from django.conf import settings

from report_generator.constructor_settings import (REPORT_DIR,
                                                   OPENOFFICE_SERVER_PORT)
from report_generator.exceptions import ReportGeneratorError, EntityException
from report_generator.core.builder import AlchemyQueryBuilder
from report_generator.query_builder.proxy import QueryProxy
from report_generator.report_builder.api import TemplateSectionWriter
from report_generator.report_builder.enums import (ReportType,
                                                   DocumentResultFileTypes,
                                                   TableDocumentResultFileTypes)
from report_generator.report_builder.models import Report
from report_generator.report_builder.proxy import ReportProxy, TemplateProxy

class ReportBuilder(object):
    """
    Сборка отчета
    """

    def __init__(self, report_key, params, result_format):

        assert report_key
        assert result_format
        assert (result_format in DocumentResultFileTypes.values or
                result_format in TableDocumentResultFileTypes.values), u'Неизвестный формат'

        self.report_key = report_key
        self.params = params
        self.result_format = result_format

        self.report = None
        self.data = {}

    def build(self):
        """
        """

        self._get_report()
        self._get_data()
        return self._report_building()

    def _get_report(self):
        """
        """

        try:
            report = Report.objects.get(report_key=self.report_key)
        except Report.DoesNotExist:
            raise ReportGeneratorError(u'Не найден отчет, который вы пытаетесь построить')

        self.report = report

    def _get_data(self):
        """
        """

        for alchemy_query in self._get_alchemy_queries():
            try:
                self.data[alchemy_query.name] = dict(entity=alchemy_query,
                                         data = alchemy_query.get_data(self.params))
            except EntityException, e:
                raise ReportGeneratorError(unicode(e))
            except DataError:
                raise ReportGeneratorError(
                    u'Произошла ошибка в исполняемом SQL-запросе. Возможно, '
                    u'причина в том, что типы параметров на форме составления '
                    u'запроса и соответствующего параметра БД не совпадают. '
                    u'Обратитесь к составителю запросов.')

    def _get_alchemy_queries(self):
        """
        """

        queries_ids = ReportProxy.get_queries_ids(self.report)
        queries_proxy = QueryProxy.get_queries(queries_ids)
        entity_cache = {}
        return (AlchemyQueryBuilder(
            name=query_proxy.id,
            json_query=query_proxy.json_query,
            entity_cache=entity_cache,
            join_removal=getattr(settings, 'REPORT_GENERATOR_JOIN_REMOVAL', False),
        ).build() for query_proxy in queries_proxy)


    def _report_building(self):
        """
        """

        template = self.report.template
        if not template.file:
            raise ReportGeneratorError(u'У отчета не задан файл шаблона')

        document_type = template.document_type

        try:
            if document_type == ReportType.TABLE:
                return self._prepare_spreadsheet(template)
            elif document_type == ReportType.DOCUMENT:
                return self._prepare_document(template)
            else:
                raise ReportGeneratorError(u'Неверное расширение шаблона')
        except ReportGeneratorError, e:
            raise ReportGeneratorError(u'На сервере произошла ошибка: %s' %e.message)

    def _prepare_document(self, template):
        """
        Подготавливает текстовый документ
        """

        # Бабахаем копию шаблона
        temp_file_name = os.path.join(gettempdir(), template.file_name)

        with open(temp_file_name, 'w+b') as tfile:
            tfile.write(template.file.read())

        report = DocumentReport(temp_file_name, converter=OpenOfficeConverter(port=OPENOFFICE_SERVER_PORT))

        sections = TemplateProxy.get_json_sections(template)

        if not sections:
            raise ReportGeneratorError(u'Шаблон составлен неверно: нет ни одной секции')

        # В текстовых отчетах понятие секции формально
        section = sections[0]

        query_template_data = {}

        # В текстовый документ выводим только одиночные записи
        query_data = self.data[section.get('query_id')]['data'][0]

        for field in section.get('query').get('params'):
            query_template_data[field.get('template_field')[1:-1]] = unicode(query_data[field.get('name')])

        return self._return_file(report, ReportType.DOCUMENT, template, data=query_template_data)

    def _prepare_spreadsheet(self, template):
        """
        Подготавливаем таблицу
        """

        temp_file_name = os.path.join(gettempdir(), template.file_name)

        with open(temp_file_name, 'w+b') as tfile:
            tfile.write(template.file.read())

        report = SpreadsheetReport(temp_file_name, converter=OpenOfficeConverter(port=OPENOFFICE_SERVER_PORT))

        sections = TemplateProxy.get_json_sections(template)

        if not sections:
            raise ReportGeneratorError(u'Шаблон составлен не верно: нет ни одной секции')

        TemplateSectionWriter.fill_template(sections, report, self.data, self.report.subst_values)

        return self._return_file(report, ReportType.TABLE, template)

    def _return_file(self, report, type, template, data=None):
        """
        Занимается созданием файла отчета, и его отдачей
        """

        enum = ReportType.get_enum(type)
        result_file_enum_value = enum.values[self.result_format]

        file_name = template.file_name.split('\\')[-1]

        file_name_with_bad_extension = '%s_%s' % (uuid.uuid1(), file_name)

        #Меняем расширение файла на необходимое нам
        file_name = reduce(lambda x, y: x+y,
            file_name_with_bad_extension.split('.')[:-1])
        file_name = '%s.%s' % (file_name, result_file_enum_value['extension'])

        full_static_name = os.path.join(REPORT_DIR, file_name)

        full_abs_name = os.path.join(settings.PROJECT_ROOT, full_static_name)

        if type == ReportType.DOCUMENT:
            report.build(full_abs_name, data, file_type=result_file_enum_value['type'])

        elif type == ReportType.TABLE:
            report.build(full_abs_name, file_type=result_file_enum_value['type'])

        return full_static_name
