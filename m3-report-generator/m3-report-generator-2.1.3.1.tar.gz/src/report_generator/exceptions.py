#coding: utf-8

"""
Все исключения проекта.
"""
class ReportGeneratorError(Exception):
    """
    Базовое исключение сервера генератора отчетов.
    """

class EntityException(Exception):
    """
    Базовое исключение для сущностей
    """

class SettingsException(Exception):
    """
    Неверные настройки
    """

class DjangoModelNotFound(EntityException):
    """
    Исключение модель не найдена
    """
    def __init__(self, model_name, *a, **k):
        super(DjangoModelNotFound, self).__init__(self, *a, **k)
        self.model_name = model_name

    def __str__(self):
        return u'В кэше моделей Django не удалось найти модель по имени %s ' % self.model_name


class DBTableNotFound(EntityException):
    """
    Алхимия не нашла таблицу для модели Django
    """
    def __init__(self, model_name, *a, **k):
        super(DBTableNotFound, self).__init__(self, *a, **k)
        self.model_name = model_name

    def __str__(self):
        return u'SqlAlchemy не удалось определить таблицу БД для модели Django с именем %s' % self.model_name


class EntityNotFound(EntityException):
    """
    Не найдена сущность
    """
    def __init__(self, entity_name, *a, **k):
        super(EntityNotFound, self).__init__(self, *a, **k)
        self.entity_name = entity_name

    def __str__(self):
        return u'Не удалось найти Entity с именем %s' % self.entity_name


class DBColumnNotFound(EntityException):
    """
    Не найдена колонка в модели
    """
    def __init__(self, model_name, field_name, *a, **k):
        super(DBColumnNotFound, self).__init__(self, *a, **k)
        self.model_name = model_name
        self.field_name = field_name

    def __str__(self):
        return u'В модели %s не найдена колонка %s' % (self.model_name, self.field_name)

class ReportException(Exception):
    """
    Ошибки отчета
    """
    pass