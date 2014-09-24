#coding:utf-8
'''
Created on 11.06.2010

@author: akvarats
'''

from m3.ui import actions
from m3.helpers import ui as ui_helpers

from m3.ui.ext import windows
from m3.ui.ext import panels
from m3.ui.ext import fields
from m3.ui.ext import controls

import helpers

class UsersActions(actions.ActionPack):
    '''
    Пакет действий для пользователей системы
    '''
    
    def __init__(self):
        super(UsersActions, self).__init__()
        self.actions = [
            UsersDataAction(),
        ]
        
class UsersDataAction(actions.Action):
    '''
    Получение списка пользователей
    '''
    url = '/users-data'
    
    def context_declaration(self):
        return [
            actions.ActionContextDeclaration(name='filter', type=int, required=True, default=''),
            actions.ActionContextDeclaration(name='start', type=int, required=True, default=0),
            actions.ActionContextDeclaration(name='limit', type=int, required=True, default=25),
        ]
    
    def run(self, request, context):
        return actions.JsonResult(ui_helpers.paginated_json_data(helpers.get_users_query(context.filter), context.start, context.limit))
    

class SelectUsersListWindow(windows.ExtWindow):
    '''
    Окно со списком пользователей
    '''
    
    def __init__(self, *args, **kwargs):
        super(SelectUsersListWindow, self).__init__(*args, **kwargs)
        self.title = u'Выберите пользователей'
        self.width = 600
        self.height = 400
        self.layout = 'fit'
        self.modal = True
        self.template_globals = 'm3-users/select-users-window.js'
        
        self.grid = panels.ExtObjectGrid(sm=panels.ExtGridCheckBoxSelModel())
        self.grid.add_column(header = u'Логин', data_index = 'username', width=150)
        self.grid.add_column(header = u'Фамилия', data_index = 'last_name', width=150)
        self.grid.add_column(header = u'Имя', data_index = 'first_name', width=150)
        self.grid.add_column(header = u'E-mail', data_index = 'email', width=150)
        
        self.items.append(self.grid)
        
        self.buttons.extend([
            controls.ExtButton(text='OK', handler='appendUsers'),
            controls.ExtButton(text='Отмена', handler='closeWindow'),
        ])        