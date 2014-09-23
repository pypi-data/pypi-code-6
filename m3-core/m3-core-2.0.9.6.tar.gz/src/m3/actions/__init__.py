#coding:utf-8
import threading
import inspect
import abc
import re
import importlib
import sys
import time

from django.conf import settings
from django.utils.importlib import import_module
from django import http

from django.utils.log import logger

from results import *

from exceptions import *

import utils

from context import (
    ActionContext,
    ActionContextDeclaration,
    DeclarativeActionContext,
    RequiredFailed,
    ContextBuildingError,
    CriticalContextBuildingError,
)

from metrics import create_statsd_client

_STATSD_CLIENT = create_statsd_client(settings)


ACD = ActionContextDeclaration


_clean_url = lambda s: re.sub(r'^[/^]*(.*?)[$/]*$', r'\1', s)


def _import_by_path(path):
    """
    Импортирует объект по пути @path вида "full.package.path.to.some_object"
    """
    match = re.match(r'^(?:(.*)\.)?([^.]+)$', path)
    if match is None:
        raise ValueError(u'Wrong path to import: %r' % path)
    module_name, obj_name = match.groups()
    module = importlib.import_module(module_name)
    return getattr(module, obj_name)


def _name_of(obj):
    """
    Возвращает для указанного объекта имя вида
    "package.ClassOfObject"
    или
    "package.ClassOfParent.ClassOfObject", если obj имеет атрибут "parent"
    """

    def cls_name(obj):
        return (obj if inspect.isclass(obj) else obj.__class__).__name__

    parent = getattr(obj, 'parent', None)
    if parent:
        parent = '%s.' % cls_name(parent)
    else:
        parent = ''

    package = inspect.getmodule(obj).__name__

    obj = cls_name(obj)

    return '%s.%s%s' % (package, parent, obj)


#==============================================================================
# Абстрактный механизм проверки прав и его реализация,
# проверяющая права через механизм django.contrib.auth.models.User.has_perm
#==============================================================================
class AbstractPermissionChecker(object):
    """
    Абстрактный механизм проверки прав
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def has_action_permission(self, request, action, subpermission=None):
        """
        Метод должен возвращать True, если выполнение @action
        допустимо в контексте запроса @request
        """
        pass

    @abc.abstractmethod
    def has_pack_permission(self, request, pack, permission):
        """
        Метод должен возвращать True, если действие,
        характеризуемое парой @pack/@permission,
        допустимо в контексте запроса @request
        """
        pass

    @staticmethod
    def get_perm_code(action_or_pack, subpermission=None):
        '''
        Возвращает код действия, для контроля прав доступа
        '''
        code = action_or_pack.get_absolute_url()
        # уберем из кода префикс системы,
        # т.к. код права должен быть относительным
        if hasattr(settings, 'ROOT_URL') and (
                code.startswith(settings.ROOT_URL)):
            code = code[len(settings.ROOT_URL):]
        if subpermission:
            code = '%s#%s' % (code, subpermission)
        return code


class AuthUserPermissionChecker(AbstractPermissionChecker):
    """
    Backend, проверяющий права через
    django.contrib.auth.models.User.has_perm

    Требует подключения в проекте session-middleware, т.к. опирается
    на наличие в request атрибута 'user',
    указывающего на текущего пользователя
    """
    def has_action_permission(self, request, action, subpermission=None):
        """
        Метод должен возвращать True, если выполнение @action
        допустимо в контексте запроса @request
        """
        # контракт
        assert isinstance(action, Action)
        assert isinstance(action.parent, ActionPack)
        if subpermission:
            assert isinstance(subpermission, str)

        # если ползователя нет (аноним) - прав тоже нет
        if not request.user:
            return False

        result = True
        if action.need_check_permission:
            if subpermission:
                assert (
                    subpermission in action.sub_permissions or
                    subpermission in action.parent.sub_permissions
                ), (
                    u'Подправо ("%s") должно быть описано в экшне или паке'
                    % subpermission
                )
                result = request.user.has_perm(
                    action.get_perm_code(subpermission))
            else:
                result = request.user.has_perm(action.get_perm_code())
        return result

    def has_pack_permission(self, request, pack, permission):
        """
        Метод должен возвращать True, если действие,
        характеризуемое парой @pack/@permission,
        допустимо в контексте запроса @request
        """
        assert isinstance(pack, ActionPack)
        if permission:
            assert isinstance(permission, str)

        result = True
        if pack.need_check_permission:
            assert permission in pack.sub_permissions, (
                u'Подправо ("%s") должно быть описано в паке' % permission)
            result = request.user.has_perm(pack.get_perm_code(permission))
        return result


class BypassPermissionChecker(AbstractPermissionChecker):
    """
    Механизм проверки прав, "разрешающий всем и всё"
    """
    def has_action_permission(self, request, action, subpermission=None):
        return True

    def has_pack_permission(self, request, pack, permission):
        return True


class LegacyPermissionChecker(AbstractPermissionChecker):
    """
    Мех-м проверки прав, созданный для совместимости со старыми проектами
    """
    @staticmethod
    def get_perm_code(pack_or_action, subpermission=None):
        code = pack_or_action.get_absolute_url()
        # уберем из кода префикс системы,
        # т.к. код права должен быть относительным
        if hasattr(settings, 'ROOT_URL') and (
                code.startswith(settings.ROOT_URL)):
            code = code[len(settings.ROOT_URL):]
        if subpermission:
            code = '%s#%s' % (code, subpermission)
        return code

    def has_action_permission(self, request, action, subpermission=None):
        '''
        Проверка пава на выполнение действия для указанного пользователя
        '''
        assert isinstance(action.parent, ActionPack)
        # Если в наборе действий need_check_permission=True,
        # а в самом действии False, то права не проверяются
        # Если в наборе действий need_check_permission=True,
        # и в самом действии True, то права проверяются
        # Если в наборе действий need_check_permission=False,
        # а в самом действии True, то права не проверяются
        # Если в наборе действий need_check_permission=False,
        # а в самом действии False, то права не проверяются
        # Т.е. права проверяются только,
        # если в наборе действий и в действии включена проверка прав
        # Признак need_check_permission в вышестоящих наборах действий
        # не влияет на решение, т.к. в тех наборах свои действия

        # Проверим, что в действии и наборе разрешена проверка прав
        user_obj = request.user
        code = self.get_perm_code(action, subpermission)
        if action.need_check_permission and (
                action.parent.need_check_permission):
            # если пользователя нет, значит аноним - ему дадим отпор
            if user_obj:
                # проверим что права на выполнение есть
                return user_obj.has_perm(code)
            else:
                return False
        else:
            return True

    def has_pack_permission(self, request, pack, permission):
        '''
        Проверка на внутреннее право пака для указанного пользователя
        '''
        assert isinstance(permission, str)
        # Подчиненные права набора действий
        # проверяются только в случае разрешения проверки в наборе действий
        # Если переданный код не прописан в правах этого действия,
        # то это не наш код - значит всё разрешено
        user_obj = request.user
        if pack.need_check_permission and permission in pack.sub_permissions:
            # если пользователя нет, значит аноним - ему дадим отпор
            if user_obj:
                # проверим что права на выполнение есть
                return user_obj.has_perm(self.get_perm_code(pack, permission))
            else:
                return False
        return True


#========================== экземпляр проверятеля прав ========================
class LazyContainer(object):
    """
    Ленивая обёртка для объектов, указываемых в settings.
    Предназначена для позднеё загрузки объектов - по первому обращению
    """

    def __init__(self, fabric):
        self._fabric = fabric

    def _get_obj(self):
        if not hasattr(self, '_cache'):
            self._cache = self._fabric()
        return self._cache

    def __getattr__(self, attr):
        if attr == '_cache':
            return super(LazyContainer, self).__getattribute__(attr)
        else:
            return getattr(self._get_obj(), attr)


def _permission_checker_fabric():
    """
    Получение экземпляра permission checker
    """
    _OLD_PERMISSION_CHECKING = getattr(
        settings, 'CONTROLLER_SHOULD_USE_OLD_PERMISSION_CHECKING', False)

    if _OLD_PERMISSION_CHECKING:
        # backend проверки прав, совместимый со старыми проектами
        result = LegacyPermissionChecker
    else:
        path = getattr(settings, 'M3_PERMISSION_CHECKER', None)
        if path is None:
            # если backend не задан в настройках, то исходим из того,
            # подключены ли пользователи Django
            if 'django.contrib.auth' in settings.INSTALLED_APPS:
                result = AuthUserPermissionChecker
            else:
                result = BypassPermissionChecker
        else:
            # в настройках можно указать свой backend для проверки прав
            if isinstance(path, str):
                # указан строкой - импортируем
                result = _import_by_path(path)
            if not (inspect.isclass(result) and issubclass(
                    result, AbstractPermissionChecker)):
                raise TypeError(
                    u'M3_PERMISSION_CHECKER option value must be '
                    u'a string or class!'
                )
    # бэкенд инстанцируется для дальнейшего использования
    return result()


# ленивый экземпляр бэкенда проверки прав
_permission_checker = LazyContainer(_permission_checker_fabric)


#========================== ИСКЛЮЧЕНИЯ ========================================
class ActionException(Exception):
    def __init__(self, clazz, *args, **kwargs):
        super(Exception, self).__init__(*args, **kwargs)
        self.clazz = clazz


class ActionNotFoundException(ActionException):
    """
    Возникает в случае, если экшен не найден ни в одном контроллере
    """
    def __str__(self):
        return 'Action "%s" not registered in controller/pack' % self.clazz


class ActionPackNotFoundException(ActionException):
    """
    Возникает в случае, если пак не найден ни в одном контроллере
    """
    def __str__(self):
        return 'ActionPack "%s" not registered in controller/pack' % self.clazz


class ReinitException(ActionException):
    """
    Возникает, если из-за неправильной структуры паков один и тот же
    экземпляр экшена может быть повторно инициализирован неверными значениями.
    """
    def __str__(self):
        return 'Trying to overwrite class "%s"' % self.clazz


class ActionUrlIsNotDefined(ActionException):
    """
    Возникает если в классе экшена не задан атрибут url.
    Это грозит тем, что контроллер не сможет найти и вызвать
    данный экшен при обработке запросов.
    """
    def __str__(self):
        return (
            'Attribute "url" is not defined '
            'or empty in action "%s"' % self.clazz
        )


#==============================================================================
class Action(object):
    '''
    Базовый класс, от которого должны наследоваться все Action'ы в системе.
    Заменяет собой классические вьюшки Django.
    '''

    # Часть адреса запроса которая однозначно определяет его принадлежность к
    # конкретному Action'у
    url = ''

    # Ссылка на ActionPack к которому принадлежит данный Action
    parent = None

    # Ссылка на контроллер к которому принадлежит данный Action
    controller = None

    # Наименование действия для отображения
    verbose_name = None

    # Признак обработки прав доступа,
    # при выполнении действия (по-умолчанию отключен)
    # Как обрабатывается этот признак - смотри в has_permission
    need_check_permission = False

    # Словарь внутренних прав доступа, используемых в действии
    # ключ - код права, который совмещается с кодом действия
    # значение - наименование права
    # Пример: {'tab2':u'Редактирование вкладки Доп. сведения',
    #          'work_visible':u'Просмотр сведений о работе'}
    # Общий код права доступа будет иметь вид:
    #     /edit#tab2 и /edit#work_visible соответственно
    # Как обрабатывается этот список - смотри в has_sub_permission
    sub_permissions = {}

    # Логический путь действия в прикладной системе.
    # Используется только для отображения и группировки
    # действий с одинаковым путем.
    # Также может использоваться для создания меню.
    # Например, путь может быть: "Справочники\Общие" или "Реестры"
    path = None

    def get_sub_permission_code(self, sub_code):
        # метод оставлен для совместимости
        return self.get_perm_code(sub_code)

    def has_sub_permission(self, user_obj, sub_code, request):
        # метод оставлен для совместимости
        return self.has_perm(request, sub_code)

    def get_permission_code(self):
        # метод оставлен для совместимости
        return self.get_perm_code()

    def has_permission(self, user_obj, request):
        # метод оставлен для совместимости
        return self.has_perm(request)

    #================= НОВЫЙ ИНТЕРФЕЙС ПРОВЕРКИ ПРАВ ==========================
    def has_perm(self, request, subpermission=None):
        """
        Интерфейсный метод проверки (под)прав экшна.

        Использовать ВМЕСТО has_permission/has_sub_permission
        """
        return _permission_checker.has_action_permission(
            request, self, subpermission)

    def get_perm_code(self, subpermission=None):
        """
        Получение кода (под)права
        """
        # по-умолчанию код генерится backend`ом
        return _permission_checker.get_perm_code(self, subpermission)
    #==========================================================================

    def pre_run(self, request, context):
        """
        Метод для предварительной обработки
        входящего запроса *request* и контекста *context*,
        перед передачений в run().
        Если возвращает значение отличное от None,
        обработка запроса прекращается и результат
        уходит во вьюшку контроллера.
        """
        pass

    def post_run(self, request, context, response):
        """
        Метод для постобработка результата работы Action'а.
        Принимает исходный запрос *request*,
        результат работы run() *response*
        и извлеченный контекст *context*.
        """
        pass

    def context_declaration(self):
        """
        Метод декларирует необходимость наличия
        определенных параметров в контексте.
        Должен возвращать список из экземпляров *ActionContextDeclaration*
        либо
        словарь описания контекста для *DeclarativeActionContext*
        """
        pass

    def run(self, request, context):
        """
        Обеспечивает непосредственное исполнение запроса
        (аналог views в Django).
        Обязательно должен быть перекрыт в наследнике.
        Должен возвращать экземпляр одного из наследников *ActionResult*
        """
        raise NotImplementedError()

    @classmethod
    def absolute_url(cls):
        '''
        Возвращает полный путь до действия.
        НО при условии что этот экшен используется
        ТОЛЬКО В ОДНОМ ПАКЕ И КОНТРОЛЛЕРЕ, иначе валим всех!
        Ищет перебором!
        '''
        url = ControllerCache.get_action_url(cls)
        if not url:
            raise ActionNotFoundException(clazz=cls)
        return url

    def get_packs_url(self):
        """
        Возвращает строку, полный адрес от контроллера до текущего экшена
        """
        assert isinstance(self.parent, ActionPack)
        path = []
        pack = self.parent
        while pack is not None:
            path.append(pack.url)
            pack = pack.parent
        return ''.join(reversed(path))

    def get_absolute_url(self):
        '''
        Возвращает полный путь от хоста до конечного экшена
        @deprecated: Дублирует absolute_url
        '''
        #TODO: Переписать, т.к. этот код дублирует функции контроллера
        assert isinstance(self.controller, ActionController), (
            '%s is not actioncontroller in %s' % (self.controller, self))
        # Очищаем от мусора рег. выр.
        url = self.url.replace('$', '')
        return self.controller.url + self.get_packs_url() + url

    @classmethod
    def get_verbose_name(cls):
        return cls.verbose_name if cls.verbose_name else cls.__name__


class ActionPack(object):
    '''
    Базовый класс для всех ActionPack'ов.
    Предназначен для хранения в себе других
    экшенов и паков, схожих по целям.
    '''
    # Адрес экшенпака
    url = ''

    # Ссылка на вышестоящий пакет, тот в котором зарегистрирован данный пакет
    parent = None

    # Наименование Набора действий для отображения
    verbose_name = None

    # Признак обработки прав доступа,
    # при выполнении дочерних действий (по-умолчанию отключен)
    # Как обрабатывается этот признак - смотри в Action.has_permission
    need_check_permission = False

    # Словарь внутренних прав доступа, используемых в наборе действий
    # ключ - код права, который совмещается с адресом (кодом) набора действий
    # значение - наименование права
    # Пример: {'edit':u'Редактирование записи'}
    # Общий код права доступа будет иметь вид: /users#edit
    # Как обрабатывается этот список - смотри в has_sub_permission
    sub_permissions = {}

    # Логический путь набора действий в прикладной системе.
    # Используется только для отображения
    # и группировке наборов с одинаковым путем.
    # Также может использоваться для создания меню.
    # Например, путь может быть: "Справочники\Общие" или "Реестры"
    path = None

    def __init__(self):
        # Список действий зарегистрированных на исполнение в данном пакете
        self.actions = []
        # Список дочерних пакетов (подпакетов),
        # зарегистрированных на исполнение в данном пакете
        self.subpacks = []

    @classmethod
    def absolute_url(cls):
        """
        Возвращает полный адрес (url) от контроллера до текущего экшенпака
        """
        path = [cls.url]
        pack = cls.parent
        while pack is not None:
            path.append(pack.url)
            pack = pack.parent
        url = ''.join(reversed(path))

        contr_url = ''
        for cont in ControllerCache.get_controllers():
            p = cont.find_pack(cls)
            if p:
                contr_url = cont.url
                break
        return contr_url + url

    def get_absolute_url(self):
        """
        Возвращает абсолютный путь (НОРМАЛЬНО, в отличие от absolute_url)
        """
        assert hasattr(self, 'controller')
        pack = self
        if pack.parent:
            path = []
            while pack.parent:
                path.insert(0, pack.url)
                pack = pack.parent
        else:
            path = [pack.url]
        return '/'.join([pack.controller.url] + map(_clean_url, path))

    def get_permission_code(self):
        # метод оставлен для совместимости
        return self.get_perm_code()

    def get_sub_permission_code(self, sub_code):
        # метод оставлен для совместимости
        return self.get_perm_code(sub_code)

    def has_sub_permission(self, user_obj, sub_code, request):
        # метод оставлен для совместимости
        return self.has_perm(request, sub_code)

    #================= НОВЫЙ ИНТЕРФЕЙС ПРОВЕРКИ ПРАВ ==========================
    def has_perm(self, request, permission):
        """
        Интерфейсный метод проверки подправ пака.

        Использовать ВМЕСТО has_sub_permission
        """
        return _permission_checker.has_pack_permission(
            request, self, permission)

    def get_perm_code(self, permission=None):
        """
        Получение кода (под)права
        """
        # по-умолчанию код генерится backend`ом
        return _permission_checker.get_perm_code(self, permission)
    #==========================================================================

    def pre_run(self, request, context):
        """
        Метод для предварительной обработки
        входящего запроса *request* и контекста *context*
        перед передачений в нижестоящий экшен или пак.
        Если возвращает значение отличное от None, обработка запроса
        прекращается и результат уходит во вьюшку контроллера.
        """
        pass

    def post_run(self, request, context, response):
        '''
        Метод для постобработки результата работы вышестоящего экшена или пака.
        Принимает исходный запрос *request*, результат работы *response* и
        извлеченный контекст *context*.
        '''
        pass

    @classmethod
    def get_verbose_name(cls):
        return (
            cls.title if hasattr(cls, 'title') and cls.title
            else cls.verbose_name if cls.verbose_name else cls.__name__
        )


class ActionController(object):
    '''
    Класс коонтроллер - обеспечивает обработку
    пользовательских запросов путем передачи
    их на исполнение соответствущим Action'ам
    '''

    # Наименование Контроллера для отображения
    verbose_name = None

    class FakePacks:
        """
        Класс содержит заглушки методов, чтобы инспектор кода не ругался,
        т.к. настоящие методы присваиваются классу в рантайме.
        """
        def append(self, item):
            pass

        def extend(self, items_list):
            pass

    def __init__(self, url='', name=None):
        '''
        url - используется для отсечения лишней части пути в запросе, поскольку
              управление в пак передается из вьюшки
        name - человеческое название контроллера. Используется для отладки.
        '''
        # ДЛЯ СОВМЕСТИМОСТИ.
        # Имитирует список паков торчащий наружу
        self.packs = self.FakePacks()
        self.packs.append = self.append_pack
        self.packs.extend = self.extend_packs

        # Используется для отсечения лишней части пути в запросе
        self.url = url
        self.name = name

        # Словарь для быстрого разрешения запросов.
        # Состоит из полного пути запроса, списка
        # вызываемых паков и экшена.
        # Пример: {'/dict/lpu/get_rows': ([DictPack, LPUPack], RowsAction)}
        self._url_patterns = {}

        # Словари для быстрого поиска паков по имени и классу, например:
        # {'DictPack', <DictPack instance at 0x01FBACB0>}
        self._packs_by_name = {}
        self._packs_by_type = {}
        self._actions_by_type = {}
        self._actions_by_name = {}
        # TODO: Тоже самое можно добавить для short_name
        # в экшенах вместо m3.helpers.urls

        self.top_level_packs = []

        # Блокировка для перестроения паттернов урлов
        self._rebuild_lock = threading.RLock()

        # Признак того, что контроллер зарегистрирован во внутреннем кеше
        self._registered = False

    def __str__(self):
        return (
            self.name if self.name
            else super(ActionController, self).__str__()
        )

    #==========================================================================
    # Методы для быстрого поиска экшенов и паков по разным атрибутам
    #==========================================================================
    def _add_action_to_search_dicts(self, action, full_path):
        """ Добавляет экшен в словари для быстрого доступа """
        assert isinstance(action, Action)
        self._actions_by_name[action.__class__.__name__] = (action, full_path)
        self._actions_by_type[action.__class__] = (action, full_path)

    def _add_pack_to_search_dicts(self, pack):
        """ Добавляет экшенпак в словари для быстрого доступа """
        assert isinstance(pack, ActionPack)
        self._packs_by_name[pack.__class__.__name__] = pack
        self._packs_by_type[pack.__class__] = pack

    def _rebuild_search_dicts(self):
        """
        Полностью перестраивает поисковые словари.
        Бывает нужно, если иерархия экшенов непредсказуемо изменяется
        """
        self._actions_by_name.clear()
        self._actions_by_type.clear()
        for full_path, v in self._url_patterns.iteritems():
            _, action = v
            self._add_action_to_search_dicts(action, full_path)
        # Обновлять _packs_by_name и _packs_by_type не нужно!

    #==========================================================================
    # Методы формирующие иерархию экшенов и паков
    #==========================================================================
    def _load_class(self, full_path):
        '''
        По полному пути загружает и созвращает класс
        '''
        # Получаем имя модуля и класса в нём
        dot = full_path.rindex('.')
        mod_name = full_path[:dot]
        pack_name = full_path[dot + 1:]
        # Пробуем загрузить
        mod = import_module(mod_name)
        clazz = getattr(mod, pack_name)
        return clazz

    def _build_pack_node(self, clazz, stack):
        # Что-бы нам не передали, нужно создать экземпляр
        if isinstance(clazz, str):
            clazz = self._load_class(clazz)()
        elif inspect.isclass(clazz):
            clazz = clazz()

        # Отладочный атрибут built нужен,
        # чтобы обнаружить повторное перестроение экшенов
        if hasattr(clazz, '_built'):
            raise ReinitException(clazz=clazz)
        clazz._built = True

        # Присваиваем родителя
        if len(stack) > 0:
            clazz.parent = stack[-1]

        if isinstance(clazz, ActionPack):
            # Для быстрого поиска
            self._add_pack_to_search_dicts(clazz)

            stack.append(clazz)
            # Бежим по экшенам
            for action in clazz.actions:
                self._build_pack_node(action, stack)
            # Бежим по пакам
            for pack in clazz.subpacks:
                self._build_pack_node(pack, stack)
                pack.controller = self
            stack.pop()
        else:
            clazz.controller = self
            full_path = self._build_full_path(stack, clazz)

            # Для быстрого поиска
            self._add_action_to_search_dicts(clazz, full_path)

            self._url_patterns[full_path] = (stack[:], clazz)

    def _invoke(self, request, action, stack):
        '''
        Непосредственный вызов экшена с отработкой всех событий
        '''
        from m3 import ApplicationLogicException

        # проверим что права на выполнение есть
        allowed = _permission_checker.has_action_permission(request, action)

        if not allowed:
            # Стандартное сообщение об отсутствии прав
            msg = u'У вас нет прав на выполнение этого действия!'

            # Если разработчик указал verbose_name у action-а,
            # то добавляем название действия
            if action.verbose_name:
                msg = ' '.join([msg, u'Действие:', action.verbose_name])

            return OperationResult.by_message(msg)

        # Заполняем контект и проверяем его
        rules = action.context_declaration()
        context = self.build_context(request, rules)
        try:
            context.build(request, rules)
        except CriticalContextBuildingError:
            # критическая ошибка сбора контекста - должна валиться
            raise
        except ContextBuildingError as e:
            # некритичную ошибку - показываем пользователю
            return OperationResult.by_message(unicode(e))
        except RequiredFailed as e:
            # если контекст неправильный, то возвращаем
            # фейльный результат операции
            return OperationResult.by_message(
                u'Не удалось выполнить операцию. '
                u'Не задан обязательный<br>параметр: ' + e.reason
            )

        # В request заносим информацию о паках и экшене, которые будут
        # выполнены в процессе обработки запроса
        request.target_packs = stack
        request.target_action = action

        try:
            # Все ПРЕ обработчики
            for pack in stack:
                result = pack.pre_run(request, context)
                if result is not None:
                    return result
            # Сам экшен
            result = action.pre_run(request, context)
            if result is not None:
                return result
            response = action.run(request, context)
            result = action.post_run(request, context, response)
            if result is not None:
                return result
            # Все ПОСТ обработчики с конца
            for pack in reversed(stack):
                result = pack.post_run(request, context, response)
                if result is not None:
                    return result
        except ApplicationLogicException as exc:
            return OperationResult(
                success=False, message=exc.exception_message)

        # по возможности запихиваем текущий контекст в response
        if isinstance(response, BaseContextedResult):
            response.set_context(context)
        return response

    def process_request(self, request):
        """
        Обработка входящего запроса *request* от клиента.
        Обрабатывается по аналогии с UrlResolver'ом Django
        """
        ControllerCache.populate()

        path = request.path
        matched = self._url_patterns.get(path)
        if matched:
            stack, action = matched

            with _STATSD_CLIENT(self, request):
                try:
                    result = self._invoke(request, action, stack)
                except:
                    if settings.DEBUG:
                    # Записывает сообщение в логгер если включен тестовый режим
                        logger.exception(
                            u'ActionController.process_request: '
                            u'перехвачена необработанная ошибка'
                        )
                    raise

            if isinstance(result, ActionResult):
                return result.get_http_response()

            # Если вернули редирект,
            # то нужно повторно обработать запрос, уже с новым экшеном
            elif isinstance(result, ActionRedirectResult):
                new_path = self.get_action_url(result.action)
                if not new_path:
                    raise ActionNotFoundException(result.action)

                request.path = new_path
                result.prepare_request(request)
                return self.process_request(request)

            return result

        raise http.Http404()

    def build_context(self, request, rules):
        '''
        Выполняет построение контекста вызова операции ActionContext
        на основе переданного request
        '''
        if isinstance(rules, dict):
            return DeclarativeActionContext()
        else:
            return ActionContext()

    #==========================================================================
    # Методы, предназначенные для поиска экшенов и паков в контроллере
    #==========================================================================
    def find_pack(self, type):
        """
        Ищет экшенпак класса *type* внутри иерархии котроллера.
        Возвращает его экземпляр или None если не находит.
        *type* может быть классом или строкой с названием класса,
        это позволяет избежать кроссимпортов.
        """
        ControllerCache.populate()

        if isinstance(type, basestring):
            return self._packs_by_name.get(type)
        elif issubclass(type, ActionPack):
            return self._packs_by_type.get(type)
        else:
            raise ValueError('Wrong type of argument %s' % type)

    def find_action(self, type):
        """
        Ищет экшен класса *type* внутри иерархии котроллера.
        Возвращает его экземпляр или None если не находит.
        *type* может быть классом или строкой с названием класса,
        это позволяет избежать кроссимпортов.
        """
        ControllerCache.populate()

        if isinstance(type, basestring):
            clazz, _ = self._actions_by_name.get(type, (None, None))
        elif issubclass(type, Action):
            clazz, _ = self._actions_by_type.get(type, (None, None))
        else:
            raise ValueError('Wrong type of argument %s' % type)

        return clazz

    def get_action_url(self, type):
        """
        Возвращает полный URL адрес для класс или имени класса экшена *action*
        """
        ControllerCache.populate()

        if isinstance(type, str):
            _, full_path = self._actions_by_name.get(type, (None, None))
        elif issubclass(type, Action):
            _, full_path = self._actions_by_type.get(type, (None, None))
        else:
            raise ValueError('Wrong type of argument %s' % type)

        return full_path

    #==========================================================================
    # Методы, предназначенные для добавления/изменения/удаления
    # пакетов действий в контроллер
    #==========================================================================
    def append_pack(self, pack):
        """ Добавляет *pack*, объект типа ActionPack, в контроллер. """
        # нам обязательно нужен экземпляр класса
        # этот метод повторяется кучу раз
        if isinstance(pack, str):
            cleaned_pack = self._load_class(pack)()
        elif inspect.isclass(pack):
            cleaned_pack = pack()
        else:
            cleaned_pack = pack

        self._build_pack_node(cleaned_pack, [])

        if cleaned_pack not in self.top_level_packs:
            self.top_level_packs.append(cleaned_pack)
            cleaned_pack.controller = self
        ControllerCache.register_controller(self)

    def extend_packs(self, packs):
        '''
        Производит массовое добавление экшенпаков в контроллер.
        @param packs: список объектов типа ActionPack,
        которые необходимо зарегистрировать в контроллере
        '''
        for pack in packs:
            self.append_pack(pack)

    def _norm_url(self, url):
        '''
        Очищает части адреса от мусора.
        Раньше были планы использовать регулярные выражения в адресах,
        сейчас остался мусор от них.
        '''
        for char in ['^', '&', '$', '/']:
            if url.startswith(char):
                url = url[1:]
            if url.endswith(char):
                url = url[:-1]
        return '/' + url if url else ''

    def _build_full_path(self, packs_list, final_action):
        '''
        Возвращает полный адрес от контроллера через паки до конечного экшена.
        '''
        if not final_action.url:
            raise ActionUrlIsNotDefined(final_action)
        return self._norm_url(self.url) + ''.join([
            self._norm_url(x.url) for x in packs_list]
        ) + self._norm_url(final_action.url)

    def wrap_pack(self, dest_pack, wrap_pack):
        '''
        Вставляет экшенпак wrap_pack внутрь иерархии перед dest_pack.
        Таким образом можно перехватывать запросы и ответы пака dest_pack.

        Допустим есть цепочка паков:
           A1 - X - A2 - A3    |   A1 - Y - X - A2 - A3
           B1 - B2 - X         |   B1 - B2 - Y - X
           X - C1 - C2         |   Y - X - C1 - C2
        Для решения нужно:
        1. Найти экземпляры пака X
        2. В цепочку вместо X вставить Y->X c учетом левых и правых участников
        3. Перестроить адреса пробежавшись по цепочке

        @param dest_pack: Пак который будем оборачивать
        @param wrap_pack: Оборачивающий пак
        '''
        assert (
            issubclass(dest_pack, ActionPack) and
            issubclass(wrap_pack, ActionPack)
        )

        wrapper = wrap_pack()
        self._add_pack_to_search_dicts(wrapper)
        new_patterns = {}
        current_packs_slice = None
        # списки соседей
        left_packs = []
        right_packs = []

        for url, value in self._url_patterns.iteritems():
            packs_list, final_action = value

            # Поиск пака и соседей в списке
            left_pack = None
            for pos, pack in enumerate(packs_list):
                if pack.__class__ == dest_pack:
                    if pos > 0:
                        left_pack = packs_list[pos - 1]
                    break
            else:
                # Просто копируем
                new_patterns[url] = value
                continue

            # Мутация соседей
            pack.parent = wrapper
            packs_list.insert(pos, wrapper)
            if left_pack:
                wrapper.parent = left_pack
                left_packs.append(left_pack)
            right_packs.append(pack)

            # Создание нового урла
            full_path = self._build_full_path(packs_list, final_action)
            new_patterns[full_path] = (packs_list[:], final_action)
            current_packs_slice = packs_list[:pos + 1]

        self._url_patterns = new_patterns

        # У враппера могут быть собственные экшены и паки.
        # Их тоже нужно построить. Но врапперы также могут быть наследованы
        # от оригинальных паков, поэтому не нужно перестраивать
        # уже существующие экшены и паки, только заменить у них родителя
        if current_packs_slice:
            for subpack in wrapper.subpacks:
                if subpack not in pack.subpacks:
                    self._build_pack_node(subpack, current_packs_slice)

            for action in wrapper.actions:
                if action not in pack.actions:
                    self._build_pack_node(action, current_packs_slice)

            # добавим в левые паки наш врапер,
            # как подчиненный пак без перестройки узлов
            # это нужно для корректной навигации сверху-вниз,
            # а иначе мы никак не узнаем какие паки ниже
            for pack in left_packs:
                if wrapper not in pack.subpacks:
                    pack.subpacks.append(wrapper)
            for pack in right_packs:
                if pack not in wrapper.subpacks:
                    wrapper.subpacks.append(pack)
        else:
            raise ActionPackNotFoundException(dest_pack)

        self._rebuild_search_dicts()

    def wrap_action(self, dest_pack, dest_action, wrap_pack):
        '''
        Вставляет перед экшеном dest_action,
        входящим в пак dest_pack, промежуточный пак wrap_pack.

        ВНИМАНИЕ! Экшены как правило обращаются к своим пакам
        через атрибут "parent", поэтому, вероятно, будут возникать ошибки,
        из-за того, что оборачивающий пак
        не предоставляет методы изначального пака.
        Оборачивающий пак можно наследовать от оригинального,
        но тогда вместо оборачивая целесообразно использовать подмену паков.

        @param dest_pack: Пак в который входит оборачиваемый экшен
        @param dest_action: Оборачиваемый экшен
        @param wrap_pack: Оборачивающий пак
        '''
        assert (
            issubclass(dest_pack, ActionPack) and
            issubclass(wrap_pack, ActionPack) and
            issubclass(dest_action, Action)
        )
        wrapper = wrap_pack()
        self._add_pack_to_search_dicts(wrapper)
        new_patterns = {}
        current_packs_slice = None

        for url, value in self._url_patterns.iteritems():
            packs_list, final_action = value

            # Поиск исходного пака и экшена в нём
            last_pack = packs_list[-1]
            if last_pack.__class__ == dest_pack and (
                    final_action.__class__ == dest_action):
                # Вставка
                packs_list.append(wrapper)
                wrapper.parent = last_pack
                final_action.parent = wrapper

                # Создание нового урла
                full_path = self._build_full_path(packs_list, final_action)
                new_patterns[full_path] = (packs_list[:], final_action)
                current_packs_slice = packs_list

            else:
                # Просто копируем
                new_patterns[url] = value

        self._url_patterns = new_patterns

        if current_packs_slice:
            # У враппера могут быть собственные экшены и паки.
            # Их тоже нужно построить.
            for subpack in wrapper.subpacks:
                self._build_pack_node(subpack, current_packs_slice)
            for action in wrapper.actions:
                self._build_pack_node(action, current_packs_slice)
        else:
            raise ActionPackNotFoundException(dest_pack)

        self._rebuild_search_dicts()

    def dump_urls(self):
        '''
        Отладочный метод.
        Выводит в консоль список всех адрес зарегистрированных в контроллере.
        '''
        print '==== CONTROLLER WITH URL: %s ======' % self.url
        for key in sorted(self._url_patterns.keys()):
            print key
        print
        print 'Total patterns %s' % len(self._url_patterns.keys())

    def get_action_by_url(self, url):
        """
        Получить Action по url
        """
        ControllerCache.populate()

        matched = self._url_patterns.get(url)
        if matched:
            _, action = matched
            return action

    def get_top_actions(self):
        '''
        Получение списка действий или наборов, находящихся на первом уровне
        '''
        top_packs = []
        for stack, act in self._url_patterns.values():
            if len(stack) == 0:
                # значит экшин на верхнем уровне
                if act not in top_packs:
                    top_packs.append(act)
            else:
                if stack[0] not in top_packs:
                    top_packs.append(stack[0])
        return top_packs

    def get_packs(self):
        '''
        Возвращение всех паков в контроллере
        '''
        return self._packs_by_name.values()

    def reset(self):
        '''
        HARD RESET всего что наделал контроллер с паками и экшенами
        '''
        for pack in self.top_level_packs:
            if hasattr(pack, '_built'):
                del(pack._built)
                for action in pack.actions:
                    if hasattr(action, '_built'):
                        del(action._built)
        self._actions_by_name.clear()
        self._actions_by_type.clear()
        self._packs_by_name.clear()
        self._packs_by_type.clear()
        self.top_level_packs = []


class ControllerCache(object):
    '''
    Внутренний класс платформы,
    который отвечает за хранение кеша контроллеров
    и связанных с ним экшенов и паков.
    '''
    _loaded = False
    _write_lock = threading.RLock()

    # словарь зарегистрированных контроллеров в прикладном приложении
    _controllers = set()

    #==========================================================================
    # Методы, предназначенные для поиска экшенов
    # и паков во всех контроллерах системы
    #==========================================================================

    @classmethod
    def get_action_url(cls, type):
        """ Возвращает URL экшена *type* по его имени или классу """
        assert isinstance(type, basestring) or issubclass(type, Action)
        cls.populate()
        for cont in cls._controllers:
            url = cont.get_action_url(type)
            if url:
                return url

    @classmethod
    def find_pack(cls, pack):
        """
        Ищет заданный *pack* по имени класса или классу
        во всех зарегистрированных контроллерах.
        Возвращает экземпляр первого найденного пака.
        """
        for cont in list(cls._controllers):
            p = cont.find_pack(pack)
            if p:
                return p

    @classmethod
    def find_action(cls, action):
        """
        Ищет заданный *action* по имени класса или классу
        во всех зарегистрированных контроллерах.
        Возвращает экземпляр первого найденного экшена.
        """
        for cont in list(cls._controllers):
            p = cont.find_action(action)
            if p:
                return p

    @classmethod
    def get_action_by_url(cls, url):
        """ Возвращает Action по переданному *url* """
        for cont in cls._controllers:
            act = cont.get_action_by_url(url)
            if act:
                return act
        return

    #==========================================================================
    @classmethod
    def _self_test(cls):
        """
        Проверяет корректность регистрации экшнов/паков
        """

        cls.populate()

        result = []

        def warn_if_class(obj, name):
            if inspect.isclass(obj):
                result.append(
                    '%r is not the instance but class!' % _name_of(obj))
                return True
            return False

        def shortname_checker(acc):
            def check(obj, name):
                sn = getattr(obj, 'shortname', None) or getattr(
                        obj, 'shortname', None)
                if sn:
                    name = acc.get(sn)
                    if name:
                        result.append(
                            '%r have shortname, reserved for %r!' % (
                                _name_of(obj), name))
                    else:
                        acc[sn] = _name_of(obj)
            return check

        def existense_checker(acc):
            def check(obj, name):
                if name in acc:
                    result.append(
                        '%r already registered!' % name)
                    return True
                acc.add(name)
                return False
            return check

        check_action_sn = shortname_checker({})
        check_pack_sn = shortname_checker({})
        check_reregister = existense_checker(set())

        def check_packs(packs):
            for pack in packs:
                pack_name = _name_of(pack)
                if not warn_if_class(pack, pack_name):
                    check_pack_sn(pack, pack_name)
                    if pack.subpacks:
                        result.append(
                            '%r have subpacks - code smell!' % pack_name)
                        check_packs(pack.subpacks)

                for action in pack.actions:
                    action_name = _name_of(action)
                    if not warn_if_class(action, action_name):
                        if not check_reregister(action, action_name):
                            if check_action_sn(action, action_name):
                                continue

        for cont in cls._controllers:
            check_packs(cont.top_level_packs)

        return result


    @classmethod
    def register_controller(cls, controller):
        '''
        Выполняет регистрацию контроллера *controller* во внутреннем кеше.
        '''
        assert isinstance(controller, ActionController)
        cls._controllers.add(controller)

    @classmethod
    def populate(cls):
        """
        Загружает в кэш ActionController'ы
        из перечисленных в INSTALLED_APPS приложений.
        В каждом из них загружает модуль *app_meta*
        и пытается выполнить метод *register_actinos* внутри него.
        Выполняется только один раз. Возвращает истину в случае успеха.
        """
        if cls._loaded:
            return False
        cls._write_lock.acquire()
        try:
            if cls._loaded:
                return False
            # Из инитов всех приложения пытаемся выполнить register_ui_actions
            for app_name in settings.INSTALLED_APPS:
                try:
                    module = import_module('.app_meta', app_name)
                except ImportError, err:
                    if err.args[0].find('No module named') == -1:
                        raise
                    continue
                proc = getattr(module, 'register_actions', None)
                if callable(proc):
                    proc()
            cls._loaded = True
        finally:
            cls._write_lock.release()
        return True

    @classmethod
    def dump_urls(cls):
        '''
        Отладочный метод.
        Выводит в консоль адреса всех контроллеров зарегистрированных в кэше.
        '''
        print '------------ CONTROLLER CACHE DUMP ------------'
        for cont in cls._controllers:
            cont.dump_urls()

    @classmethod
    def require_update(cls):
        """
        Сбрасывает внутренний флаг заполненности контроллера.
        Следующий запрос к контроллеру вызовет
        перестройку иерархии экшенов и паков.
        """
        for cont in cls.get_controllers():
            cont.reset()
        cls._loaded = False

    @classmethod
    def get_controllers(cls):
        """
        Возвращает множество всех контроллеров зарегистрированных в кэше
        """
        return cls._controllers
