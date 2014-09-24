#coding: utf-8
import json

import threading
from abc import ABCMeta, abstractmethod
from django.conf import settings

sqlparse = None
try:
    import sqlparse
except ImportError:
    pass

from django.db.models import loading

from sqlalchemy import func as func_generator, bindparam
from sqlalchemy.sql.expression import (
    select, join, outerjoin, ColumnElement, true, false
)

from m3_legacy.datastructures import TypedList
from alchemy_wrapper import SQLAlchemyWrapper

from report_generator.exceptions import (DBTableNotFound, DBColumnNotFound,
                                    EntityNotFound, EntityException, ReportGeneratorError)
from report_generator.query_builder.proxy import QueryProxy
from report_generator.core.db_wrapper import WrapperBuilder

class BaseAlchemyEntity(object):
    """
    Базовая сущность запроса SQLAlchemy
    """

    __metaclass__ = ABCMeta

    _instance_cache = {}

    def __init__(self, id, alias = None, entity_cache=None):

        self.id = id
        self.alias = alias
        self._aliased_table = None
        self.entity_cache = entity_cache

        c = self.entity_cache.get((self.id, alias))
        if c:
            self.__dict__ = c.__dict__
        else:
            self.entity_cache[(self.id, alias)] = self
        # c = self._instance_cache.get((self.id, alias))
        # if c:
        #     self.__dict__ = c.__dict__
        # else:
        #     BaseAlchemyEntity._instance_cache[(self.id, alias)] = self

    @classmethod
    def _clear_instances(cls):
        for v in cls._instance_cache.values():
            v._aliased_table = None

    @classmethod
    def clear_instances(cls):
        """Очищение экземпляров моделей"""
        #Блокируем доступ другим потокам
        with threading.RLock():
            cls._clear_instances()

    @abstractmethod
    def _get_alchemy_table(self, params):
        """
        Возвращаем таблицу в формате SQLAlchemy
        """
    @abstractmethod
    def get_alchemy_field(self, field_name, params):
        """
        Возвращает поле таблицы в формате SqlAlchemy
        """
    def get_subquery(self, params):
        """
        Возвращает подзапрос с алиасом. Параметры params передаются
        чтобы модифицировать запрос в зависимости от данных
        """
        if self._aliased_table is None:
            table = self._get_alchemy_table(params)
            self._aliased_table = table.alias(self.alias)
        return self._aliased_table


class TableEntity(BaseAlchemyEntity):
    """
    Для обозначения таблиц пришедших из БД
    """

    def __init__(self, id, alias=None, **kwargs):
        super(TableEntity, self).__init__(id, alias, kwargs['entity_cache'])

        self.wrapper = WrapperBuilder.build_wrapper()

    def _get_alchemy_table(self, params):

        # id_ = self.id.split('__')[0]
        id_ = self.id
        app_label, model_name = id_.split('.')
        model = loading.get_model(app_label, model_name)
        table_name = model._meta.db_table

        table = self.wrapper.metadata.tables.get(table_name)
        if table is None:
            raise DBTableNotFound(model_name=table_name)
        return table

    def get_alchemy_field(self, field_id, params):
        """
        Получение поля
        :param field_id: идентификатор поля
        :param params: дополнительные параметры для создания запроса
        """
        app_label, model_name, field_name = field_id.split('.')

        column = self.get_subquery(params).columns.get(field_name)
        if column is None:
            column = self.get_subquery(params).columns.get(field_name + '_id')
        if column is None:
            raise DBColumnNotFound(model_name, field_name)

        return column


class QueryEntity(BaseAlchemyEntity):
    """
    Для обозначения запросов созданных в КО.
    """

    def __init__(self, id, alias = None, entity_cache=None,
                 alchemy_query_builder=None,
                 outer_query_json=None):
        super(QueryEntity, self).__init__(id, alias, entity_cache)

        # class AlchemyQueryBuilder
        self.builder = alchemy_query_builder
        self.outer_query_json = outer_query_json

    def _build_sub_alchemy_query(self):
        """
        Строим подзапрос
        """
        query_id, query_name = self.id.split('.')

        query_proxy = QueryProxy.load_query(int(query_id))

        entity = self.builder(
            name=query_name,
            json_query=query_proxy.json_query,
            outer_query_json=self.outer_query_json,
            join_removal=getattr(settings, 'REPORT_GENERATOR_JOIN_REMOVAL', False),
            join_removal_checker='check_subquery_join_removal',
            alias=self.alias,
            entity_cache=self.entity_cache
        ).build()

        if entity is None:
            raise EntityNotFound(query_proxy.name)

        return entity # instance AlchemyQuery

    def _get_alchemy_table(self, params):
        entity = self._build_sub_alchemy_query()
        query = entity.create_query(params=params)

        # if self.alias:
        #     query = query.label(self.alias)

        return query

    def get_alchemy_field(self, field_id, params):
        """
        Получение поля
        :param field_id: идентификатор поля
        :param params: дополнительные параметры для создания запроса
        """

        field_list = field_id.split('.')
        query_id, query_name = field_list[:2]
        field_name = field_list[-1]
        try:
            columns = self.get_subquery(params).columns
            column = columns.get(field_name)
            if column is None:
                column = columns[field_name + '_id']
        except KeyError:
            raise DBColumnNotFound(query_name, field_name)

        return column


class Field(object):
    """
    Для обозначения поля
    """

    # Все поля
    ALL_FIELDS = '*'

    def __init__(self, entity, field_id, alias=None):
        self.entity = entity # instance Table, AlchemyQuery

        self.field_id = field_id

        self.alias = alias

    def get_alchemy_field(self, params):
        """
        Возвращает поле в формате SqlAlchemy.
        Пробрасывает вызов той сущности, с которой само работает.
        """
        field = self.entity.get_alchemy_field(field_id=self.field_id,
            params=params)
        return field

    def get_name(self):
        """
        Получение имени поля
        """
        return self.alias or self.field_id.split('.')[-1]


class Aggregate(object):
    """
    Набор классов для агрегирования
    """
    class BaseAggregate(object):
        def __init__(self, field):
            assert isinstance(field, Field), '"field" must be "Field" type'
            self.field = field

        def get_alchemy_func(self, column):
            """функция агрегирования из SQLAlchemy"""
            raise NotImplementedError()

    class Max(BaseAggregate):
        def get_alchemy_func(self, column):
            return func_generator.max(column)

    class Min(BaseAggregate):
        def get_alchemy_func(self, column):
            return func_generator.min(column)

    class Count(BaseAggregate):
        def get_alchemy_func(self, column):
            return func_generator.count(column)

    class Sum(BaseAggregate):
        def get_alchemy_func(self, column):
            return func_generator.sum(column)

    class Avg(BaseAggregate):
        def get_alchemy_func(self, column):
            return func_generator.avg(column)


class Relation(object):
    """
    Связь между сущностями
    """

    def __init__(self, field_first, field_second,
                 outer_first=False, outer_second=False,
                 alias_first=None, alias_second=None):
        """
        :param field_first: Первое поле
        :param outer_first: Тип связи, внешняя, или внутренняя. True - внешняя

        :param field_second: Второе поле
        :param outer_second: Тип связи, внешняя, или внутренняя. True - внешняя
        """
        assert isinstance(field_first, Field), '"field_first" must be "Field" type'
        assert isinstance(field_second, Field), '"field_first" must be "Field" type'

        self.field_first = field_first
        self.outer_first = outer_first

        self.field_second = field_second
        self.outer_second = outer_second

        self.alias_first = alias_first
        self.alias_second = alias_second


class SortOrder(object):
    """
    Для сортировки
    """

    ASC = 1
    DESC = 2

    VALUES = set([
        (ASC, u'По возрастанию'),
        (DESC, u'По убыванию')
    ])

    def __init__(self, field, order=None):

        assert isinstance(field, Field)
        assert order in (SortOrder.ASC, SortOrder.DESC)

        self.field = field
        self.order = order

    @classmethod
    def get_order_code(cls, order_text):

        for value in SortOrder.VALUES:
            sort_code, sort_text = value
            if sort_text == order_text:
                return sort_code


class Where(object):
    """
    Для условий
    """

    AND = 'AND'
    OR = 'OR'
    NOT = 'not'

    EQ = 'eq'
    NE = 'ne'
    LT = 'lt'
    LE = 'le'
    GT = 'gt'
    GE = 'ge'
    ISNULL = 'isnull'
    ISNOTNULL = 'isnotnull'
    ISDISTINCTFROM = 'isdistinctfrom'
    ISNOTDISTINCTFROM = 'isnotdistinctfrom'
    TRUE = 'Btrue'
    FALSE = 'Bfalse'
    IN = 'in'


    # TODO: Пока не используется оператор between
    BETWEEN = 'between'

    conditions = {
        EQ: u'= (Вхождение)',
        NE: u'!= (Не вхождение)',
        LT: '<',
        LE: '<=',
        GT: '>',
        GE: '>=',
        ISNULL: u'Является NULL',
        ISNOTNULL: u'Не является NULL',
        ISDISTINCTFROM: u'IS DISTINCT FROM',
        ISNOTDISTINCTFROM: u'IS NOT DISTINCT FROM',
        TRUE: u'ИСТИНА',
        FALSE: u'ЛОЖЬ',
        IN: u'IN',  # используется пользовательский выбор
    }

    connectors = {
        AND: 'AND',
        OR: 'OR'
    }

    # Типы параметров.
    # NORMAL_PARAM значение для подстановки в условие
    # FIELD_PARAM параметр поле модели.
    VALUE_PARAM = 1
    FIELD_PARAM = 2
    CONSTANT = 3

    param_type = {
        VALUE_PARAM: u'Параметр для подстановки',
        FIELD_PARAM: u'Параметр поле',
        CONSTANT: u'Константа'
    }

    def __init__(self, left=None, op=None, right=None):
        """
        :param left: Левый операнд
        :param op: Оператор (=, !=, <, >, <=, >=, ...)
        :param right: Правый операнд
        """
        self.left = left
        self.operator = op
        self.right = right

    def __and__(self, other):
        assert isinstance(other, Where), 'Value must be type is "Where"'
        return Where(self, Where.AND, other)

    def __or__(self, other):
        assert isinstance(other, Where), 'Value must be type is "Where"'
        return Where(self, Where.OR, other)

    def __invert__(self):
        return Where(self, Where.NOT)

    def is_empty(self):
        """ Возвращает истину, если условие пустое """
        return self.left is None and self.right is None

    def get_parameters(self, ent_ins):
        """ Возвращает список с именами параметров участвующих в условии """
        if self.is_empty():
            return []

        all_params = []

        def process_part(part):
            if isinstance(part, Param):
                part.bind_to_entity(ent_ins)
                all_params.append(part)
            elif isinstance(part, Where):
                all_params.extend( part.get_parameters(ent_ins) )

        process_part(self.left)
        process_part(self.right)

        return all_params

    @classmethod
    def get_param_types(cls):

        return [(Where.VALUE_PARAM, Where.param_type[Where.VALUE_PARAM]),
            (Where.FIELD_PARAM, Where.param_type[Where.FIELD_PARAM])]


class Grouping(object):
    """
    Для группировки
    """

    MIN = u'Минимум'
    MAX = u'Максимум'
    COUNT = u'Количество'
    SUM = u'Сумма'
    AVG = u'Среднее'

    def __init__(self, group_fields, aggregate_fields):
        self.group_fields = group_fields
        self.aggregate_fields = aggregate_fields

    @staticmethod
    def get_aggr_functions():
        return {
            Grouping.MIN: Aggregate.Min,
            Grouping.MAX: Aggregate.Max,
            Grouping.COUNT: Aggregate.Count,
            Grouping.SUM: Aggregate.Sum,
            Grouping.AVG: Aggregate.Avg
        }


class Param(object):
    """
    Базовый класс для фиксированных значений и параметров в условии Where
    """
    STRING = 1
    NUMBER = 2
    DICTIONARY = 3
    DATE = 4
    BOOLEAN = 5
#    COMBO = 6

    VALUES = {
        STRING: u'Текст',
        NUMBER: u'Число',
        DATE: u'Дата',
        BOOLEAN: u'Флаг',
        DICTIONARY: u'Выбор из справочника',
#        COMBO: u'Выбор из списка значений',
        }

    def __init__(self, name, verbose_name, type):

        if type:
            assert type in Param.VALUES.keys(), 'type must be value in Param.VALUES'

        # Тип параметра
        self.type = type

        # Название параметра: Имя класса + '.' + Имя параметра
        self.name = name

        # Человеческое название параметра
        self.verbose_name = verbose_name

    def bind_to_entity(self, ent):
        """
        Чтобы имена параметров не пересекались, во время формирования запроса
        к имени параметра добавляется имя класса
        """

        if self.name.find('.') == -1:
            self.name = '%s.%s' % (ent.__class__.__name__, self.name)

    def get_name(self):
        """
        Возвращает название параметра
        :return: str
        """
        return self.name

    def get_verbose_name(self):
        """
        Возвращает название, понятное человеку.
        :return: str
        """
        return self.verbose_name

    def get_type(self):
        """
        Возвращает тип параметра
        :return: str
        """
        return self.type

    @staticmethod
    def get_type_choices():
        return ( (k, v) for k, v in Param.VALUES.items() )


def _in_func(x, y):
    try:
        return x.in_(json.loads(y.replace("\'", "\"").replace('&quot;', '\"')))
    except:
        return x.op('IN')('"%s"' % y)


class AlchemyQuery(object):
    """
    Класс запрос для Alchemy
    """

    # Карта для перевода операций конструктора запросов в алхимию
    OPERATION_MAP = {
        Where.EQ: lambda x, y: x == y,
        Where.NE: lambda x, y: x != y,
        Where.LT: lambda x, y: x < y,
        Where.LE: lambda x, y: x <= y,
        Where.GT: lambda x, y: x > y,
        Where.GE: lambda x, y: x >= y,
        Where.AND: lambda x, y: x & y,
        Where.OR: lambda x, y: x | y,
        Where.NOT: lambda x, y: ~x,
        Where.BETWEEN: lambda x, y: x.between(y[0], y[1]),
        Where.ISNULL: lambda x, y: x == None,
        Where.ISNOTNULL: lambda x, y: x != None,
        Where.ISDISTINCTFROM: lambda x, y: x.op("IS DISTINCT FROM")(y),
        Where.ISNOTDISTINCTFROM: lambda x, y: x.op("IS NOT DISTINCT FROM")(y),
        Where.TRUE: lambda x, y: true(),
        Where.FALSE: lambda x, y: false(),
        Where.IN: _in_func
    }

    def __init__(self, name):

        # Имя запроса
        self.name = name
        # instance QueryEntity or Table
        self.entities = []

        # Типизированный список связей, над вышеупомянутами объектами
        self.relations = TypedList(type=Relation)

        # Список полей, по которым нужно проводить группировку
        self.group_by = None

        # Объект условий
        self.where = None

        # Список объектов SortOrder
        self.order_by = TypedList(type=SortOrder)

        # Список объектов Field
        self.select = TypedList(type=Field)

        # Выводить повторяющиеся записи?
        self.distinct = None

        # Количество показываемых записей
        self.limit = 0

        # Смещение от начала выборки
        self.offset = 0

        self.wrapper = WrapperBuilder.build_wrapper()
        self.metadata = self.wrapper.metadata
        self.session = self.wrapper.session

    def does_wrapper_exist(self):
        """
        Существует ли Wrapper
        :return:
        """
        return isinstance(self.wrapper, SQLAlchemyWrapper)

    def create_query(self, params=None, first_head=False):

        if not len(self.select):
            raise EntityException(u'Нет данных для SELECT')

        select_columns = self._create_columns(params)
        join_sequence = self._create_join(params)
        whereclause = self._create_where_expression(self.where, params, first_head)

        query = select(columns=select_columns, whereclause=whereclause,
            from_obj=join_sequence, distinct = (True if self.distinct else False))

        query = self._create_grouping(query, params)
        query = self._create_sorting(query, params)
        query = self._create_limit_offset(query, params, first_head)

        return query

    def _create_columns(self, params):
        select_columns = []

        def populate(field):
            assert isinstance(field, Field)

            column = field.get_alchemy_field(params)
            if field.alias:
                column = column.label(field.alias)

            column = self._prepare_aggregate_for_field(field, column)

            select_columns.append(column)

        map(populate, self.select)
        map(populate, [x.field for x in self.group_by.aggregate_fields])

        return select_columns

    def _prepare_aggregate_for_field(self, field, column):

        if self.group_by and self.group_by.aggregate_fields:
            aggregate_fields = self.group_by.aggregate_fields
            for af in aggregate_fields:
                if af.field.field_id == field.field_id:
                    column = af.get_alchemy_func(column)
                    column = column.label(field.alias)
                    break
        return column

    def _create_join(self, params):

        join_sequence = None
        for rel in self.relations:
            assert isinstance(rel, Relation)

            left_column = rel.field_first.get_alchemy_field(params)
            right_column = rel.field_second.get_alchemy_field(params)

            if join_sequence is None:

                onclause = (left_column == right_column) # _BinaryExpression

                if rel.outer_first or rel.outer_second:
                    join_sequence = outerjoin(left_column.table, right_column.table, onclause)
                else:
                    join_sequence = join(left_column.table, right_column.table, onclause)

            else:
                onclause = (left_column == right_column) #_BinaryExpression

                if rel.outer_first or rel.outer_second:
                    join_sequence = join_sequence.outerjoin(right_column.table, onclause)
                else:
                    join_sequence = join_sequence.join(right_column.table, onclause)

        join_sequence = None if join_sequence is None else [join_sequence]
        return join_sequence

    def _get_func_by_operator(self, operator):
        """ Возвращает функцию соответствующую логической операции """
        func = self.OPERATION_MAP.get(operator)
        if not func:
            raise NotImplementedError(u'Логическая операция "%s" не реализована в WHERE' % operator)
        return func

    def _is_param_empty(self, value):
        """
        Из-за особой хитрости передаваемых параметров это делается не очевидно.
        Возвращает истину, если значение параметра пустое.
        """
        if value is None:
            return True
        if not value:
            return True
        if isinstance(value, (tuple, list)) and not len(value):
            return True
        return False

    def _create_where_expression(self, where, params, first_head):

        # Пустые условия пропускаем
        if where is None or where.is_empty():
            return

        # Если условие составное, то обрабатываем его рекурсивно
        left, right = where.left, where.right
        if isinstance(where.left, Where):
            left = self._create_where_expression(left, params, first_head)
        if isinstance(where.right, Where):
            right = self._create_where_expression(right, params, first_head)

        # Если отсутствует одна из частей условия, то возвращаем существующую
        if left is None and right is not None:
            return right
        elif left is not None and right is None:
            return left
        elif left is None and right is None:
            return

        func = self._get_func_by_operator(where.operator)

        def give_me_some_class(iterable, class_1):
            has_one = False
            for x in iterable:
                if not isinstance(x, ColumnElement):
                    has_one = True
                    if isinstance(x, class_1):
                        return x
            # if has_one:
            #     raise TypeError('Where argument must be string, Param of Field instance')

        part_param = give_me_some_class([left, right], Param)
        part_field = give_me_some_class([left, right], Field)

        # Текущий узел WHERE не содержит ни поля ни параметра,
        # значит он объединяет 2 логических условия. Разбор параметров не требется.
        if part_param is None and part_field is None:
            return func(left, right)

        left = part_field.get_alchemy_field(params)

        if isinstance(part_param, Param):
            right = bindparam(part_param.name, required=True)
        # elif isinstance(part_param, basestring):
        #
        # Константа в условии
        elif part_param is None:
            if isinstance(right, Field):
                right = right.get_alchemy_field(params)
            # right = 2
        else:
            right = part_param.get_alchemy_field(params)

        if part_param and isinstance(part_param, Param) and isinstance(params, dict):
            value = params.get(part_param.name)

            # Если параметры заданы, но нужного не оказалось, то убираем условие нафиг!
            if self._is_param_empty(value):
                return

            # Хитрая замена IN (ARRAY[]) на ANY(ARRAY[])
            if isinstance(value, (list, tuple)):
                right = func_generator.any(right)

        exp = func(left, right)
        return exp

    def _create_grouping(self, query, params):
        """
        Добавляет в запрос алхимии конструкцию GROUP BY
        """
        if self.group_by and self.group_by.group_fields:
            for field in self.group_by.group_fields:
                col = field.get_alchemy_field(params)
                query = query.group_by(col)
        return query

    def _create_sorting(self, query, params):
        """
        Добавляет в запрос алхимии конструкцию ORDER BY
        """
        sorted_fields = []
        for sort_order in self.order_by:
            field, order = sort_order.field, sort_order.order
            column = field.get_alchemy_field(params)
            column = self._prepare_aggregate_for_field(field, column)

            # Добавляем сортировочные функции
            if order == SortOrder.ASC:
                column = column.asc()
            elif order == SortOrder.DESC:
                column = column.desc()

            sorted_fields.append(column)

        return query.order_by(*sorted_fields)

    def _get_param(self, params, key, default=None, single=True):
        value = params.get(key)
        if not self._is_param_empty(value):
            if single and isinstance(value, (list, tuple)):
                return value[0]
            return value
        return default

    def _create_limit_offset(self, query, params, first_head):
        """
        Добавляет в запрос алхимии срез по LIMIT и OFFSET. Из-за того, что эти операторы не
        поддердивают работу с параметрами, приходится подставлять их напрямую в запрос, если
        текущий проход является генеративным.
        """
        limit_value = 0
        offset_value = 0

        if params and isinstance(params, dict):
            class_name = self.__class__.__name__ + '.'
            if first_head:
                limit_value = self._get_param(params, 'limit', 0)
                offset_value = self._get_param(params, 'offset', 0)
            else:
                limit_value = self._get_param(params, class_name + 'limit', 0)
                offset_value = self._get_param(params, class_name + 'offset', 0)

        # Пробуем получить предустановленные значения
        if not limit_value and isinstance(self.limit, int) and self.limit > 0:
            limit_value = self.limit

        if not offset_value and isinstance(self.offset, int) and self.offset > 0:
            offset_value = self.offset

        # Установка значений
        if limit_value > 0:
            query = query.limit(limit_value)

        if offset_value > 0:
            query = query.offset(offset_value)

        return query

    def get_raw_sql(self):
        """ Возвращает текст SQL запроса"""
        sql = str(self.create_query())
        if sqlparse:
            sql = sqlparse.format(sql, reindent=True, keyword_case='upper')
        return sql

    def get_select_fields(self):
        """ Возвращает список всех полей entity.Field из SELECT """
        fields = []
        for field in self.select:
            assert isinstance(field, Field), '"field" must be "Field" type'
            fields.append(field)

        return fields

    def get_data(self, params=None):
        """
        Возвращает данные, полученные в результате выполнения запроса

        :param params: Параметры для запроса
        @raise ReportGeneratorError, EntityException children
        """
        params = params or {}

        BaseAlchemyEntity.clear_instances()

        query = self.create_query(params=params, first_head=True)

        if self.does_wrapper_exist():
            self.wrapper.engine.echo = True
        else:
            raise ReportGeneratorError(u'Не подключен wrapper.')
        cursor = query.execute(params)
        data = cursor.fetchall()

        return data
