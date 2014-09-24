#coding: utf-8
import json
from m3_legacy.datastructures import TypedList

from m3_ext.ui import render_component
from m3_ext.ui.all_components import *
from m3_ext.ui.containers.base import BaseExtPanel


class ConstructorWindow(ExtWindow):
    """
    Класс, связанный с главным окном приложения
    """

    def __init__(self, src, *args, **kwargs):
        super(ConstructorWindow, self).__init__(*args, **kwargs)

        # JS шаблон, в котором создается главное окно
        self.template = 'js/constructor_window.js'

        # src - адрес, из которого будет подгружены данные во фрейм главного окна
        self.src = src

    def render(self):

        return render_component(self)
    
    
class SimpleTreeGrid(BaseExtPanel):
    '''
    Дерево с колонками
    '''
    def __init__(self, *args, **kwargs):
        super(SimpleTreeGrid, self).__init__(*args, **kwargs)
        self.template = 'js/simple-tree-grid.js'

        self.master_column_id = None

        self.auto_expand_column = None

        self.data = []

        # Список колонок
        self._items = []

        self.top_bar = SimpleTreeGrid.TopBar()

        self.init_component(*args, **kwargs)

    # def make_read_only(self, access_off=True, exclude_list=[], *args, **kwargs):
    #     # Описание в базовом классе ExtUiComponent.
    #     # Обрабатываем исключения.
    #     access_off = self.pre_make_read_only(access_off, exclude_list, *args, **kwargs)
    #     # Выключаем\включаем компоненты.
    #     super(SimpleTreeGrid, self).make_read_only(access_off, exclude_list, *args, **kwargs)
    #     self.read_only = access_off
    #     # контекстное меню.
    #     context_menu_items = [self.handler_contextmenu,
    #                           self.handler_containercontextmenu]
    #     for context_menu in context_menu_items:
    #         if (context_menu and
    #             hasattr(context_menu,'items') and
    #             context_menu.items and
    #             hasattr(context_menu.items,'__iter__')):
    #                 for item in context_menu.items:
    #                     if isinstance(item, ExtUIComponent):
    #                         item.make_read_only(self.read_only, exclude_list, *args, **kwargs)

    def t_render_record(self):
        result = []
        for x in self._items:
            result.append({
                "name": x.data_index
            })
        result.extend([
            {"name": '_id', "type": 'int'},
            {"name": '_level', "type": 'int'},
            {"name": '_is_leaf', "type": 'bool'},
            {"name": '_parent', "type": 'int'}
        ])

        return json.dumps(result)

    def t_render_data(self):
        result = []
        for datum_ in self.data:
            datum = {}
            datum.update(datum_)
            result.append(datum)

        return json.dumps(result)

    def t_render_columns(self):
        return self.t_render_items()


    class TopBar(containers.ExtToolBar):
        '''
        Внутренний класс для удобной работы топбаром грида
        '''
        def __init__(self, *args, **kwargs):
            super(SimpleTreeGrid.TopBar, self).__init__(*args, **kwargs)
            # self.button_new = controls.ExtButton(text = u'Добавить',
            #                         icon_cls = 'add_item', handler='topBarNew')
            # self.button_edit = controls.ExtButton(text = u'Изменить',
            #                         icon_cls = 'edit_item', handler='topBarEdit')
            # self.button_delete = controls.ExtButton(text = u'Удалить',
            #                         icon_cls = 'delete_item', handler='topBarDelete')
            # self.button_refresh = controls.ExtButton(text = u'Обновить',
            #                         icon_cls = 'x-tbar-loading', handler='topBarRefresh')
            #
            # self.items.extend([
            #     self.button_new,
            #     self.button_edit,
            #     self.button_delete,
            #     self.button_refresh,
            # ])
            #
            # self.init_component()


    def add_nodes(self, *args):
        '''
        Добавляет переданные узлы дерева
        :param *args: Узлы дерева
        '''
        for node in args:
            self.data.append(node)

    def add_column(self,**kwargs):
        '''
        Добавляет колонку с аргументами
        :param **kwargs: Аргументы
        '''
        self.columns.append(ExtGridColumn(**kwargs))

    def add_bool_column(self,**kwargs):
        '''
        Добавляет колонку с аргументами
        :param **kwargs: Аргументы
        '''
        self.columns.append(ExtGridBooleanColumn(**kwargs))

    def add_number_column(self,**kwargs):
        '''
        Добавляет колонку с аргументами
        :param **kwargs: Аргументы
        '''
        self.columns.append(ExtGridNumberColumn(**kwargs))

    def add_date_column(self,**kwargs):
        '''
        Добавляет колонку с аргументами
        :param **kwargs: Аргументы
        '''
        self.columns.append(ExtGridDateColumn(**kwargs))

    @property
    def columns(self):
        return self._items

    # @property
    # def url(self):
    #     return self.__url

    # @url.setter
    # def url(self, value):
    #     self.tree_loader.url = value
    #     self.__url = value

    # #//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\
    # # Врапперы над событиями listeners[...]
    # #------------------------------------------------------------------------
    # @property
    # def handler_contextmenu(self):
    #     return self._listeners.get('contextmenu')
    #
    # @handler_contextmenu.setter
    # def handler_contextmenu(self, menu):
    #     menu.container = self
    #     self._listeners['contextmenu'] = menu
    #
    # @property
    # def handler_containercontextmenu(self):
    #     return self._listeners.get('containercontextmenu')
    #
    # @handler_containercontextmenu.setter
    # def handler_containercontextmenu(self, menu):
    #     menu.container = self
    #     self._listeners['containercontextmenu'] = menu
    #
    # @property
    # def handler_click(self):
    #     return self._listeners.get('click')
    #
    # @handler_click.setter
    # def handler_click(self, function):
    #     self._listeners['click'] = function
    #
    # @property
    # def handler_dblclick(self):
    #     return self._listeners.get('dblclick')
    #
    # @handler_dblclick.setter
    # def handler_dblclick(self, function):
    #     self._listeners['dblclick'] = function
    #
    # @property
    # def handler_dragdrop(self):
    #     return self._listeners.get('dragdrop')
    #
    # @handler_dragdrop.setter
    # def handler_dragdrop(self, function):
    #     self._listeners['dragdrop'] = function
    #
    #
    # @property
    # def handler_dragover(self):
    #     return self._listeners.get('nodedragover')
    #
    # @handler_dragover.setter
    # def handler_dragover(self, function):
    #     self._listeners['nodedragover'] = function
    #
    #
    # @property
    # def handler_startdrag(self):
    #     return self._listeners.get('startdrag')
    #
    # @handler_startdrag.setter
    # def handler_startdrag(self, function):
    #     self._listeners['startdrag'] = function
    #
    #
    # @property
    # def handler_enddrag(self):
    #     return self._listeners.get('enddrag')
    #
    # @handler_enddrag.setter
    # def handler_enddrag(self, function):
    #     self._listeners['enddrag'] = function
    #
    # @property
    # def handler_drop(self):
    #     return self._listeners.get('nodedrop')
    #
    # @handler_drop.setter
    # def handler_drop(self, function):
    #     self._listeners['nodedrop'] = function
    #
    # @property
    # def handler_beforedrop(self):
    #     return self._listeners.get('beforenodedrop')
    #
    # @handler_beforedrop.setter
    # def handler_beforedrop(self, function):
    #     self._listeners['beforenodedrop'] = function
    #
    # #----------------------------------------------------------------------------
    #
    # def render_base_config(self):
    #     super(SimpleTreeGrid, self).render_base_config()
    #     self._put_config_value('useArrows', True)
    #     self._put_config_value('autoScroll', False)
    #     self._put_config_value('animate', True)
    #     self._put_config_value('containerScroll', True)
    #     if self.drag_drop and not self.read_only:
    #         self._put_config_value('enableDD', True)
    #         self._put_config_value('dropConfig', {'allowContainerDrop': self.allow_container_drop,
    #                                               'allowParentInsert': self.allow_parent_insert
    #                                               })
    #     else:
    #         self._put_config_value('enableDrop', self.enable_drop)
    #         self._put_config_value('enableDrag', self.enable_drag)
    #
    #     self._put_config_value('columns', self.t_render_columns)
    #     self._put_config_value('loader', self.t_render_tree_loader)
    #     self._put_config_value('root', self.t_render_root)
    #     self._put_config_value('plugins', lambda: '[%s]' % ','.join(self.plugins))
    #
    # def render_params(self):
    #     super(SimpleTreeGrid, self).render_params()
    #     self._put_params_value('customLoad', self.custom_load)
