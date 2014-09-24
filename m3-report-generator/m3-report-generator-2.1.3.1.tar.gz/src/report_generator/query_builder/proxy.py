#coding: utf-8

import json

from m3_ext.ui.icons import Icons

from report_generator.exceptions import ReportGeneratorError
from report_generator.query_builder.models import Query


def escape_chars(str_):
    return str_.replace("'", "\"").replace('\"', '&quot;')

# Пришлось дублировать или кросс-импорт
class EntityTypes(object):

    MODEL = 1
    QUERY = 2

    TYPES = {
        MODEL: u'Модели проекта',
        QUERY: u'Запросы'
    }

class QueryProxy(object):
    """
    Прокси класс для работы с запросом
    """

    def __init__(self, query_name, json_query, query_id = None):

        # Идентификатор запроса
        self.id = query_id

        # Имя запроса
        self.name = query_name

        # json представление запроса
        self.json_query = json_query

    def save_query(self):
        """
        Сохранение
        """

        if self.id:
            try:
                query = Query.objects.get(id=self.id)
            except Query.DoesNotExist:
                raise ReportGeneratorError(u'Объекта с таким id не существует')

            query.name = self.name
            query.json_query = json.dumps(self.json_query)
        else:
            query = Query(name=self.name, json_query=json.dumps(self.json_query))

        query.save()

        return query.id

    @classmethod
    def delete_query(cls, ids):
        """
        Удаление запроса
        """

        Query.objects.filter(id__in=ids).delete()

    @classmethod
    def load_query(cls, query_id):
        """
        Загрузка заместителя запроса по ID
        """

        try:
            query = Query.objects.get(id=query_id)
        except Query.DoesNotExist:
            raise ReportGeneratorError(u'Не найден запрос')

        json_query = json.loads(query.json_query)
        return QueryProxy(query_id=query.id, query_name=query.name, json_query=json_query)

    def set_json_query(self, query_id):

        try:
            query = Query.objects.get(query_id)
        except Query.DoesNotExist:
            self.json_query = None
            return

        self.json_query = query.json_query

    def get_relations(self):
        """
        Подготавливает данные об отношениях, для загрузки в окно редактирования запросов
        """

        relations = self.json_query.get('relations')

        return [(relation.get('id'),
                 relation.get('outerFirst'),
                 relation.get('value'),
                 relation.get('outerSecond'),
                 relation.get('leftEntityType'),
                 relation.get('rightEntityType')) for relation in relations]

    def get_distinct(self):
        return self.json_query.get('distinct')

    def get_selected_fields(self, id_suffix=None):
        """
        Подготавливает данные о select полях, для загрузки в окно редактирования запросов
        """
        # id_suffix = None

        fields = self.json_query.get('selected_fields')
        # debug_print(fields)

        def populate(field):
            id_list = field.get('id').split('.')
            # debug_print(id_list)
            entity_id = '.'.join(id_list[:-1]) + (
                ('__' + id_suffix) if id_suffix else ''
            )
            # debug_print(entity_id)
            id_ = '.'.join([entity_id, id_list[-1]])

            return (
                id_,
                field.get('fieldName'),
                field.get('alias', ''),
                field.get('sorting', ''),
                field.get('entityType'),
                entity_id,
                field.get('fieldVerboseName')
            )

        return map(populate, fields)

    def get_limit(self):
        return self.json_query.get('limit')

    def get_entities(self):
        """
        Подготавливает данные о внутренних сущностях, для загрузки в окно редактирования запросов
        """

        entities =  self.json_query.get('entities')

        return [(entity.get('id'), entity.get('title'), entity.get('entityType'), entity.get('entityId'))
                for entity in entities]

    def get_group(self):
        return self.json_query.get('group')

    def get_group_fields(self):
        """
        Подготавливает данные о групповых полях, для загрузки в окно редактирования запросов
        """

        group_fields = self.get_group().get('group_fields')

        return [(group_field.get('id'),
                 group_field.get('fieldName'),
                 group_field.get('entityId'),
                 group_field.get('entityType')) for group_field in group_fields]

    def get_group_aggr_fields(self):
        """
        Подготавливает данные об аггрегируемых полях для загрузки в окно редактирования запросов
        """

        aggr_fields = self.get_group().get('group_aggr_fields')

        return [(aggr_field.get('id'),
                 aggr_field.get('fieldName'),
                 aggr_field.get('alias'),
                 aggr_field.get('function'),
                 aggr_field.get('entityId'),
                 aggr_field.get('entityType'),
                 aggr_field.get('fieldVerboseName')) for aggr_field in aggr_fields]

    def get_join_removal(self):
        return self.json_query.get('join_removal', False)

    def get_where(self):
        """
        Подготавливает данные об условиях, для загрузки в окно редактирования запросов
        """

        where_conditions = self.json_query.get('cond_fields')

        # return [(where.get('id'),
        #          where.get('verboseName'),
        #          where.get('condition'),
        #          where.get('parameter'),
        #          where.get('expression'),
        #          where.get('connector'),
        #          where.get('param_type'),
        #          where.get('id_field'),
        #          where.get('entity_name'),
        #          where.get('first_field_entity_type'),
        #          where.get('second_field_entity_type')) for where in where_conditions]
        result = []
        for where_ in where_conditions:
            print where_
            where = {}
            where.update(where_)
            where['id_'] = escape_chars(where['id_'])
            where['expression'] = escape_chars(where['expression'])
            where['parameter'] = escape_chars(where['parameter'])
            where['_is_loaded'] = True
            if where.get('_parent') is None:
                where['_parent'] = None
            # del where['id']
            result.append(where)
        return result

    def get_query_params(self):
        """
        Возвращает список имен параметров запроса
        """

        where_conditions = self.json_query.get('cond_fields')

        params = []

        def populate(where):
            param_type = where.get('param_type')

            #cross import
            # Можно исправить, если передать QueryProxy в конструктор QueryEntity
            from report_generator.core.query_components import Where
            if param_type == Where.VALUE_PARAM:
                params.append(
                    dict(name = where.get('parameter'),
                         query_id = self.id,
                         field = where.get('verboseName'),
                         leaf = True,
                         iconCls = Icons.TABLE_GEAR)
                )

        # Условия данного запроса
        map(populate, where_conditions)

        # Пробегаемся по всем сущностям и рекурсивно вызываем данную функцию
        entities = self.json_query.get('entities')
        for entity in entities:

            entity_type = entity.get('entityType')

            # Если сущность запрос, то берём и её параметры
            if entity_type == EntityTypes.QUERY:

                entity_id = entity.get('entityId')
                id, name = entity_id.split('.')

                query_proxy = QueryProxy.load_query(query_id=int(id))

                params.extend(query_proxy.get_query_params())

        return params

    @classmethod
    def get_query_data(cls, id):
        """
        Возвращаем парметры и select поля запроса
        """

        query_proxy = cls.load_query(id)

        return cls.get_params_data(query_proxy), cls.get_select_data(query_proxy)

    @classmethod
    def get_queries(cls, ids):
        """
        Возвращаем query_proxy для каждого запроса представленного ID-ром
        """

        queries = Query.objects.filter(id__in=ids)

        return [QueryProxy(query_name=query.name, json_query=json.loads(query.json_query),
                        query_id=query.id) for query in queries]

    @classmethod
    def get_select_data(cls, query_proxy):
        """
        Возвращает данные о selecte для запроса
        """

        root_select_node = dict(query_id=query_proxy.id,
                                name=query_proxy.name,
                                leaf=False,
                                expanded=True,
                                iconCls=Icons.FOLDER_TABLE,
                                draggable=False)

        selected_fields = query_proxy.json_query.get('selected_fields')
        aggr_fields = query_proxy.json_query.get('group').get(
            'group_aggr_fields'
        )

        def populate(selected_field):

            d = dict(name=selected_field.get('alias') or selected_field.get('fieldName'),
                     leaf=True,
                     iconCls=Icons.TABLE_LINK,
                     query_id=query_proxy.id)

            root_select_node.setdefault('children', []).append(d)

        map(populate, selected_fields)
        map(populate, aggr_fields)

        return root_select_node

    @classmethod
    def get_params_data(cls, query_proxy):
        """
        Возвращает параметры запроса
        """

        root_params_node = dict(id=query_proxy.id,
                                name=query_proxy.name,
                                leaf=True,
                                expanded=True,
                                iconCls=Icons.FOLDER_TABLE,
                                draggable=False)

        params = query_proxy.get_query_params()

        def populate(param):
            root_params_node.setdefault('children', []).append(param)

        map(populate, params)

        return root_params_node
