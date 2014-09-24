#coding:utf-8
"""
Created on 12.05.2011
@author: Сафиуллин В. А.
"""
from django.db.models import ForeignKey

try:
    from sqlalchemy.engine.url import URL
    from sqlalchemy.ext.sqlsoup import SqlSoup
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import mapper, relationship
    import sqlalchemy as sa
except ImportError:
    # sqlalchemy может быть не установлен
    URL = SqlSoup = declarative_base = mapper = relationship = sa = None


from m3.helpers import logger


#============================= ИСКЛЮЧЕНИЯ ==================================

class AlchemyWrapperError(Exception):
    pass

#=============================== КЛАССЫ ====================================

class SingletonMeta(type):
    def __init__(self, name, bases, dict):
        super(SingletonMeta, self).__init__(name, bases, dict)
        self.instance = None

    def __call__(self, *args, **kw):
        if self.instance is None:
            self.instance = super(SingletonMeta, self).__call__(*args, **kw)
        return self.instance


class SQLAlchemyWrapper(object):
    """
    Класс обёртка, предназначенный для подключения БД SqlAlchemy
    используя настройки Django:
    wrapper = SQLAlchemyWrapper(settings.DATABASES)
    Содержит атрибуты необходимые для управлений БД и выполнения запросов:
    engine - подключение к БД
    metadata - коллекция из таблиц и колонок БД
    session - сессия для запросов
    """
    __metaclass__ = SingletonMeta

    # Карта соответствия между драйверами Django и SqlAlchemy
    DRIVER_MAP = {
        "django.db.backends.sqlite3": "sqlite",
        "django.db.backends.postgresql_psycopg2": "postgresql",
        "django.db.backends.mysql": "mysql",
    }

    ERROR_NO_PK = 'could not assemble any primary key columns for mapped table'

    _models_map_cache = None

    def __init__(self, db_config):
        # Создаем движок БД
        default_db = db_config['default']
        url = self._create_url(default_db)
        self.engine = sa.create_engine(url)

        # Реверс инжиниринг БД ;)
        self.soup = SqlSoup(self.engine)
        self.soup._metadata.reflect()
        self.metadata = self.soup._metadata
        self.session = self.soup.session

    def _create_url(self, db_config):
        """ Возвращает URL для соединения с БД """
        django_driver = db_config['ENGINE']
        driver = self.DRIVER_MAP.get(django_driver)
        if not driver:
            raise AlchemyWrapperError('Driver %s was not found in map' % django_driver)

        url = URL(
            drivername = driver,
            username = db_config['USER'],
            password = db_config['PASSWORD'],
            host = db_config['HOST'],
            port = db_config['PORT'] or None, # От пустой строки алхимия падает
            database = db_config['NAME'])
        return url

    def create_map_class(self, class_name, table):
        """ Возвращает класс обертку над таблицей алхимии """
        base = declarative_base(name=str(class_name))
        try:
            return mapper(base, table)
        except Exception as e:
            msg = str(e)
            if msg.find(self.ERROR_NO_PK) > 0:
                logger.warning(msg)
                return
            raise e

    def _check_installed_apps(self, model):
        """
        Проверяет, может ли модель с именем model_name быть подключена к проекту.
        Это нужно потому, что в приложениях проекта могут быть импорты из contrib'ов,
        которые не подключены в INSTALLED_APPS и их модели не существуют в БД.
        Хотя это нарушает принцип IoC, но прециденты встречаются.
        """
        for app_name in settings.INSTALLED_APPS:
            pure_module_name = model.__module__.replace('.models', '')
            if pure_module_name.startswith(app_name):
                return True

        return False

    def _create_accessor_property(self, db, mapped_table, property_name, field):
        """
        Создает свойство указывающее через JOIN на другую таблицу
        """
        # Получаем алхимическую таблицу и поле с которой будет связывание
        related_model_name = field.rel.to._meta.object_name # Мегахак!
        related_field_name = field.rel.field_name
        related_mapped_table = db[related_model_name]

        left_column = related_mapped_table.columns[related_field_name]
        right_column = mapped_table.columns[field.attname]
        primaryjoin = (left_column == right_column)

        # Добавляем свойство
        property_value = relationship(related_mapped_table, primaryjoin=primaryjoin)
        mapped_table.add_property(property_name, property_value)

    def _get_alchemy_table(self, model):
        """
        Возвращает алхимическую таблицу по модели Django
        """
        table_name = model._meta.db_table
        try:
            return self.soup._metadata.tables[table_name]
        except KeyError:
            logger.warning('Table %s was not reflected in SqlAlchemy metadata' % table_name)

    def get_models_map(self, create_mappers=False, create_properties=True):
        """
        Возвращает объект для быстрого доступа к таблицам SqlAlchemy.
        Атрибуты объекта имеют имена соответствующих моделей Django, а
        их значения - метатаблицы алхимии.
            create_mappers - вместо таблиц алхимии создаются map-объекты
            create_properties - в map-объектах создаются свойства по аналогии с ассессорами Django
        """
        if self._models_map_cache:
            return self._models_map_cache

        try:
            from django.db.models.loading import cache
        except ImportError:
            raise AlchemyWrapperError('Cross import from settings.py')

        meta_collection = {}

        model_collection = ModelCollection()
        for model in cache.get_models():
            table = self._get_alchemy_table(model)

            if table is not None:
                attr_name = model._meta.object_name

                if create_mappers:
                    table = self.create_map_class(attr_name, table)
                    if table is None:
                        continue

                meta_collection[attr_name] = model._meta
                if not model_collection.has_key(attr_name):
                    model_collection[attr_name] = table
                else:
                    logger.warning('Model Collection already have model with name %s' % attr_name)

        if create_mappers and create_properties:
            # Не все так просто для MAP-объектов. Для правильной работы
            # им нужно иметь такие же свойства, как ассессоры в Django
            for attr_name, mapped_table in model_collection.items():
                meta = meta_collection[attr_name]

                # Нужно создать свойства для ForeignKey
                for field in meta.fields:
                    if isinstance(field, ForeignKey) and field.attname.endswith('_id'):

                        # Может встретиться такое западло, когда в БД колонка не является FK,
                        # но в модели Django она каким-то магическим образом помечена как FK!
                        # Это легко проверить, но в будущем возможно придется найти решение.
                        alchemy_col = mapped_table.columns[field.attname]
                        if not alchemy_col.foreign_keys:
                            logger.warning('Column %s is not foreign key but defined as it in Django' % alchemy_col)
                            continue

                        # Имя свойства такое же как FK, только без _id
                        property_name = field.attname[:-3]

                        self._create_accessor_property(model_collection, mapped_table, property_name, field)

                #TODO: Нужно создать свойства для RelatedManager

        self._models_map_cache = model_collection
        return model_collection


class ModelCollection(dict):
    """ Объект хранящий атрибуты с именами моделей Django и значениями Table """

    def __getattr__(self, name):
        """ Доступ к значениям словаря через точку """
        return self[name]

    def __setitem__(self, k, v):
        """ При добавлении пары в словарь также появляется одноименный атрибут """
        super(ModelCollection, self).__setitem__(k, v)
        setattr(self, k, v)
