#coding:utf-8
'''
Created on 11.06.2010

@author: akvarats
'''
from django.db.models.query import QuerySet
import inspect
from copy import copy

from django.db import transaction
from django.contrib.auth.models import User
import json
from django.utils import simplejson
from m3.helpers.icons import Icons

from m3.ui import actions
from m3.ui.actions.dicts.tree import BaseTreeDictionaryActions as Dicts_BaseTreeDictionaryActions
from m3.ui.actions.tree_packs import BaseTreeDictionaryActions as Packs_BaseTreeDictionaryActions
from m3.ui.actions.packs import BaseDictionaryModelActions
from m3.ui.actions.packs import BaseDictionaryActions as Dicts_BaseDictionaryActions
from m3.ui.actions.dicts.simple import BaseDictionaryActions as Packs_BaseDictionaryActions
from m3.ui.actions.results import JsonResult
from m3.ui.ext import windows
from m3.ui.ext import panels
from m3.ui.ext import fields
from m3.ui.ext import controls
from m3.ui.ext.containers.grids import ExtGridColumn
from m3.ui.ext.panels.grids import ExtObjectGrid
from m3.helpers import ui as ui_helpers
from m3.db import safe_delete, queryset_limiter
from m3.helpers import logger, urls
from m3.ui.actions import ActionContextDeclaration, ControllerCache, ActionPack, Action
from m3.ui.actions.context import ActionContext
from m3.ui.ext.containers import ExtTree, ExtTreeNode
from m3_audit.manager import AuditManager
from m3_audit.models import RolesAuditModel
from m3_users.ui import PermissionEditWindow
from users import SelectUsersListWindow
from m3.ui.ext.fields.complex import ExtSearchField

from m3_users.metaroles import get_metarole

import helpers
import models
import metaroles
import app_meta
import api

PERM_OBJECT_NOT_FOUND = u'** объект права не найден **'


class RolesActions(actions.ActionPack):
    '''
    Пакет действий для подсистемы прав пользователей
    '''

    url = '/roles'

    need_check_permission = True

    verbose_name = u'Роли пользователей'

    def __init__(self):
        super(RolesActions, self).__init__()
        self.actions = [
            RolesWindowAction(),
            EditRoleWindowAction(),
            SaveRoleAction(),
            DeleteRoleAction(),


            ShowAssignedUsersAction(), # показ окна со списком пользователей, ассоциированных с ролью
            RoleAssignedUsersDataAction(), # получение списка пользователей, ассоциированных с ролью
            SelectUsersToAssignWindowAction(), # получение окна со списком пользователей, которые можно добавить в роль
            UsersForRoleAssignmentData(), # получение списка пользователей, которых можно включить в заданную роль
            RolesDataAction(),
            AssignUsers(), # действие на добавление пользователей в роль
            DeleteAssignedUser(), # удаление связанного с ролью пользователя
            GetRolePermissionAction(), # получение списка прав доступа роли
            AddRolePermission(), # выбор прав доступа для добавления в роль
            #GetAllPermissions(), # получение дерева всех прав доступа

            EditPermissionWindowAction(),
            SaveRolePermissionAction(),
            DelAllRolePermissionAction(),
        ]

#===============================================================================
# UI actions
#  - RolesWindowAction -- получение окна со списком ролей
#  - EditRoleWindowAction -- получение окна редактирования роли
#===============================================================================

class RolesWindowAction(actions.Action):
    '''
    Действие на получение окна показа списка пользовательских ролей
    '''
    url = '/roles-window'

    verbose_name = 'Окно роли'

    need_check_permission = True

    def run(self, request, context):
        return actions.ExtUIScriptResult(data=RolesListWindow())

class EditRoleWindowAction(actions.Action):
    '''
    Получение окна редактирования роли пользователя
    '''
    url = '/edit-role-window'
    need_check_permission = True
    verbose_name = u'Добавление и редактирование роли'
    def context_declaration(self):
        return [
            ActionContextDeclaration(name=u'userrole_id', type=int, required=True, default=0)
        ]

    def run(self, request, context):

        new_role = True
        if(context.userrole_id > 0):
            new_role = False
            try:
                user_role = models.UserRole.objects.get(pk=context.userrole_id)
            except models.UserRole.DoesNotExist:
                return actions.OperationResult(success=False, message=u'Роль с указанным идентификатором не найдена')
        else:
            user_role = models.UserRole()

        window = RolesEditWindow(new_role)
        window.form.from_object(user_role)

        return actions.ExtUIScriptResult(data=window)

class ShowAssignedUsersAction(actions.Action):
    '''
    Получение окна со списком связанных пользователей
    '''
    url = '/role-assigned-users-window'

    def context_declaration(self):
        return [
            actions.ActionContextDeclaration(name='userrole_id', type=int, required=True)
        ]

    def run(self, request, context):
        window = AssignedUsersWindow()
        role = models.UserRole.objects.get(id=context.userrole_id)
        window.field_role_name.value = role.name

        return actions.ExtUIScriptResult(window)

class SelectUsersToAssignWindowAction(actions.Action):
    '''
    Показ окна с выбором сотрудников, которые не были выбраны ранее для указанной роли
    '''
    url = '/role-assigned-users-append-window'
    need_check_permission = True
    verbose_name = u'Добавление пользователя роли'

    def context_declaration(self):
        return [
            actions.ActionContextDeclaration(name='userrole_id', type=int, required=True)
        ]

    def run(self, request, context):
        role = models.UserRole.objects.get(id=context.userrole_id)
        window = SelectUsersListWindow()
        window.grid.action_data = UsersForRoleAssignmentData
        window.grid.title = u"Выберите пользователей для роли '%s'" % role.name
        window.action_submit = AssignUsers

        return actions.ExtUIScriptResult(window)

class AddRolePermission(actions.Action):
    '''
    Выбор прав доступа для добавления в роль
    '''
    url = '/role-add-permission-window'
    need_check_permission = True
    verbose_name = u'Добавление прав'
#    def context_declaration(self):
#        return [
#            actions.ActionContextDeclaration(name='userrole_id', type=int, required=True)
#        ]
#        
    def run(self, request, context):
        #role = models.UserRole.objects.get(id=context.userrole_id)
        window = SelectPermissionWindow()
        #window.title = u"Выберите права доступа для роли '%s'" % role.name
        return actions.ExtUIScriptResult(window)

#===============================================================================
# DATA actions
#===============================================================================

class RolesDataAction(actions.Action):

    url = '/roles-data'

    def context_declaration(self):
        return [
            actions.ActionContextDeclaration(name='filter', type=unicode, required=True, default=''),
            actions.ActionContextDeclaration(name='start', type=int, required=True, default=0),
            actions.ActionContextDeclaration(name='limit', type=int, required=True, default=25),
        ]

    def run(self, request, context):
        return actions.JsonResult(ui_helpers.paginated_json_data(helpers.get_roles_query(context.filter), context.start, context.limit))

class RoleAssignedUsersDataAction(actions.Action):
    '''
    Получение данных (списка) пользователей, которые прикреплены к указанной роли
    '''
    url = '/role-users'

    def context_declaration(self):
        return [
            actions.ActionContextDeclaration(name='userrole_id', type=int, required=True),
            actions.ActionContextDeclaration(name='filter', type=str, requeired=False),
            actions.ActionContextDeclaration(name='start', type=int, required=True),
            actions.ActionContextDeclaration(name='limit', type=int, required=True)
        ]

    def run(self, request, context):
        filter = getattr(context, 'filter', None)
        return actions.ExtGridDataQueryResult(helpers.get_assigned_users_query(context.userrole_id, filter), context.start, context.limit)

class UsersForRoleAssignmentData(actions.Action):
    '''
    Получение списка пользователей, которые могут быть назначены на роль
    '''

    url = '/role-assign-users-unassigned'

    def context_declaration(self):
        return [
            actions.ActionContextDeclaration(name='userrole_id', type=int, required=True),
            actions.ActionContextDeclaration(name='filter', type=str, required=True, default=u''),
            actions.ActionContextDeclaration(name='start', type=int, required=True),
            actions.ActionContextDeclaration(name='limit', type=int, required=True)
        ]

    def run(self, request, context):
        users = helpers.get_unassigned_users(context.userrole_id, context.filter)
        rows, total = queryset_limiter(users, context.start, context.limit)
        return actions.PreJsonResult({'rows': rows, 'total': total})
        #return actions.ExtGridDataQueryResult(helpers.get_unassigned_users(context.userrole_id, context.filter))

def get_perms_text(user_role, action=None, pack=None):
    '''достает права на выполнение, редактирование и тд - повторяет действия из экшна EditPermissionWindowAction
    вполне уместно тк сохранение происходит по тому же принципу....возможно не работает для objectPack-ов'''
    perm_codes = []
    act_perms = []
    act_url = ''
    act_urls = []
    sub_permissions = None
    if action:
        sub_permissions=getattr(action, 'sub_permissions', {})
        act_url = action.absolute_url()
        act_urls = [[act_url, '']]
    elif pack:
        if isinstance(pack, Dicts_BaseDictionaryActions) or isinstance(pack, Packs_BaseDictionaryActions) or\
           isinstance(pack, Dicts_BaseTreeDictionaryActions) or isinstance(pack, Packs_BaseTreeDictionaryActions):
            sub_permissions=getattr(pack, 'sub_permissions', {})
            act_url = pack.absolute_url()
            act_urls = [[act_url, pack.list_window_action.url.rstrip('$')]]


    if act_url:
    # создадим словарь кодов прав в том виде, в котором они должны храниться в таблице
        for a_url in act_urls:
            perms_list = ['on_desktop', 'enabled'] + sub_permissions.keys()
            for ps in perms_list:
                if ps == 'on_desktop':
                    url = a_url[0] + a_url[1]
                else:
                    url = a_url[0]
                if ps == 'enabled':
                    perm_codes.append(unicode(url))
                else:
                    perm_codes.append(unicode(url) + u'#' + unicode(ps))

        role_perms = list(models.RolePermission.objects.filter(role=user_role, permission_code__in=perm_codes))
        for rp in role_perms:
            pc_list = rp.permission_code.split(u'#')
            if len(pc_list) > 1:
                if pc_list[-1]=='on_desktop':
                    act_perms.append(u'Отображение')
                if pc_list[-1]=='edit':
                    act_perms.append(u'Редактирование')
            else:
                act_perms.append(u'Выполнение')
    if act_perms:
        act_perms.sort()
        return  ','.join(act_perms)
    else:
        return u''


class GetRolePermissionAction(actions.Action):
    """
    Получение списка прав доступа для указанной роли
    """
    url = '/role-permission-rows'

    ACTION = 'action'
    PACK = 'pack'
    CONTROLLER = 'controller'

    def context_declaration(self):
        return [
            actions.ActionContextDeclaration(name='userrole_id', type=int, required=True),
            actions.ActionContextDeclaration(name='metarole', type=str, required=False, default=None)
        ]

    def run(self, request, context):

        metarole = getattr(context, 'metarole', None)
        if not metarole:
            return JsonResult({})

        user_role = models.UserRole.objects.get(id=context.userrole_id) if context.userrole_id else None

        res = []
        for controller in ControllerCache.get_controllers():

            if hasattr(controller, 'metaroles') and metarole in map(lambda x: x.code, controller.metaroles) or \
               (controller.url == '/m3-users' and metarole== metaroles.ADMIN):
                contr_dict = dict(name=controller.verbose_name or controller.name or controller.__class__.__name__,
                    expanded=True,
                    children=[],
                    class_name=controller.__class__.__name__,
                    iconCls=Icons.APPLICATION_VIEW_LIST,
                    type=self.CONTROLLER)

                for pack in controller.get_packs():
                    if pack.need_check_permission:
                        #сбор прав
                        pack_perms = get_perms_text(user_role, pack=pack)

                        pack_dict = dict(name=pack.verbose_name or pack.__class__.__name__,
                            expanded=True,
                            children=[],
                            perm = pack_perms,
                            class_name=pack.__class__.__name__,
                            type=self.PACK,
                            iconCls=Icons.PACKAGE,
                            sub_permissions=getattr(pack, 'sub_permissions', {}))

                        contr_dict.setdefault('children', []).append(pack_dict)

                        for action in pack.actions:
                            if action.need_check_permission:
                                #сбор прав
                                act_perms = get_perms_text(user_role, action=action)
                                action_dict = dict(name=action.verbose_name or action.__class__.__name__,
                                    expanded=False,
                                    leaf=True,
                                    perm = act_perms,
                                    class_name=action.__class__.__name__,
                                    type=self.ACTION,
                                    iconCls=Icons.COG,
                                    sub_permissions=getattr(action, 'sub_permissions', {}))

                                pack_dict.setdefault('children', []).append(action_dict)

                        pack_dict['leaf'] = len(pack_dict['children']) == 0

                contr_dict['leaf'] = len(contr_dict['children']) == 0

                res.append(contr_dict)

        return JsonResult(json.dumps(res))

def get_all_permission_tree():
    """
    Общий подход к формированию дерева прав доступа (алгоритм):
    собирается список прав доступа исходя из наборов действий, действий, субправ наборов действий, субправ действий
    у каждого элемента списка прав должен быть путь в дереве (пока строкой), наименование права доступа, полное наименование права (для грида прав)
    путь в дереве строится из значения path элемента, а если он отсутствует, то по иерархии этого элемента в фактической структуре действий и набора действий 
    """
    class PermProxy(ExtTreeNode):
        def __init__(self, id, parent=None, name='', url='', can_select=True, fullname=None, path = ''):
            super(PermProxy, self).__init__()
            self.parent = parent
            if parent:
                parent.add_children(self)
            self.name = name
            self.path = path
            self.expanded = True
            self.items['name'] = name
            self.items['url'] = url
            self.items['fullname'] = fullname if fullname else name
            self.can_check = can_select

    def find_node(node_name, parent_node, res):
        for item in res:
            if item.parent == parent_node and item.name.upper() == node_name.upper():
                return item
        return None

    def add_path(path, res):
        '''
        Добавление пути набора действий в дерево
        '''
        parent_node = None
        if path:
            items = path.strip().split("\\") #.replace("/", "\\")
            for name in items:
                node = find_node(name, parent_node, res)
                if not node:
                    node = PermProxy(len(res) + 1, parent_node, name, '', False)
                    res.append(node)
                parent_node = node
        return parent_node
    
    def get_action_sub_perm_path(action, sub_perm_code):
        result = ''
        if action:
            if sub_perm_code in action.sub_permissions.keys():
                path = action.sub_permissions[sub_perm_code]
                items = path.strip().split("\\") #.replace("/", "\\")
                # если длина пути больше 1, значит указали путь - выделим путь и имя
                if len(items) > 1:
                    name = items[-1]
                    items.remove(name)
                    result = '\\'.join(items)
                else:
                    # если нет пути, то построим путь по экшену
                    result = get_action_perm_path(action)
                    result = result + ('\\' if result != '' else '') + action.get_verbose_name()
        return result
    
    def get_action_perm_path(action):
        result = ''
        if action:
            # если указан путь, то строится по этому пути, иначе по иерархии паков
            if action.path:
                result = action.path
            else:
                result = get_actionpack_perm_path(action.parent)
                result = result + ('\\' if result != '' else '') + action.parent.get_verbose_name()
        return result
    
    def get_actionpack_sub_perm_path(actionpack, sub_perm_code):
        result = ''
        if actionpack:
            if sub_perm_code in actionpack.sub_permissions.keys():
                path = actionpack.sub_permissions[sub_perm_code]
                items = path.strip().split("\\") #.replace("/", "\\")
                # если длина пути больше 1, значит указали путь - выделим путь и имя
                if len(items) > 1:
                    name = items[-1]
                    items.remove(name)
                    result = '\\'.join(items)
                else:
                    # если нет пути, то построим путь по набору экшенов
                    result = get_actionpack_perm_path(actionpack)
                    result = result + ('\\' if result != '' else '') + actionpack.get_verbose_name()
        return result
    
    def get_actionpack_perm_path(actionpack):
        result = ''
        if actionpack:
            # если указан путь, то строится по этому пути, иначе по иерархии паков
            if actionpack.path:
                result = actionpack.path
            else:
                if actionpack.parent:
                    result = get_actionpack_perm_path(actionpack.parent)
                    result = result + ('\\' if result != '' else '') + actionpack.parent.get_verbose_name()
        return result
    
    def add_nodes(parent_node, action_set, res, ctrl):
        # если передали Набор действий, то у него надо взять Действия и подчиненные Наборы
        if isinstance(action_set, ActionPack):
            # найдем и создадим путь, по которому набор будет отображаться в дереве
            #path = action_set.path if hasattr(action_set, 'path') and action_set.path else ctrl.verbose_name if ctrl.verbose_name else ctrl.__class__.__name__
            #start_count = len(res)
            #parent_node = add_path(path, res)
            # получим отображаемое имя набора 
            #name = action_set.get_verbose_name()
            #item = PermProxy(len(res) + 1, parent_node, name, action_set.absolute_url(), False)
            #res.append(item)
            #count = len(res)
            # обработаем действия
            if action_set.need_check_permission:
                for act in action_set.actions:
                    # добавляем если надо проверять права или есть подчиненные права
                    add_nodes(None, act, res, ctrl)
            # обработаем подчиненные права
            # добавляем если надо проверять права или есть подчиненные права
            if action_set.need_check_permission and action_set.sub_permissions:
                pack_name = action_set.get_verbose_name()
                for key, value in action_set.sub_permissions.items():
                    fullname = '%s - %s' % (pack_name, value)
                    path = get_actionpack_sub_perm_path(action_set, key)
                    url = action_set.get_sub_permission_code(key)
                    if not url in res_urls.keys():
                        child4 = PermProxy(len(res) + 1, None, value, url, True, fullname, path)
                        res.append(child4)
                        res_urls[url] = child4
            # обработаем подчиненные Наборы
            for pack in action_set.subpacks:
                add_nodes(None, pack, res, ctrl)
            # удалим созданные элементы, если небыло дочерних
            #if len(res) - count == 0:
                #res.remove(item)
            #    while len(res) > start_count:
            #        item = res.pop()
            #        if item.parent:
            #            item.parent.children.remove(item)
        # если передали Действие
        elif isinstance(action_set, Action):
            if action_set.need_check_permission or action_set.sub_permissions:
                if inspect.isclass(action_set):
                    action_set = action_set()
                if action_set.parent:
                    pack = action_set.parent
                    pack_name = pack.get_verbose_name()
                else:
                    pack_name = ''
                #name = action_set.verbose_name if action_set.verbose_name else action_set.__class__.__name__
                name = action_set.get_verbose_name()
                fullname = '%s - %s' % (pack_name, name)
                if action_set.need_check_permission:
                    path = get_action_perm_path(action_set)
                    url = action_set.absolute_url()
                    if not url in res_urls.keys():
                        item = PermProxy(len(res) + 1, None, name, url, True, fullname, path)
                        res.append(item)
                        res_urls[url] = item
                # у действия берем подчиненные права
                for key, value in action_set.sub_permissions.items():
                    items = value.strip().split("\\")
                    # если длина пути больше 1, значит указали путь - выделим путь и имя
                    if len(items) > 1:
                        name = items[-1]
                        pack_name = items[-2] 
                    else:
                        name = value
                    fullname = '%s - %s' % (pack_name, name)
                    path = get_action_sub_perm_path(action_set, key)
                    url = action_set.get_sub_permission_code(key)
                    if not url in res_urls.keys():
                        child3 = PermProxy(len(res) + 1, None, name, url, True, fullname, path)
                        res.append(child3)
                        res_urls[url] = item
    res = []
    res_urls = {}
    # пройдемся по контроллерам
    for ctrl in ControllerCache.get_controllers():
        # пройдемся по верхним наборам действий
        for pack in ctrl.get_top_actions():
            add_nodes(None, pack, res, ctrl)
    
    # выстроим иерархию
    for item in res:
        if not item.parent:
            parent_node = add_path(item.path, res)
            if parent_node:
                parent_node.add_children(item)
                item.parent = parent_node
    # преобразуем список в дерево (оставим только корневые элементы)
    nodes = []
    for item in res:
        if not item.parent:
            nodes.append(item)
    return nodes

#===============================================================================
# OPERATIONS
#===============================================================================
class SaveRolePermissionAction(actions.Action):
    '''
    Сохранение роли пользователя
    '''

    url = '/save-permission-role'

    def context_declaration(self):
        return [
            actions.ACD(name=u'type', type=str, required=True),
            actions.ACD(name=u'class_name', type=str, required=True),
            actions.ACD(name=u'userrole_id', type=int, required=True, default=0),
            actions.ACD(name=u'perms', type=object, required=True, default=[]),
        ]

    def run(self, request, context):

        act_urls = []
        perm_codes = {}
        is_dict_pack = False

        try:
            # создадим список адресов экшенов
            if context.type == GetRolePermissionAction.ACTION:
                act_url = ControllerCache.find_action(str(context.class_name)).absolute_url()
                act_urls = [[act_url, '']]
            elif context.type == GetRolePermissionAction.PACK:
                pack = ControllerCache.find_pack(str(context.class_name))
                # Для справочников берем только экшен окна.
                # В системе два класса справочников - смотрим на оба
                if isinstance(pack, Dicts_BaseDictionaryActions) or isinstance(pack, Packs_BaseDictionaryActions) or\
                        isinstance(pack, Dicts_BaseTreeDictionaryActions) or isinstance(pack, Packs_BaseTreeDictionaryActions):
                    acts = [pack.list_window_action]
                    is_dict_pack = True
                else:
                    acts = pack.actions
                act_url = pack.absolute_url()
                for act in acts:
                    if pack.need_check_permission or act.need_check_permission or is_dict_pack:
                        a_url = act_url
                        if not is_dict_pack:
                            a_url += act.url.rstrip('$')
                        act_urls.append([a_url, act.url.rstrip('$')])

            # создадим словарь кодов прав в том виде, в котором они должны храниться в таблице
            for a_url in act_urls:
                for ps in context.perms.items():
                    if ps[0] == 'on_desktop' and is_dict_pack:
                        url = a_url[0] + a_url[1]
                    else:
                        url = a_url[0]
                    if ps[0] == 'enabled':
                        perm_codes.update({unicode(url): ps[1]})
                    else:
                        perm_codes.update({unicode(url) + u'#' + unicode(ps[0]): ps[1]})

            # возьмем записи всех прав для роли
            role_perms = models.RolePermission.objects.filter(role=context.userrole_id, permission_code__in=perm_codes.keys())

            # Лишние записи прав удалим
            for rp in role_perms:
                if rp.permission_code not in perm_codes:
                    rp.delete()

            # создадим записи о правах, если права есть, иначе удалим записи
            for np in perm_codes:
                perm_query = role_perms.filter(permission_code=np)

                assert perm_query.count() < 2, u'Код права на action должен быть уникальным в таблице'

                if perm_query and not perm_codes[np]:
                    rp = perm_query.get()
                    rp.delete()
                elif not perm_query and perm_codes[np]:
                    rp = models.RolePermission(role_id=context.userrole_id, permission_code=np)
                    rp.save()

        except:
            logger.exception(u'Не удалось сохранить права роли пользователя')
            return actions.OperationResult(success=False, message=u'Не удалось сохранить права роли пользователя.')

        return actions.OperationResult(success=True)

class DelAllRolePermissionAction(actions.Action):
    """
    Удаление всех прав для роли
    """
    url = '/del-all-permission-url'
    need_check_permission = True
    verbose_name = u'Удаление всех прав для роли'

    def context_declaration(self):
        return [
            actions.ACD(name='userrole_id', type=int, required=True, default=0),
            ]

    def run(self, request, context):
        # возьмем записи всех прав для роли
        role_perms = models.RolePermission.objects.filter(role=context.userrole_id)
        role_perms.all().delete()
        return actions.OperationResult(success=True)


class SaveRoleAction(actions.Action):
    '''
    Сохранение роли пользователя
    '''

    url = '/save-role'

    def context_declaration(self):
        return [
            ActionContextDeclaration(name=u'userrole_id', type=int, required=True, default=0),
            ActionContextDeclaration(name=u'perms', type=object, required=True, default=[])
        ]

    def run(self, request, context):
        try:
            if context.userrole_id > 0:
                try:
                    user_role = models.UserRole.objects.get(id=context.userrole_id)
                except models.UserRole.DoesNotExist:
                    return actions.OperationResult(success=False, message=u'Роль с указанным идентификатором не найдена')
            else:
                user_role = models.UserRole()


            context.user_role = user_role

            window = RolesEditWindow()
            window.form.bind_to_request(request)
            window.form.to_object(user_role)

            user_role.save()

#            # сохраним также права доступа
#            ids = []
#            for perm in context.perms:
#                code = perm['permission_code']
#                q = models.RolePermission.objects.filter(role=user_role, permission_code=code).all()
#                if len(q) > 0:
#                    perm_obj = q[0]
#                else:
#                    perm_obj = models.RolePermission(role=user_role, permission_code=perm['permission_code'])
#                perm_obj.disabled = perm['disabled']
#                # self._handle_record_auditing(request, context, perm_obj, user_role) # аудит до сохранения,- TODO?
#                perm_obj.save()
#
#                ids.append(perm_obj.id)
#
#            # удалим те, которые не обновились
#            models.RolePermission.objects.filter(role=user_role).exclude(id__in=ids).delete()

        except:
            logger.exception(u'Не удалось сохранить роль пользователя')
            return actions.OperationResult(success=False, message=u'Не удалось сохранить роль пользователя.')

        return actions.OperationResult(success=True)  
    
    def _get_role(self, request, context):
        if(context.userrole_id > 0):
            try:
                user_role = models.UserRole.objects.get(id=context.userrole_id)
            except models.UserRole.DoesNotExist:
                return actions.OperationResult(success=False, message=u'Роль с указанным идентификатором не найдена')
        else:
            user_role = models.UserRole()
        # только два скоупа в питоне ))
        return user_role
    
    def _get_existing_permissions(self, request=None, context=None):
        return models.RolePermission.objects.filter(role=context.user_role)
    
    # Есть копипаста
    def _get_supplied_permissions(self, request, context):
        result = []
        for perm in context.perms:
            code = perm['permission_code']
            q = models.RolePermission.objects.filter(role=context.user_role, permission_code=code).all()
            if len(q) > 0:
                perm_obj = q[0]
            else:
                perm_obj = models.RolePermission(role=context.user_role, permission_code=perm['permission_code'])
            perm_obj.disabled = perm['disabled']                
            
            result.append(perm_obj)
        return result
        
    def _added_permissions(self, existing, supplied):
        result = list(supplied)
        for e in existing:
            for s in supplied:
                if e.id == s.id:
                    result.remove(s)
        return result
                                            
    def _deleted_permissions(self, existing, supplied):
        result = list(existing)
        for e in existing:
            for s in supplied:
                if e.id == s.id:
                    result.remove(e)
        return result
        
        

class DeleteRoleAction(actions.Action):

    url = '/delete-role'
    need_check_permission = True
    verbose_name = u'Удаление роли'
    def context_declaration(self):
        return [
            ActionContextDeclaration(name=u'userrole_id', type=int, required=True)
        ]

    def run(self, request, context):
        try:
            user_role = models.UserRole.objects.get(id=context.userrole_id)
        except models.UserRole.DoesNotExist:
            return actions.OperationResult(success=False, message=u'Роль с указанным идентификатором не найдена')

        if len(helpers.get_assigned_users_query(user_role)) > 0:
            return actions.OperationResult(success=False, message=u'К данной роли привязаны пользователи. Удалять такую роль нельзя')

        user_role.delete()
#        try:
#            if not safe_delete(user_role):
#                # FIXME: return в try - это зло
#                return actions.OperationResult(success=False, message=u'Не удалось удалить роль пользователя.<br>На эту запись есть ссылки в базе данных.')
#        except:
#            logger.exception(u'Не удалось удалить роль пользователя')
#            return actions.OperationResult(success=False, message=u'Не удалось удалить роль пользователя.<br>Подробности в логах системы.')

        return actions.OperationResult(success=True)

class AssignUsers(actions.Action):
    '''
    Сопоставление пользователей роли
    '''
    url = '/assign-users-to-role'

    def context_declaration(self):
        return [
            actions.ActionContextDeclaration(name='userrole_id', type=int, required=True),
            actions.ActionContextDeclaration(name='ids', type=str, required=True),
        ]


    def run(self, request, context):
        # получаем список пользователей, которые уже были ассоциированы с ролью

        try:

            user_ids = context.ids.strip().split(' ')
            for strid in user_ids:
                if not strid:
                    continue
                try:
                    user_id = int(strid)
                    api.set_user_role(user_id, context.userrole_id)
                except ValueError:
                    logger.warning(u'Не верный user id %s' % strid)
                    continue
                    
        except:
            logger.exception(u'Не удалось добавить список пользователей в роль')

            return actions.OperationResult(success=False, message=u'Не удалось добавить пользователей в роль')
        return actions.OperationResult(success=True,)

class DeleteAssignedUser(actions.Action):
    """
    Удаление связанного с ролью пользователя
    """

    url = '/delete-assigned-user'
    need_check_permission = True
    verbose_name = u'Удаление пользователя роли'
    def context_declaration(self):
        return [
            actions.ACD(name='assigneduser_id', type=ActionContext.ValuesList(), required=True)
        ]

    def run(self, request, context):
        for assigneduser_id in context.assigneduser_id:
            try:
                assigned_user = models.AssignedRole.objects.get(id=assigneduser_id)
            except models.AssignedRole.DoesNotExist:
                return actions.OperationResult(success=False, message=u'Не удалось удалить запись. Указанный пользователь не найден.')


            try:
                api.remove_user_role(assigned_user.user, assigned_user.role)
            except Exception:
                logger.exception()
                return actions.OperationResult.by_message(u'Не удалось удалить запись. Подробности в логах системы.')


        return actions.OperationResult()

class EditPermissionWindowAction(actions.Action):
    """
    """
    url = '/edit-permission-url'
    need_check_permission = True
    verbose_name = u'Окно редактирования роли'

    def context_declaration(self):
        return [
            actions.ACD(name='type', type=str, required=True),
            actions.ACD(name='class_name', type=str, required=True),
            actions.ACD(name='name', type=str, required=True),
            actions.ACD(name='userrole_id', type=int, required=True, default=0),
            actions.ACD(name='userrole_name', type=unicode, required=True, default=u''),
            actions.ACD(name='userrole_metarole', type=unicode, required=True, default=u''),
        ]

    def run(self, request, context):

        # Если роль еще не сохранена, то сохраним её
        try:
            if context.userrole_id:
                user_role = models.UserRole.objects.get(id=context.userrole_id)
            else:
                if context.userrole_name:
                    user_role = models.UserRole(name=context.userrole_name, metarole=context.userrole_metarole)
                    user_role.save()
                    context.userrole_id = user_role.id
                else:
                    logger.exception(u'Перед назначением прав задайте наименование роли')
                    return actions.OperationResult(success=False, message=u'Перед назначением прав задайте наименование роли')
        except:
            logger.exception(u'Не удалось сохранить роль пользователя')
            return actions.OperationResult(success=False, message=u'Не удалось сохранить роль пользователя.')

        act_url = ''
        act_urls = []
        perm_codes = []
        perm_obj = dict()
        permissions = None
        is_dict_pack = False

        # Возьмем список дополнительных прав и адрес экшена
        if context.type == GetRolePermissionAction.ACTION:
            permissions = getattr(ControllerCache.find_action(str(context.class_name)), 'sub_permissions', None)
            act_url = ControllerCache.find_action(str(context.class_name)).absolute_url()
            act_urls = [[act_url, '']]
        elif context.type == GetRolePermissionAction.PACK:
            permissions = getattr(ControllerCache.find_pack(str(context.class_name)), 'sub_permissions', None)
            pack = ControllerCache.find_pack(str(context.class_name))
            # Для справочников берем только экшен окна.
            # В системе два класса справочников - смотрим на оба
            if isinstance(pack, Dicts_BaseDictionaryActions) or isinstance(pack, Packs_BaseDictionaryActions) or\
                   isinstance(pack, Dicts_BaseTreeDictionaryActions) or isinstance(pack, Packs_BaseTreeDictionaryActions):
                acts = [pack.list_window_action]
                is_dict_pack = True
                act_url = pack.absolute_url()
                for act in acts:
                    if pack.need_check_permission and act.need_check_permission or is_dict_pack:
                        a_url = act_url
                        if not is_dict_pack:
                            a_url += act.url.rstrip('$')
                        act_urls.append([a_url, act.url.rstrip('$')])

        win = PermissionEditWindow(permissions=permissions)
        win.form.url = SaveRolePermissionAction.absolute_url()

        # Заполним форму только для экшена, т.к. пак объединяет в себе несколько экшенов с, возможно, разным набором разрешений
        # Справочники - исключение, там берем только один экшен
        if act_url:
            # создадим словарь кодов прав в том виде, в котором они должны храниться в таблице
            for a_url in act_urls:
                for ps in ([win.chk_enabled.name, win.chk_on_desktop.name] + permissions.keys()):
                    if ps == 'on_desktop' and is_dict_pack:
                        url = a_url[0] + a_url[1]
                    else:
                        url = a_url[0]
                    if ps == 'enabled':
                        perm_codes.append(unicode(url))
                    else:
                        perm_codes.append(unicode(url) + u'#' + unicode(ps))

            role_perms = models.RolePermission.objects.filter(role=user_role, permission_code__in=perm_codes)
            for rp in role_perms:
                pc_list = rp.permission_code.split(u'#')
                if len(pc_list) > 1:
                    sub_perm = pc_list[-1]
                else:
                    sub_perm = u'enabled'
                perm_obj[sub_perm] = True

            win.form.from_object(perm_obj)

        return actions.ExtUIScriptResult(data=win)


#===============================================================================
# UI 
#===============================================================================

class RolesListWindow(windows.ExtWindow):

    def __init__(self, *args, **kwargs):
        super(RolesListWindow, self).__init__(*args, **kwargs)

        self.title = u'Роли пользователей'
        self.layout = 'fit'
        self.width = 540
        self.height = 500
        self.template_globals = 'm3-users/roles-list-window.js'

        #=======================================================================
        # Настройка грида со списком ролей
        #=======================================================================
        self.grid = panels.ExtObjectGrid()
        self.grid.add_column(header=u'Наименование роли', data_index='name', width=300)
        self.grid.add_column(header=u'Метароль', data_index='metarole_name', width=240)
        self.items.append(self.grid)

        self.grid.action_data = RolesDataAction
        self.grid.action_new = EditRoleWindowAction
        self.grid.action_edit = EditRoleWindowAction
        self.grid.action_delete = DeleteRoleAction
        self.grid.top_bar.button_new.text = u'Добавить новую роль'
        self.grid.top_bar.items.append(controls.ExtButton(text=u'Показать пользователей', icon_cls='search', handler='contextMenu_ShowAssignedUsers'))
        self.grid.row_id_name = 'userrole_id'

        # дополнительные действия формы
        self.grid.action_show_assigned_users = ShowAssignedUsersAction

        self.grid.context_menu_row.add_item(text=u'Показать пользователей', icon_cls='user-icon-16', handler='contextMenu_ShowAssignedUsers')
        #self.grid.context_menu_row.add_item(text = u'Показать разрешения роли', icon_cls = 'edit_item', handler='contextMenu_ShowPermissions')
        self.grid.context_menu_row.add_separator()


        self.init_component(*args, **kwargs)


class RolesEditWindow(windows.ExtEditWindow):
    """
    Окно редактирования роли
    """

    CONTROLLER_TYPE = GetRolePermissionAction.CONTROLLER
    ACTION_TYPE = GetRolePermissionAction.ACTION
    PACK_TYPE = GetRolePermissionAction.PACK

    def __init__(self, new_role=False, *args, **kwargs):
        super(RolesEditWindow, self).__init__(*args, **kwargs)

        # Окно редактирования прав доступа
        self.edit_permission_url = EditPermissionWindowAction.absolute_url()
        self.del_all_permission_url = DelAllRolePermissionAction.absolute_url()

        self.width = 800
        self.height = 600
        self.modal = True

        self.new_role = new_role

        self.template_globals = 'm3-users/edit-role-window.js'

        self.title = u'Роль пользователя'
        self.layout = 'border'
        self.form = panels.ExtForm(layout='form', region='north', height=60, style={'padding': '5px'})

        self.form.label_width = 100
        self.form.url = SaveRoleAction.absolute_url()

        self.field_name = fields.ExtStringField(name='name', label=u'Наименование', allow_blank=False, anchor='100%')

        self.field_metarole = fields.ExtDictSelectField(name='metarole', label=u'Метароль', anchor='100%',
            hide_trigger=False, hide_dict_select_trigger=True)

        self.field_metarole.configure_by_dictpack(metaroles.Metaroles_DictPack, app_meta.users_controller)
        self.field_metarole.trigger_action = 'all'
        self.field_metarole.editable = False
        self.field_metarole.ask_before_deleting = False
        self.field_metarole.action_context = ActionContext(exclude_by_code=simplejson.dumps([metaroles.SUPER_ADMIN, metaroles.GENERIC_USER]))

        self.form.items.extend([self.field_name, self.field_metarole])


        tree = ExtTree()
        tree.layout = 'auto'
        tree.title = u'Параметры на форме'
        tree.region = 'center'
        tree.drag_drop = True
        tree.root_text = 'Root'
        tree.header = True
        tree.enable_drop = False

        tree.url = GetRolePermissionAction.absolute_url()

        act = ExtGridColumn()
        act.header = u'Наименование'
        act.data_index = 'name'
        act.menu_disabled = True
        act.width = 200

#        class_name = ExtGridColumn()
#        class_name.header = u'Название класса'
#        class_name.data_index = 'class_name'
#        class_name.menu_disabled = True
#
#        ttype = ExtGridColumn()
#        ttype.header = u'Права'
#        ttype.data_index = 'type'
#        ttype.menu_disabled = True        class_name = ExtGridColumn()
#        class_name.header = u'Название класса'
#        class_name.data_index = 'class_name'
#        class_name.menu_disabled = True
#
#        ttype = ExtGridColumn()
#        ttype.header = u'Права'
#        ttype.data_index = 'type'
#        ttype.menu_disabled = True

        perm = ExtGridColumn()
        perm.header = u'Права'
        perm.data_index = 'perm'
        perm.menu_disabled = True

        tree.columns.extend([act, perm])

        self.tree = tree

#        self.grid = ExtObjectGrid(title=u"Права доступа", region="center")
#        self.grid.action_data = GetRolePermissionAction
#        self.grid.action_new = AddRolePermission
#        self.grid.top_bar.items.append(controls.ExtButton(text=u'Удалить', icon_cls='delete_item', handler='deletePermission'))
#        self.grid.top_bar.button_refresh.hidden = True
#        self.grid.force_fit = True
#        self.grid.allow_paging = False
#        self.grid.row_id_name = 'permission_code'
#        self.grid.store.id_property = 'permission_code'
#        self.grid.store.auto_save = False
#        #self.grid.add_column(header=u'Действие', data_index='permission_code', width=100)
#        self.grid.add_column(header=u'Разрешенные права', data_index='verbose_name', width=100)
#        self.grid.add_bool_column(header=u'Запрет', data_index='disabled', width=50, text_false=u'Нет', text_true=u'Да', hidden=True)
        self.items.append(self.tree)

        self.buttons.extend([
            controls.ExtButton(text=u'Сохранить', handler='submitForm'),
            controls.ExtButton(text=u'Отмена', handler='cancelForm')
        ])

class AssignedUsersWindow(windows.ExtWindow):
    '''
    Окно просмотра пользователей, которые включены в данную роль
    '''
    def __init__(self, *args, **kwargs):
        super(AssignedUsersWindow, self).__init__(*args, **kwargs)
        self.title = u'Пользователи, с указанной ролью'
        self.width = 700
        self.height = 400
        self.modal = True

        self.layout = 'border'
        self.panel_north = panels.ExtForm(layout='form', region='north', height=40, label_width=50, style={'padding': '5px'})
        self.panel_center = panels.ExtPanel(layout='fit', region='center', body_cls='x-window-mc', title=u'Пользователи с данной ролью', style={'padding': '5px'})

        self.items.extend([
            self.panel_north,
            self.panel_center,
        ])

        # настройка северной панели
        self.field_role_name = fields.ExtStringField(name='role-name', label=u'Роль', anchor='100%', read_only=True)
        self.panel_north.items.append(self.field_role_name)

        # настройка центральной панели
        self.grid_users = panels.ExtObjectGrid()
        self.grid_users.allow_paging = False
        self.grid_users.add_column(header=u'Логин', data_index='user_login', width=100)
        self.grid_users.add_column(header=u'Фамилия', data_index='user_last_name', width=200)
        self.grid_users.add_column(header=u'Имя', data_index='user_first_name', width=200)
        self.grid_users.add_column(header=u'E-mail', data_index='user_email', width=200)
        self.grid_users.action_data = RoleAssignedUsersDataAction

        search_text_grid = ExtSearchField(empty_text = u'Поиск', component_for_search = self.grid_users)
        self.grid_users.top_bar.add_fill()
        self.grid_users.top_bar.items.append(search_text_grid)

        self.grid_users.allow_paging = True

        self.grid_users.action_new = SelectUsersToAssignWindowAction

        self.grid_users.action_delete = DeleteAssignedUser
        self.grid_users.top_bar.button_new.text = u'Добавить пользователей'
        self.grid_users.context_menu_grid.menuitem_new.text = u'Добавить пользователей'
        self.grid_users.context_menu_row.menuitem_new.text = u'Добавить пользователей'
        self.grid_users.context_menu_row.menuitem_delete.text = u'Удалить пользователя из роли'
        self.grid_users.row_id_name = 'assigneduser_id'
        self.panel_center.items.append(self.grid_users)


        self.buttons.append(controls.ExtButton(text=u'Закрыть', handler='closeWindow'))

class SelectPermissionWindow(windows.ExtEditWindow):
    '''
    Окно выбора прав доступа для добавления в роль
    '''
    def __init__(self, *args, **kwargs):
        super(SelectPermissionWindow, self).__init__(*args, **kwargs)
        self.title = u'Выберите права доступа для роли'
        self.width = 600
        self.height = 500
        self.maximizable = True
        self.layout = 'fit'
        self.tree = ExtTree()
        self.tree.add_column(header=u'Имя', data_index='name', width=140)
        self.tree.master_column_id = 'name'
        self.tree.nodes = get_all_permission_tree()
        self.items.append(self.tree)
        self.buttons.append(controls.ExtButton(text=u'Выбрать', handler='''function select(btn, e, baseParams) {
            var tree = Ext.getCmp('%s');
            var records = tree.getChecked();
            win.fireEvent('closed_ok', records);
            win.close(true);
        }''' % self.tree.client_id))
        self.buttons.append(controls.ExtButton(text=u'Отмена', handler='cancelForm'))


#===============================================================================
# Справочник "Роли пользователей"
#===============================================================================
class Roles_DictPack(BaseDictionaryModelActions):
    '''
    Справочник "Роли пользователей".
    
    Используется для выбора значений.
    '''
    url = '/roles-dict'
    shortname = 'user-roles-dictpack'
    model = models.UserRole
    title = u'Роли пользователей системы'
    list_columns = [('name', u'Наименование'), ]
    edit_window = RolesEditWindow
    filter_fields = ['name']
    list_readonly = True # справочник - только для выбора из него
