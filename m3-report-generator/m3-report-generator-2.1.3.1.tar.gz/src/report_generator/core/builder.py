#coding: utf-8
from django.db.models import get_model, ForeignKey

from report_generator.core.query_components import *

class EntityTypes(object):
    """
    Типы сущностей
    Модели / запросы
    """
    MODEL = 1
    QUERY = 2

    TYPES = {
        MODEL: u'Модели проекта',
        QUERY: u'Запросы'
    }

    # Сопоставление типа сущности и класса. Используется в фабрике сущностей.
    CLASS_MAP = {
        MODEL: TableEntity,
        QUERY: QueryEntity
    }

    @classmethod
    def get_entity_type_title(cls, type):
        """
        Возвращает заголовок для сущностей
        """

        return EntityTypes.TYPES.get(type)


class EntityFactory(object):
    """
    Фабрика потомков constructor.core.query_component.BaseAlchemyEntity
    """

    @classmethod
    def create_entity(cls, entity_id, entity_type, json_query, entity_cache):
        """
        По JSON представлению сущности строим потомка BaseAlchemyEntity
        :param entity_id уникальный идентификатор, связан с названием
        модели или запроса
        :param entity_type тип сущности из EntityTypes
        :param json_query составные части запроса в формате json
        :param entity_cache кеш сущностей
        """

        assert entity_type in EntityTypes.TYPES, u'Не поддерживаемый тип сущности'

        entity = entity_id.split('__')
        if len(entity) == 1:
            alias = None
        else:
            # сущность имеет вид acc_roll.AccRoll__1377664746837
            alias = entity_id.split('.')[-1]
        entity_id_ = entity[0]

        entity_class = EntityTypes.CLASS_MAP.get(entity_type)
        return entity_class(
            entity_id_,
            alias=alias,
            entity_cache=entity_cache,
            alchemy_query_builder=AlchemyQueryBuilder,
            outer_query_json=json_query)


class AlchemyQueryBuilder(object):
    """
    Превращает некий обьект в AlchemyQuery
    """

    def __init__(self, name, **kwargs):
        self.wrapper = WrapperBuilder.build_wrapper()
        self.json_query = kwargs.get('json_query')
        self.apply_join_removal = kwargs.get('join_removal', False)
        self.alchemy_query = AlchemyQuery(name)
        self.join_removal_checker = kwargs.get(
            'join_removal_checker',
            'can_remove_join'
        )
        self.outer_query_json = kwargs.get('outer_query_json')
        self.alias = kwargs.get('alias')
        self.join_removal_entities = {}
        self.entity_cache = kwargs['entity_cache']

    def build(self):
        """
        Построение запроса
        """
        self._prepare_internal_entities()
        self._prepare_relations()
        self._prepare_group_by()
        self._prepare_select_and_order_fields()
        self._prepare_where()
        self._prepare_limit()
        self._prepare_distinct()

        return self.alchemy_query

    def can_remove_entity(self, entity):
        """
        Проверка того, что можно удалить сущность запроса,
        не изменив сути результата
        :param entity: сущность
        """
        if not self.apply_join_removal:
            return False, True
        if not self.outer_query_json:
            return False, True
        if not self.outer_query_json.get('join_removal', False):
            return False, True

        entity_id = entity['entityId']
        # if self.json_query['entities'][0]['entityId'] == entity_id:
        #     return False, True
        no_relation_right = True
        if not self.outer_query_json:
            for selected in self.json_query['selected_fields']:
                if selected['entityId'] == entity_id:
                    return False, True
        else:

            for relation in self.json_query['relations']:
                second_entity_id_ = self.parse_relation_id(relation['id'])
                # if second_entity_id == entity['id']:
                rel_dict = self._parse_relation(relation)
                second_alias = rel_dict['second_alias']
                first_alias = rel_dict['first_alias']
                first_field_n = rel_dict['first_field_n']
                second_field_n = rel_dict['second_field_n']
                first_entity_id = rel_dict['first_entity_id']
                second_entity_id = rel_dict['second_entity_id']
                if second_entity_id_ == entity_id:
                    no_relation_right = False
                    if not self.check_subquery_join_removal(
                        relation, self.outer_query_json,
                        second_alias, first_field_n, second_field_n,
                        first_entity_id, second_entity_id
                    ):
                        return False, False
        #TODO: группируемые поля
        return True, no_relation_right

    def parse_relation_id(self, relation_id):
        """
        Парсим правую часть связи
        :param relation_id идентификатор связи
        """
        left, right = relation_id.split('|')
        entity_id, _ = right.split('-')
        return entity_id

    def parse_relation_id_left(self, relation_id):
        """
        Парсим левую часть связи
        :param relation_id идентификатор связи
        """
        left, right = relation_id.split('|')
        entity_id, _ = left.split('-')
        return entity_id


    def get_field(self, model_id, field_name):
        """
        Получение поля
        :param model_id идентификатор модели
        :param field_name идентификатор поля
        """
        model = get_model(*model_id.split('.', 1))
        return model._meta.get_field(field_name[:-3])

    def check_subquery_join_removal(
        self,
        relation,
        outer_query_json,
        entity_alias,
        first_field_name,
        second_field_name,
        first_entity_id,
        second_entity_id
    ):
        """
        Проверяем, что можно удалить сущности из подзапроса,
        не изменив результат запроса
        """
        if not self.apply_join_removal:
            return False

        if not self.outer_query_json:
            return False
        if not self.outer_query_json.get('join_removal', False):
            return False
        # Если есть условия, удаление join-ов невозможно
        relation_id = self.parse_relation_id(relation['id'])

        for rel in self.json_query.get('relations'):
            if relation_id == self.parse_relation_id_left(rel['id']):
                return False
        for condition in self.json_query['cond_fields']:
            if relation_id in condition['id_']:
                return False
        for condition in self.outer_query_json['cond_fields']:
            if self.alias and self.alias == condition['id_field'].split('.')[1]:
                return False
        group = self.json_query.get('group')

        # Группируемые поля
        for grouping_field in group.get('group_fields'):
            if relation_id in grouping_field['entityId']:
                return False
        for group_aggr_field in group.get('group_aggr_fields'):
            if relation_id == group_aggr_field['entityId']:
                return False

        group = self.outer_query_json.get('group')
        for selected in self.json_query['selected_fields']:
            for grouping_field in group.get('group_fields'):
                if selected['entityId'] == relation_id:
                    if grouping_field['fieldName'] == (selected['alias'] or selected['fieldName']):
                        return False
        # Агрегируемые поля при группировке
        for selected in self.json_query['selected_fields']:
            for group_aggr_field in group.get('group_aggr_fields'):
                if selected['entityId'] == relation_id:
                    if group_aggr_field['fieldName'] == (selected['alias'] or selected['fieldName']):
                        return False

        # Если во внешнем запросе выбираются поля из внутреннего,
        # сущности с такими полями удалить нельзя
        for selected in self.json_query['selected_fields']:
            for outer_selected in outer_query_json['selected_fields']:
                if self.alias and self.alias == outer_selected['entityId'].split('.')[1]:
                    if selected['fieldName'] == outer_selected['fieldName']:
                        if self.parse_relation_id(relation['id']) == selected['entityId']:
                            return False
                        if (
                            not relation['outerFirst']
                        ) or (
                            second_field_name != 'id'
                        ) or (
                            not first_field_name.endswith('_id')
                        ):
                            return False
                        first_field = self.get_field(first_entity_id, first_field_name)
                        if not isinstance(first_field, ForeignKey):
                            return False
        return True

    def can_remove_join(self,
                        relation,
                        rel,
                        entity_alias,
                        first_field_name,
                        second_field_name,
                        first_entity_id,
                        second_entity_id):
        return False
        if (
            not self.apply_join_removal
        ) or (
            not relation['outerFirst']
        ) or (
            second_field_name != 'id'
        ) or (
            not first_field_name.endswith('_id')
        ):
            return False
        first_field = self.get_field(first_entity_id, first_field_name)
        if not isinstance(first_field, ForeignKey):
            return False

        for selected in self.json_query['selected_fields']:
            sel_id = selected['entityId']
            if entity_alias in sel_id:
                return False
        return True

    def _prepare_internal_entities(self):
        """
        Подготовка подсущностей
        """
        entities = []
        for entity in self.json_query.get('entities'):
            can_remove, no_relation_right = self.can_remove_entity(entity)
            if not can_remove:
                entities.append(entity)
            elif not no_relation_right:
                self.join_removal_entities[entity['id']] = True
        self.alchemy_query.entities = entities

        # self.alchemy_query.entities = [self._prepare_entity_object(x) for x
        #     in self.json_query.get('entities')]
    def _prepare_entity_object(self, entity):
        """
        Создание сущности по объекту
        """
        entity_id = entity.get('entityId')
        entity_type = entity.get('entityType')

        return EntityFactory.create_entity(entity_id, entity_type,
                                           self.json_query,
                                           self.entity_cache)

    def _parse_relation(self, relation):
        first_part, second_part = relation.get('id').split('|')
        first_entity_id, first_field_id = first_part.split('-')
        first_entity_id, first_alias_suffix = first_entity_id.split('__')
        first_field_n = first_field_id.split('.')[-1]
        # first_field_id = u'.'.join([first_entity_id, first_field_n])
        first_alias = u''.join([
            first_entity_id.split('.')[-1], '__', first_alias_suffix
        ])
        second_entity_id, second_field_id = second_part.split('-')
        second_entity_id, second_alias_suffix = second_entity_id.split('__')
        second_field_n = second_field_id.split('.')[-1]
        # second_field_id = u'.'.join([second_entity_id, second_field_n])
        second_alias = u''.join([
            second_entity_id.split('.')[-1], '__', second_alias_suffix
        ])
        return locals()

    def _prepare_relations(self):
        """
        """

        relations = self.json_query.get('relations')

        def populate(relation):
            rel_dict = self._parse_relation(relation)
            second_alias = rel_dict['second_alias']
            first_alias = rel_dict['first_alias']
            first_field_n = rel_dict['first_field_n']
            second_field_n = rel_dict['second_field_n']
            first_entity_id = rel_dict['first_entity_id']
            second_entity_id = rel_dict['second_entity_id']
            first_field_id = rel_dict['first_field_id']
            second_field_id = rel_dict['second_field_id']

            first_outer = relation.get('outerFirst')
            second_outer = relation.get('outerSecond')

            if not getattr(self, self.join_removal_checker)(
                relation, self.outer_query_json,
                second_alias, first_field_n, second_field_n,
                first_entity_id, second_entity_id
            ):
                rel = Relation(
                    self._prepare_field(field_id=first_field_id, entity_type=relation.get('leftEntityType')),
                    self._prepare_field(field_id=second_field_id, entity_type=relation.get('rightEntityType')),
                    outer_first=first_outer,
                    outer_second=second_outer,
                    alias_first=first_alias,
                    alias_second=second_alias
                )
                self.alchemy_query.relations.append(rel)



        map(populate, relations)

    def _prepare_field(self, field_id, entity_type, alias=None):
        if entity_type == EntityTypes.MODEL:
            app, model, field = field_id.split('.')
            entity_id = '.'.join([app, model])
        else:
            q_id, q_name = field_id.split('.')[:2]  # app, model,
            entity_id = '.'.join([q_id, q_name])

        entity = EntityFactory.create_entity(
            entity_id, entity_type, self.json_query, self.entity_cache)

        return Field(entity=entity, field_id=field_id, alias=alias)

    def _prepare_group_by(self):

        self.alchemy_query.group_by = Grouping(group_fields=self._prepare_group_fields(),
            aggregate_fields=self._prepare_aggregation_fields())

    def _prepare_group_fields(self):

        group_fields = []

        def populate(group_field):
            field = self._prepare_field(group_field.get('id'), group_field.get('entityType'))
            group_fields.append(field)

        map(populate, self.json_query.get('group').get('group_fields'))

        return group_fields

    def _prepare_aggregation_fields(self):

        aggregation_fields = []

        def populate(aggr_field):

            field = self._prepare_field(aggr_field.get('id'), entity_type=aggr_field.get('entityType'),
                alias=aggr_field.get('alias'))
            aggr_func = aggr_field.get('function')

            if aggr_func:
                aggr_class = Grouping.get_aggr_functions()[aggr_func]
                aggregation_fields.append(aggr_class(field))

        map(populate, self.json_query.get('group').get('group_aggr_fields'))

        return aggregation_fields

    def _prepare_select_and_order_fields(self):

        def populate(select_field):
            if select_field['entityId'] in self.join_removal_entities:
                return
            field = self._prepare_field(select_field.get('id'), entity_type=select_field.get('entityType'),
                alias=select_field.get('alias'))
            self.alchemy_query.select.append(field)

            sort_order = SortOrder.get_order_code(select_field.get('sorting'))
            if sort_order:
                self.alchemy_query.order_by.append(SortOrder(field, order=sort_order))

        map(populate, self.json_query.get('selected_fields'))

    def _prepare_limit(self):

        self.alchemy_query.limit = self.json_query.get('limit')

    def _prepare_distinct(self):

        self.alchemy_query.distinct = self.json_query.get('distinct')

    def _prepare_where(self):

        conditions = self.json_query.get('cond_fields')

        def populate(condition):
            param_type = condition.get('param_type')
            if param_type == Where.VALUE_PARAM:
                right = Param(
                    name=condition.get('parameter'),
                    type=None,
                    verbose_name=None
                )
            elif param_type == Where.FIELD_PARAM:
                right = self._prepare_field(
                    condition.get('parameter'),
                    entity_type=condition.get('second_field_entity_type')
                )
            elif param_type == Where.CONSTANT:
                right = condition.get('parameter')
            else:
                raise ValueError(u'Неизвестный тип параметра')
            where = Where(
                left=self._prepare_field(
                    condition.get('id_field'),
                    condition.get('first_field_entity_type')
                ),
                op=condition.get('condition'),
                right=right)
            return where
            # if not self.alchemy_query.where:
            #     self.alchemy_query.where = where
            # else:
            #     if condition.get('connector') == Where.AND:
            #         self.alchemy_query.where &= where
            #     elif condition.get('connector') == Where.OR:
            #         self.alchemy_query.where |= where
        conditions_tree = {}
        for cond in conditions:
            conditions_tree.setdefault(
                unicode(cond.get('_parent')), []
            ).append(cond)

        def make_where(parent_id):
            where_ = None
            connector = Where.AND
            for condition in filter(
                lambda x: x.get('_parent', 0) == parent_id, conditions
            ):
                _where = populate(condition)

                if unicode(condition.get('_id')) in conditions_tree:
                    _where_, connector_ = make_where(condition.get('_id'))
                    if connector_ == Where.AND:
                        _where &= _where_
                    elif connector_ == Where.OR:
                        _where |= _where_

                if where_ is None:
                    where_ = _where
                    connector = condition['connector']
                elif condition.get('connector') == Where.AND:
                    where_ &= _where
                elif condition.get('connector') == Where.OR:
                    where_ |= _where

            return where_, connector

        self.alchemy_query.where, _ = make_where(0)
