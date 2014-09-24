#coding: utf-8

import os
import datetime
from tempfile import gettempdir

from m3_ext.ui.icons import Icons

from simple_report.report import SpreadsheetReport, DocumentReport
from simple_report.converter.open_office import OpenOfficeConverter
from simple_report.xlsx.section import Section

import settings

from report_generator.constructor_settings import OPENOFFICE_SERVER_PORT
from report_generator.exceptions import ReportException, ReportGeneratorError
from report_generator.core.query_components import Param
from report_generator.core.helpers import get_packs
from report_generator.report_builder.models import SectionTypeOutput, SubstValues


class FieldType(object):
    """
    Класс для работы с параметрами
    """

    @classmethod
    def _get_items_types(cls):
        """
        """

        res = []
        for key, value in Param.get_type_choices():
            d = dict(type=key, verbose_name=value, type_values=[])
            if key == Param.DICTIONARY:
                d['type_values'] = get_packs()
            res.append(d)

        return res

    @classmethod
    def get_field_types(cls):
        """
        """

        types = FieldType._get_items_types()
        return [(ttype.get('type'), ttype.get('verbose_name'))
                        for ttype in types]

    @classmethod
    def get_field_type_values(cls, item_type):
        """
        """

        types = FieldType._get_items_types()

        for ttype in types:
            if ttype.get('type') == item_type:
                return [(type_value.get('name'), type_value.get('verbose_name'))
                            for type_value in ttype.get('type_values')]
        else:
            raise ReportException(u'Некоректный тип значения')


class TemplateRenderer(object):
    """
    Парсит шаблон
    """

    # Шаблоны документы
    WRITER_EXTENSIONS = ['docx', 'odt']

    # Шаблоны таблицы
    CALC_EXTENSIONS = ['xls', 'xlsx', 'ods']

    # Единственная секция для шаблона-документа
    # (вообще говоря для него не существует понятия секции)
    WRITER_SECTION_NAME = u'Поля документа'

    def __init__(self, file_name, file_object):
        assert file_name
        assert file_object and hasattr(file_object, 'read')

        self.file_name = file_name
        self.f_object = file_object

    def save_file(self):
        """
        Сохранеят файл
        Возвращает путь до сохранненого файла
        """

        temp_file_name = os.path.join(gettempdir(), self.file_name)

        with open(temp_file_name, 'w+b') as tfile:
            tfile.write(self.f_object.read())

        return temp_file_name

    def get_sections(self):
        """
        Возвращает секции и параметры в шаблоне с использованием темповых директорий
        """

        extension = self.file_name.split('.')[-1]
        if extension in self.WRITER_EXTENSIONS:
            return self._get_writer_sections()
        elif extension in self.CALC_EXTENSIONS:
            return self._get_calc_sections()
        else:
            raise ReportException(u"Расширение '%s' файла %s \
                не поддерживается" % (extension, self.file_name))

    def _get_writer_sections(self):
        """
        Возвращает набор полей, для совместимого документа с OO Writer
        """

        temp_file_name = self.save_file()

        document = DocumentReport(temp_file_name, converter=OpenOfficeConverter(port=OPENOFFICE_SERVER_PORT))

        root_node = dict(template_field=self.WRITER_SECTION_NAME,
            leaf=True,
            expanded=True,
            iconCls=Icons.FOLDER_BRICK)

        for param in document.get_all_parameters():
            d = dict(template_field=param,
                leaf=True,
                iconCls=Icons.BRICK_LINK,
                draggable=False)

            root_node.setdefault('children', []).append(d)

        return root_node,

    def _get_calc_sections(self):
        """
        Возвращает секции для совместимого документа с OO Calc
        """

        temp_file_name = self.save_file()

        sheet = SpreadsheetReport(temp_file_name, converter=OpenOfficeConverter(port=OPENOFFICE_SERVER_PORT))

        root_nodes = []
        for section_name, section in sheet.sections.items():
            root_node = dict(template_field=section_name,
                leaf=False,
                expanded=True,
                iconCls=Icons.FOLDER_BRICK)

            for param in section.get_all_parameters():
                d = dict(template_field=param,
                    leaf=True,
                    iconCls=Icons.BRICK_LINK,
                    draggable=False)

                root_node.setdefault('children', []).append(d)

            root_nodes.append(root_node)
        return root_nodes

# TODO необходимо отрефакторить данный класс
# Непонятно, что понаписано
class TemplateSectionWriter(object):
    """
    Класс инкапсулирует работу по выводу результатов запроса в шаблон
    """

    @classmethod
    def _get_section_tree_based_on_section(cls, section):
        # Создаем дерево секций. Каждый узел имеет вид:
        # 'section' - здесь храним обьект секции
        # 'exclude_list' - для каждой секции храним и пополняем список id-ров записей, которые уже присутствуют в выводимом шаблоне
        # 'visit' - флаг, который указывает посещался ли узел
        # 'sub_sections' - список подузлов, каждый элемент которого имеет туже структуру что и искомый узел.
        # 'record_num' - индекс последней записи. Если записей не было, то проставляем просто -1.
        section_tree = { 'section': section, 'exclude_list': [], 'visit': False, 'sub_sections': [], 'record_num': 0,
                         'template_param_indices': {}}
        queue = [section_tree]

        while queue:
            section_node = queue.pop(0)

            if not section_node['visit']:
                section_node['visit'] = True

                for sub_section in section_node['section'].get('sub_sections'):
                    section_child_node = { 'section': sub_section,
                                           'visit': False,
                                           'sub_sections': [],
                                           'record_num': 0,
                                           'template_param_indices': {}}
                    section_node['sub_sections'].append(section_child_node)
                    queue.append(section_child_node)

        return section_tree

    @classmethod
    def _get_section_orientation(cls, section):
        """
        Получаем ориентацию секции
        """

        return (Section.HORIZONTAL if section.get('type_output') == SectionTypeOutput.GORIZONTAL
                                 else Section.VERTICAL)

    @classmethod
    def _substitution_data_and_sections(cls, template_param_indices, request_data):
        """
        Сопоставляем секции и значения
        """

        query_template_data = {}

        for k, v in template_param_indices.items():
            # У медицины имеются поля datetime. Но simple_report не работает с ними.
            # Поэтому выдергиваем дату из времени и выводим только её.
            #
            # Как раз наоборот - с полями datetime simple_report работает,
            # но не с date
            rd = request_data[v]
            # if isinstance(request_data[v], datetime.datetime):
            #     rd = request_data[v].date()
            if isinstance(request_data[v], datetime.date):
                rd = datetime.datetime(*(request_data[v].timetuple()[:6]))

            query_template_data[k] = rd

        return query_template_data

    @classmethod
    def _calc_template_param_indices(cls, section_tree, data, subs_values):
        """
        Для каждого узла дерева секций вычисляем template_param_indices словари {'ИмяПараметра': 'ИмяПоля'}
        Производим подстановку значений
        """

        section_tree['visit'] = False
        queue = [section_tree]

        subs_values = subs_values.get_subst_values()
        # import pdb; pdb.set_trace()
        while queue:
            section_node = queue.pop(0)

            if not section_node['visit']:
                q_id = section_node['section'].get('query_id')
                if q_id is None:
                    continue
                query = data[q_id]
                query_data = query['data']
                sql_query = query['entity']
                fields_names = [
                    field.get_name() for field
                    in sql_query.get_select_fields()
                ]

                groupby = sql_query.group_by

                if groupby:
                    if groupby.aggregate_fields:
                        for func_field in groupby.aggregate_fields:
                            field = func_field.field
                            fields_names.append(
                                field.alias
                            )

                for field in section_node['section'].get('query').get('params'):

                    for j, sub_val in enumerate(subs_values):
                        if (field.get('query_id') == sub_val.get('query_id') and
                            field.get('name') == sub_val.get('verboseName')):
                            j1 = fields_names.index(field.get('name'))
                            for i, a in enumerate(query_data):

                                query_data[i] = list(query_data[i]) 
                                condition = sub_val.get('condition')
                                result = sub_val.get('result')
                                subst_value = sub_val.get('subst_value')
                                for b in a:
                                    if condition == 'eq':
                                        if unicode(b).lower() == result.lower():
                                            query_data[i][j1] = subst_value
                                    if condition == 'ne':
                                        if unicode(b).lower() != result.lower():
                                            query_data[i][j] = subst_value
                                    if condition == 'lt':
                                        if unicode(b).lower() < result.lower():
                                            query_data[i][j] = subst_value
                                    if condition == 'le':
                                        if unicode(b).lower() <= result.lower():
                                            query_data[i][j] = subst_value
                                    if condition == 'gt':
                                        if unicode(b).lower() > result.lower():
                                            query_data[i][j] = subst_value
                                    if condition == 'ge':
                                        if unicode(b).lower() >= result.lower():
                                            query_data[i][j] = subst_value

                                query_data[i] = tuple(query_data[i])

                    # try:

                    #FIXME поправить, когда будет возможность
                    # Если поля нет в списке (ds0),
                    # а это может случиться, если поле - ForeignKey,
                    # то попробуем найти поле ds0_id

                    field_name = field.get('name')
                    if field_name in fields_names:
                        fname = field_name
                    else:
                        fname = field_name + '_id'
                    section_node['template_param_indices'][field.get('template_field')[1:-1]] = fields_names.index(fname)
                    # except ValueError:
                    #     continue

                for child_node in section_node['sub_sections']:
                    if child_node['section'].get('query_id') == section_tree['section'].get('query_id'):
                        child_node['pokudo'] = section_tree['record_num'] - 1
                    child_node['visit'] = False
                    queue.append(child_node)

    @staticmethod
    def fill_template(sections, report, data, subs_values):
        """
        Заполняем шаблон результатами запроса
        """

        for section in sections:

            section_tree = TemplateSectionWriter._get_section_tree_based_on_section(section)

            TemplateSectionWriter._calc_template_param_indices(section_tree, data, subs_values)

            q_id = section_tree['section'].get('query_id')
            if q_id is not None:
                query = data[q_id]
                query_data = query['data']
            else:
                query_data = [{}]

            # Если условие выполняется, то секция является деревом секций
            if section_tree['section'].get('sub_sections'):

                for request_data in query_data:
                    section_tree['visit'] = False
                    queue = [section_tree]

                    while queue:
                        section_node = queue.pop(0)

                        if not section_node['visit']:
                            doc_section = report.get_section(section_node['section'].get('section'))

                            # Метод вывода
                            write_method = None

                            # Если у секции есть подсекции, то выводим одну запись и переходим к следующему узлу
                            if section_node['sub_sections'] and section_node == section_tree:
                                write_method = TemplateSectionWriter._master_record_write
                            elif (section_tree['section'].get('query_id') == section_node['section'].get('query_id')
                                  and not section_node['sub_sections']):
                                write_method = TemplateSectionWriter._detail_records_write
                            # В противном случае выводим подытоги
                            else:
                                write_method = TemplateSectionWriter._one_record_write

                            if write_method:
                                query = data[section_node['section'].get('query_id')]
                                query_data = query['data']
                                TemplateSectionWriter._template_section_writer(section_node, query_data, doc_section,
                                    method=write_method)

                            for child_node in section_node['sub_sections']:
                                if child_node['section'].get('query_id') == section_tree['section'].get('query_id'):
                                    child_node['pokudo'] = section_tree['record_num'] - 1
                                child_node['visit'] = False
                                queue.append(child_node)

            # В противном случае, секция является элементарной и мы просто выводим в неё
            # все соответствующие ей записи.
            else:
                doc_section = report.get_section(section_tree['section'].get('section'))
                TemplateSectionWriter._template_section_writer(section_tree, query_data, doc_section,
                    method=TemplateSectionWriter._all_records_write)

    @classmethod
    def _template_section_writer(cls, section_node, query_data, doc_section, method):
        """
        Шаблон вывода в метод. Шаблонный метод с композицией вместо наследования
        method() - метод вывода _master_record_write, _details_records_write, _one_record_write, _all_records_write
        """
        assert method in [TemplateSectionWriter._master_record_write, TemplateSectionWriter._detail_records_write,
                          TemplateSectionWriter._one_record_write, TemplateSectionWriter._all_records_write]

        if isinstance(query_data, list):

            oriented = cls._get_section_orientation(section_node['section'])

            method(section_node, query_data, doc_section, oriented)

        elif isinstance(query_data, dict):
            raise ReportGeneratorError(u'Запрос составлен неверно: '
                                       u'запрос пытается вставить в секцию для множественного '
                                       u'вывода одиночный объект.')
        else:
            raise ReportGeneratorError(u'Запрос составлен неверно: '
                                       u'непонятный тип ответа')

    @classmethod
    def _all_records_write(cls, section_node, query_data, doc_section, oriented):
        """
        Простой вывод всех записей в секцию
        """

        template_param_indices = section_node.get('template_param_indices')

        for request_data in query_data:

            query_template_data = cls._substitution_data_and_sections(template_param_indices, request_data)

            doc_section.flush(query_template_data, oriented)

    @classmethod
    def _one_record_write(cls, section_node, query_data, doc_section, oriented):
        """
        Вывод одной записи из результатов запроса
        """

        template_param_indices = section_node.get('template_param_indices')

        try:
            request_data = query_data[section_node['record_num']]
        except IndexError:
            return

        query_template_data = cls._substitution_data_and_sections(template_param_indices, request_data)

        doc_section.flush(query_template_data, oriented)

        section_node['record_num'] += 1

    @classmethod
    def _master_record_write(cls, section_node, query_data, doc_section, oriented):
        """
        Вывод мастер записи
        """

        template_param_indices = section_node.get('template_param_indices')

        begin_record_index = section_node.get('record_num')
        try:
            request_data = query_data[begin_record_index]
        except IndexError:
            return

        query_template_data = cls._substitution_data_and_sections(template_param_indices, request_data)

        while True:
            try:
                request_data = query_data[begin_record_index + 1]
            except IndexError:
                break
            query_template_data_next = cls._substitution_data_and_sections(template_param_indices, request_data)

            if query_template_data_next == query_template_data:
                begin_record_index += 1
            else:
                break

        end_record_index = begin_record_index

        doc_section.flush(query_template_data, oriented)

        section_node['record_num'] = end_record_index + 1

    @classmethod
    def _detail_records_write(cls, section_node, query_data, doc_section, oriented):
        """
        Вывод записи-детали
        """

        template_param_indices = section_node.get('template_param_indices')

        begin_record_index = section_node['record_num']
        end_record_index = section_node['pokudo']

        while begin_record_index <= end_record_index:

            try:
                request_data = query_data[begin_record_index]
            except IndexError:
                return

            query_template_data = cls._substitution_data_and_sections(template_param_indices, request_data)

            doc_section.flush(query_template_data, oriented)

            begin_record_index += 1

        section_node['record_num'] = end_record_index + 1