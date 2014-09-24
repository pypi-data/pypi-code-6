#coding:utf-8
'''
Created on 22.04.2011

@author: akvarats
'''

#===============================================================================
# TODO и оставшиеся непонятки
# 1. Какое дефлтное значение должно быть у поля типа Date или DateTime
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#===============================================================================

try:
    from south.utils import ask_for_it_by_name
    from south.db import db, dbs
except ImportError:
    # South может быть не установлен
    ask_for_it_by_name = db = dbs = None


#===============================================================================
# Описание врапперов над структурой элементов базы данных (таблиц и их полей)
#===============================================================================

class DBTable(object):
    '''
    Враппер над таблицами в базе данных
    '''
    def __init__(self, name=''):
        self.name = name # имя таблицы в базе данных
        self.fields = [] # список полей для таблицы в базе данных

    def find_field(self, field_name):
        '''
        Метод находит поле с указанным именем. Если поле не найдено в описании
        таблицы, то возвращается None
        '''
        for field in self.fields:
            if field.name == field_name:
                return field
        return None

class NullTable(DBTable):
    '''
    Фейковый класс, который представляет собой пустую, несуществующую таблицу.

    Данный класс необходим для того, чтобы дать понять механизмам миграции о том,
    что таблица не существует в базе данных
    '''
    def __init__(self):
        super(NullTable, self).__init__(name='')

#===============================================================================
# Классы для описания полей таблиц базы данных
#===============================================================================

class DBField(object):
    '''
    Враппер над полем таблицы в базе данных
    '''
    def __init__(self, name, allow_blank=True, indexed=True, default=None):
        self.name = name # наименование поля
        self.django_type = '' # имя в базе данных
        self.indexed = indexed # признак создания индекса для поля
        self.allow_blank = allow_blank
        self.default = default

    def django_field(self):
        '''
        Возвращает выражение для создания поля в виде джанговской модели
        '''
        field_class = ask_for_it_by_name(self.django_type)
        params = {'blank': self.allow_blank,
                  'db_index': self.indexed,
                  'default': self.default,}

        params = self.set_params(params)
        return field_class(**params)

    def set_params(self, params):
        '''
        Заполняет параметры поля, которые будут переданы в параметры
        конструктора при создании экземпляра django.db.models.fields.Field.
        '''
        return params

class IDField(DBField):
    '''
    Поле, являющееся идентификатором записи в таблице базы данных
    '''
    def __init__(self):
        super(IDField, self).__init__(name='id', indexed=True, allow_blank=False)
        self.django_type = 'django.db.models.fields.AutoField'


    def set_params(self, params):
        '''
        Для данного поля необходимо, чтобы в параметрах конструктора было
        определено только primary_key = True
        '''
        return {'primary_key': True}

class CharField(DBField):
    '''
    Поле со строковым типов в базе данных
    '''
    def __init__(self, name = '', max_length=100, allow_blank=True, indexed=False, default=''):
        super(CharField, self).__init__(name=name, allow_blank=allow_blank, indexed=indexed, default=default)
        self.max_length = max_length
        self.django_type = 'django.db.models.fields.CharField'

    def set_params(self, params):
        params['max_length'] = self.max_length
        return params

class DateField(DBField):

    def __init__(self, name='', allow_blank=True, indexed=False, auto_now=False, auto_now_add=False, default=None):
        super(DateField, self).__init__(name=name, allow_blank=allow_blank, indexed=indexed, default=None)
        self.auto_now = True
        self.auto_now_add = True
        self.django_type = 'django.db.models.fields.DateField'

    def set_params(self, params):
        params['auto_now'] = self.auto_now
        params['auto_now_add'] = self.auto_now_add
        return params


class DateTimeField(DateField):

    def __init__(self, name='', allow_blank=True, indexed=False, auto_now=False, auto_now_add=False, default=None):
        super(DateTimeField, self).__init__(name=name, allow_blank=True, indexed=indexed, auto_now=False, auto_now_add=False, default=None)
        self.django_type = 'django.db.models.fields.DateTimeField'

class TextField(DBField):

    def __init__(self, name='', allow_blank=True, indexed=False):
        super(TextField, self).__init__(name=name, allow_blank=allow_blank, indexed=indexed)
        self.default = ''
        self.django_type = 'django.db.models.fields.TextField'

    def set_params(self, params):

        params['default'] = self.default
        return params

class IntegerField(DBField):
    '''
    Поле с целочисленным значением
    '''
    def __init__(self, name='', indexed=False, default=0):
        super(IntegerField, self).__init__(name=name, allow_blank=True, indexed=indexed, default=default)
        self.django_type = 'django.db.models.fields.IntegerField'

class DecimalField(DBField):
    '''
    Числовое поле
    '''
    def __init__(self, name='', indexed=False, max_digits=15, decimal_places=2, default=0):
        super(DecimalField, self).__init__(name=name, indexed=indexed, allow_blank=False, default=default)
        self.max_digits = max_digits
        self.decimal_places = decimal_places
        self.django_type = 'django.db.models.fields.DecimalField'

    def set_params(self, params):
        params['max_digits'] = self.max_digits
        params['decimal_places'] = self.decimal_places
        return params

#===============================================================================
# Механизмы для миграции таблиц базы данных
#===============================================================================
class BaseMigrator(object):
    '''
    Базовый мигратор, выполняющий функции изменения структуры таблиц в базе
    данных.
    '''
    def __init__(self, db_name='', manual_transaction=False):
        '''
        @param db_name: ссылка на объект базы данных
        '''
        self.db_name = db_name
        self.manual_transaction = manual_transaction

    def start_transaction(self):
        '''
        Метод, начинающий транзакцию по изменению таблиц базы данных
        '''
        self._db().start_transaction()

    def commit_transaction(self):
        '''
        Метод, фиксирующий изменения в транзакции внесения изменений в структуру
        таблиц.
        '''
        self._db().commit_transaction()

    def rollback_transaction(self):
        '''
        Откат изменений в таблицах базы данных.
        '''
        self._db().rollback_transaction()


    def migrate(self, to_version, from_version=None):
        '''
        Метод миграции структуры таблицы

        @param to_version: представляет собой объект типа DBTable, который хранит
        описание
        '''

        # 1. получаем диффку между таблицами
        commands = self._diff_versions(from_version, to_version)

        # 2. выполняем команды на изменение базы данных
        if not self.manual_transaction:
            self.start_transaction()
        try:
            for command in commands:
                command.execute(self.db_name)
        except:
            if not self.manual_transaction:
                self.rollback_transaction()
            raise
        else:
            if not self.manual_transaction:
                self.commit_transaction()


    def create_table(self, table):
        '''
        Обертка над BaseMigrator.migrate, которая создает базу данных
        '''
        self.migrate(to_version=table, from_version=NullTable())

    def drop_table(self, table):
        '''
        Обертка над BaseMigrator,migrate, которая удаляет базу данных
        '''
        self.migrate(to_version=NullTable(), from_version=table)


    def _db(self):
        '''
        Вовзвращает базу данных, в которой необходимо выполнить команду.

        В случае, если dn_name не указано, то команда выполняется в базе данных
        default.
        '''
        return dbs[self.db_name] if self.db_name else db


    def _get_active_version(self, table_name):
        '''
        Метод, который возвращает текущее активное описание таблицы.

        Данный метод необходимо перекрывать в дочерних классах, которые
        собственно и реализуют поведение конкретного механизма управления
        динамическими таблицами.
        '''
        return None

    def _register_active_version(self, table_name, active_version):
        '''
        Метод регистрирует текущую активную версию базы данных. Данный метод
        требует переопределения в конкретных методах миграции.
        '''
        pass

    #===========================================================================
    # Внутренние приватные методы, которые
    #===========================================================================

    def _diff_versions(self, left_version, right_version):
        '''
        Формирует список команд, с помощью таблица с описанием left_version
        должна быть переведена в таблицу с описанием right_version
        '''
        # внимание! с целью обеспечения читаемости кода в данном методе
        # есть несколько точек выхода. берегите себя.
        commands = []

        # 0. если левой версии не существует, то надо сломиться и попытаться
        # получить её через специальные методы класса
        cleaned_right = right_version
        if not cleaned_right:
            raise Exception(u'В процедуре миграции правая версия таблицы должна быть всегда задана')

        cleaned_left = left_version if left_version else self._get_active_version(cleaned_right.name)
        if not cleaned_left:
            raise Exception(u'Не удалось получить левую версию таблицы "%s".', cleaned_right.name)

        if (not isinstance(cleaned_left, NullTable) and
            not isinstance(cleaned_right, NullTable) and
            cleaned_left.name != cleaned_right.name):
            raise Exception(u'Миграция таблиц с разными именами в левой и правой частях запрещена.')

        if (not isinstance(cleaned_left, DBTable) and
            not isinstance(cleaned_right, DBTable)):
            raise Exception(u'При выполнении миграции либо в левой, либо в правой части должно находиться описание реальной таблицы (экземпляра класса DBTable)')

        db_table = cleaned_right if isinstance(cleaned_left, NullTable) else cleaned_left

        # 1. Если правая версия является NullTable, то мы имеем дело с
        # командой на удаление таблицы, если левая версия - то создания таблицы
        if isinstance(cleaned_right, NullTable):
            commands.append(DropTableCommand(cleaned_left))
            # поскольку дальше без вариантов, то мы завершаем выполнение
            return commands

        if isinstance(cleaned_left, NullTable):
            commands.append(CreateTableCommand(cleaned_right))
            return commands

        # 2. проходимся по полям левой таблицы
        for left_field in cleaned_left.fields:
            right_field = cleaned_right.find_field(left_field.name)

            if not right_field:
                commands.append(RemoveFieldCommand(db_table, left_field))
                continue

            if ((left_field.indexed and not right_field.indexed) or
                (right_field.indexed and not left_field.indexed) or
                (left_field.allow_blank and not right_field.allow_blank) or
                (right_field.allow_blank and not left_field.allow_blank)):

                # формируем команду на изменение параметров поля
                commands.append(AlterFieldCommand(db_table, right_field))

        # 3. проходимся по полям правой таблицы
        for right_field in cleaned_right.fields:
            left_field = cleaned_left.find_field(right_field.name)
            if not left_field:
                commands.append(AppendFieldCommand(db_table, right_field))

        return commands

class DDLCommand(object):
    '''
    Общий класс команды, с помощью которой происходит изменение описания таблицы
    базы данных
    '''
    def __init__(self, db_table):
        '''
        @param db_table: описание таблицы, над которой выполняется DDL команда
        '''
        self.db_table = db_table

    def execute(self, db_name=''):
        '''
        Метод выполнения команды
        '''
        raise NotImplemented(u'Метод DDLCommand.execute() необходимо перегружать в дочерних классах.')

    def _db(self, db_name=''):
        '''
        Вовзвращает базу данных, в которой необходимо выполнить команду.

        В случае, если dn_name не указано, то команда выполняется в базе данных
        default.
        '''
        return dbs[db_name] if db_name else db


class CreateTableCommand(DDLCommand):
    '''
    Команда на создание таблицы
    '''
    def __init__(self, db_table):
        super(CreateTableCommand, self).__init__(db_table)

    def execute(self, db_name=''):
        '''
        Реализуется команда на создание таблицы в базе данных
        '''
        fields = []
        for field in self.db_table.fields:
            fields.append((field.name, field.django_field()))

        self._db(db_name).create_table(self.db_table.name, tuple(fields))


class DropTableCommand(DDLCommand):
    '''
    Команда на удаление таблицы из базы данных
    '''
    def __init__(self, db_table):
        super(DropTableCommand, self).__init__(db_table)

    def execute(self, db_name=''):

        self._db(db_name).delete_table(self.db_table.name)


class BaseFieldCommand(DDLCommand):
    '''
    Базовая команда, предназначенная для работы с полями
    '''
    def __init__(self, db_table, db_field):
        '''
        @param db_table: таблица, над которой выполняется команда (объект класса
            DBTable)
        @param db_field: поле, над которым выполняется команда (объект класса
            DBField)
        '''
        super(BaseFieldCommand, self).__init__(db_table)
        self.db_field = db_field

class AppendFieldCommand(BaseFieldCommand):
    '''
    Команда на добавление поля в таблицу
    '''
    def __init__(self, db_table, db_field):
        super(AppendFieldCommand, self).__init__(db_table, db_field)

    def execute(self, db_name=''):
        self._db(db_name).add_column(self.db_table.name, self.db_field.name, self.db_field.django_field())


class RemoveFieldCommand(BaseFieldCommand):
    '''
    Команда на удаление поля из таблицы
    '''
    def __init__(self, db_table, db_field):
        super(RemoveFieldCommand, self).__init__(db_table, db_field)

    def execute(self, db_name=''):

        self._db(db_name).delete_column(self.db_table.name, self.db_field.name)

class AlterFieldCommand(BaseFieldCommand):
    '''
    Команда на изменение параметров поля
    '''

    def __init__(self, db_table, db_field):
        super(AlterFieldCommand, self).__init__(db_table=db_table, db_field=db_field)

    def execute(self, db_name=''):
        self._db(db_name).alter_column(self.db_table.name, self.db_field.name, self.db_field.django_field())

class AppendFieldIndexCommand(BaseFieldCommand):
    '''
    Команда на добавление индекса на поле таблицы

    @deprecated: эту хрень заменяет команда AlterFieldCommand
    '''
    def __init__(self, db_table, db_field):
        super(AppendFieldIndexCommand, self).__init__(db_table, db_field)

class RemoveFieldIndexCommand(BaseFieldCommand):
    '''
    Команда на добавление индекса на поле таблицы

    @deprecated: эту хрень заменяет команда AlterFieldCommand
    '''
    def __init__(self, db_table, db_field):
        super(RemoveFieldIndexCommand, self).__init__(db_table, db_field)

class AllowFieldBlankCommand(BaseFieldCommand):
    '''
    Команда, которая разрешает заполнение поля пустыми значениями

    @deprecated: эту хрень заменяет команда AlterFieldCommand
    '''
    def __init__(self, db_table, db_field):
        super(AllowFieldBlankCommand, self).__init__(db_table, db_field)

class ForbidFieldBlankCommand(BaseFieldCommand):
    '''
    Команда, которая запрещает заполнение поля пустыми значениями

    @deprecated: эту хрень заменяет команда AlterFieldCommand
    '''
    def __init__(self, db_table, db_field):
        super(ForbidFieldBlankCommand, self).__init__(db_table, db_field)
