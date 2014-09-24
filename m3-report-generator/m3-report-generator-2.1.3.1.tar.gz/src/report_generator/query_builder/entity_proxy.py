#coding: utf-8
from collections import defaultdict

import json

from django.db.models import (
    loading, CharField, IntegerField, ForeignKey,
    DecimalField, DateField, DateTimeField, TextField, BooleanField,
    NullBooleanField
)

from m3_ext.ui.icons import Icons

import settings

from report_generator.core.entity_proxy import EntityUIProxyInterface
from report_generator.core.builder import EntityTypes
from report_generator.query_builder.models import Query
from report_generator.query_builder.proxy import QueryProxy
from report_generator.constructor_settings import MODELS, EXCLUDE_MODELS

class QueryEntityUIProxy(EntityUIProxyInterface):
    """
    Посредник между запросами созданными в КО и UI

    Протокол хранения:
    1) Сущность-запрос
        а) Идентификатор - queryId.queryName - queryId - идентификатор записи в БД,
                                                         атрибут name записи в БД
        б) Название атрибут name записи в БД.
    2) Поле сущности-запроса
    """

    @classmethod
    def get_entities(cls):
        """
        Подготавливает данные о имеющихся запросах для загрузки в дерево сущностей.
        """

        # Получаем все запросы, созданные при помощи КО.
        queries = Query.objects.values('id', 'name')

        # Корневой узел
        root_node = dict(id = EntityTypes.QUERY,
                         iconCls = Icons.FOLDER_TABLE,
                         title = EntityTypes.get_entity_type_title(EntityTypes.QUERY),
                         leaf = False,
                         expanded = True,
                         title_verbose='')

        def populate(query):
            query_name = query.get('name')
            query_id = query.get('id')
            node = dict(id='.'.join([str(query_id), query_name]),
                        leaf=True,
                        iconCls=Icons.PLUGIN,
                        title=query_name,
                        title_verbose='')

            root_node.setdefault('children', []).append(node)

        # Заполняем запросы
        map(populate, queries)

        # Если запросов , не имеется, то корневой узел добавлять не будем
        if not root_node.get('children'):
            root_node = None

        return root_node

    @classmethod
    def get_entity_fields(cls, query, id_suffix=None):
        """
        Формируем данные о полях запроса
        :param: query запрос, созданный КО, в формате constructor.query_builder.model.Query
        """

        assert isinstance(query, Query)

        # Корневой узел. Содержит имя запроса
        root_node = dict(id=u''.join([str(query.id), '.', query.name, '__', id_suffix]),
                         leaf=False,
                         iconCls=Icons.PLUGIN,
                         verbose_field=u''.join([query.name, '__', id_suffix]),
                         expanded=True)

        def populate(field):
            """
            Заполняем поля запроса
            """

            (
                id_, verbose_field, alias, _, entity_type, entity_id,
                true_verbose_field
            ) = field
            entity_id = root_node['id']

            node = dict(id_field=''.join([entity_id, '.', id_]),
                        leaf=True,
                        verbose_field=alias or verbose_field,
                        entity_type=EntityTypes.QUERY,
                        entity_id=entity_id,
                        true_verbose_field=alias or true_verbose_field)

            root_node.setdefault('children', []).append(node)

        # Используя прокси класс получаем доступ к select полям.
        # Select-поля всегда имеются.
        # Иначе клиентская часть сообщит о некорректности запроса
        # при сохранении
        proxy_obj = QueryProxy(
            query_id=query.id, query_name=query.name,
            json_query=json.loads(query.json_query)
        )
        fields = proxy_obj.get_selected_fields(id_suffix)
        fields_aggr = proxy_obj.get_group_aggr_fields()

        # Заполняем поля запроса
        map(populate, fields)
        map(populate, fields_aggr)

        # Возвращаем корневой узел
        return root_node

    @classmethod
    def get_entities_fields(cls, ids):
        """
        Для выбранных сущностей, готовим список их select полей
        """
        ids_ = []
        # Идентификатор сущности-запроса имеет вид id.name__timestamp
        ids_dict = {}
        for id_ in ids:
            id__, id_suffix = id_.split('__')
            query_id = int(id__.split('.')[0])
            ids_dict[query_id] = id_suffix
            ids_.append(
                query_id
            )
        # ids = [int(id.split('.')[0]) for id in ids]

        # Получаем список необходимых нам запросов
        queries = Query.objects.filter(id__in=ids_)
        result = []
        for query in queries:
            id_suffix = ids_dict.get(query.id, '')

            res = cls.get_entity_fields(query, id_suffix)

            result.append(res)

        return result

        return [cls.get_entity_fields(query) for query in queries]


class ModelEntityUIProxy(EntityUIProxyInterface):
    """
    Посредник между моделями проекта и UI

    Протокол хранения:
    1)Сущность-модель
        a) Идентификатор  id    = имяПриложения.имяМодели
        б) Название       title = имяМодели
    2)Поле сущности-модели
        a) Идентификатор               id = имяПоля.идентификаторМодели
        б) Идентификатор модели entity_id = идентификаторМодели
        в) Название поля     verbose_field = имяПоля
    """

    # Модели, которые не нужно добавлять. Внутренние модели конструктора.
    EXCLUDE_MODEL_LIST = [
        'Query',
        'Report',
        'ReportQuery',
        'Template',
        'FormField',
        'SubstValues'
    ]

    @classmethod
    def get_entities(cls):
        """
        Получаем список всех моделей
        """

        root_node = dict(
            id=EntityTypes.MODEL,
            iconCls=Icons.FOLDER_TABLE,
            title=EntityTypes.get_entity_type_title(EntityTypes.MODEL),
            leaf=False,
            expanded=True,
            title_verbose=''
        )

        def populate(model):

            node = dict(
                id='.'.join([model._meta.app_label, model.__name__]),
                leaf=True,
                iconCls=Icons.PLUGIN,
                title=model.__name__,
                title_verbose=(
                    model._meta.verbose_name if isinstance(
                        model._meta.verbose_name, basestring
                    ) else ""
                )
            )


            root_node.setdefault('children', []).append(node)

        map(populate, cls._filter_models())

        if not root_node.get('children'):
            root_node = None

        return root_node

    @classmethod
    def _filter_models(cls):
        """
        Фильтр моделей
        """

        # Все модели проекта и окружения
        models = loading.get_models()

        for model in models:
            model_name = model.__name__
            # Добавляем модели не принадлежащие конструктору и не указанные в списке исключений в настройках
            # прикладного проекта.
            if model_name not in cls.EXCLUDE_MODEL_LIST and model_name not in EXCLUDE_MODELS:
                # Если в настройках прикладного проекта указан список необходимых моделей, то фильтруем по
                # этому списку. В противном случае берём все.
                if MODELS and model_name in MODELS or not MODELS:
                    yield model

    @classmethod
    def get_entity_fields(cls, model_id, model_suffix=None):
        """
        Принимает имена модели и приложения, возвращает список полей для UI
        """
        app_name, model_name = model_id.split('.')

        exclude_fields = settings.REPORT_GENERATOR_SETTINGS.get(
            'EXCLUDE_FIELDS',
            {}
        ).get(model_name, set())

        model_class = loading.get_model(app_name, model_name)
        id_ = model_id
        if model_suffix is not None:
            id_ = u''.join([id_, '__', model_suffix])

        root_node = dict(
            id=id_,
            leaf=False,
            iconCls=Icons.PLUGIN,
            verbose_field=u''.join([model_name, '__', model_suffix]),
            true_verbose_field='',
            expanded=True
        )
        #if hasattr(settings, 'EXCLUDE_FIELDS')

        def populate(field):
            if field.attname in exclude_fields:
                return

            if isinstance(field, ForeignKey):
                true_verbose_field = u'ID - ' + (
                    field.verbose_name or field.attname)
            else:
                true_verbose_field = field.verbose_name or field.attname

            node = dict(
                id_field='.'.join([id_, field.attname]),
                # verbose_field = getattr(field, 'verbose_name') or field.name,
                verbose_field=field.name or field.attname,
                true_verbose_field=true_verbose_field,
                leaf=True,
                entity_type=EntityTypes.MODEL,
                entity_id=id_)

            add_tooltip(node, field)

            root_node.setdefault('children', []).append(node)

        def add_tooltip(node, field):
            #node['tooltip'] = 'test1'

            if isinstance(field, CharField):
                res = u'Тип: varchar(%s)' % field.max_length
            elif isinstance(field, IntegerField):
                buffer_ = [u'Тип: integer']
                if field.choices:
                    for number, descr in field.choices:
                        buffer_.append(u'%s: %s' % (number, descr))
                res = u'<br/>'.join(buffer_)
            elif isinstance(field, ForeignKey):
                buffer_ = [u'Тип: ссылка на']
                another_model = field.rel.to
                buffer_.append(
                    u'%s - %s' % (
                        another_model.__name__,
                        another_model._meta.verbose_name or ''
                    )
                )
                res = u'<br/>'.join(buffer_)
            elif isinstance(field, DecimalField):
                res = u'Тип: decimal(%s, %s)' % (field.max_digits,
                                                 field.decimal_places)
            elif isinstance(field, DateTimeField):
                res = u'Тип: datetime'
            elif isinstance(field, DateField):
                res = u'Тип: date'
            elif isinstance(field, TextField):
                res = u'Тип: text'
            elif isinstance(field, BooleanField):
                res = u'Тип: boolean IS NOT NULL'
            elif isinstance(field, NullBooleanField):
                res = u'Тип: boolean IS NULL'
            else:
                res = u'Тип неизвестен'
            node['qtip'] = res

        map(populate, model_class._meta.fields)

        return root_node

    @classmethod
    def get_entities_fields(cls, models_ids):
        """
        """
        result = []
        for model in models_ids:
            list_models = model.split('__')
            model_name = list_models[0]
            model_suffix = None
            if len(list_models) > 1:
                model_suffix = list_models[-1]
            result.append(cls.get_entity_fields(model_name, model_suffix))
        return result

        # return [cls.get_entity_fields(model) for model in models_ids]