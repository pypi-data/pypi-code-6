#coding:utf-8
'''
Created on 14.12.2010

@author: Камилла
'''
from m3.ui.actions import ActionPack, Action, ExtUIScriptResult, OperationResult,\
    ActionContextDeclaration, PreJsonResult
import forms

from m3.helpers import logger
import helpers as admin_helpers
import models
from m3.ui.actions.packs import BaseDictionaryModelActions

class QueryConsoleActionsPack(ActionPack):
    '''
    Набор действий для работы с административной панелью
    '''
    def __init__(self):
        super(QueryConsoleActionsPack, self).__init__()
        self.query_console_win_action = QyeryConsoleWinAction()
        self.query_console_action = QueryConsoleAction()
        self.new_query_save_win_action =  NewQuerySaveWinAction()
        self.new_query_save_action = NewQuerySaveAction()
        self.load_selected_query = LoadSelectedQuery()
        
        self.actions.extend([self.query_console_win_action
                            , self.query_console_action, self.new_query_save_win_action,
                            self.new_query_save_action, self.load_selected_query])

class QyeryConsoleWinAction(Action):
    '''
    Выводит окно для ввода запроса
    '''
    
    url = '/query_console_window'
    
    def run(self, request, context):
        window_params = {}
        window_params['query_console_window_url'] = self.parent.query_console_win_action.get_absolute_url()
        window_params['query_console_url'] = self.parent.query_console_action.get_absolute_url()
        window_params['new_query_save_url'] = self.parent.new_query_save_win_action.get_absolute_url()
        window_params['load_selected_query_url'] = self.parent.load_selected_query.get_absolute_url()
        
        window_params.update(context.__dict__)
        
        win = forms.ExtQueryConsoleWindow(window_params)
        return ExtUIScriptResult(win, context)
    
class QueryConsoleAction(Action):
    '''
    Обрабатывает запрос 
    '''
    
    url = '/query_console'
    
    def context_declaration(self):
        return [ActionContextDeclaration('query_str', default = '', type = str, required = True)]
    
    def run(self, request, context):
        error_message = ''
        checking = context.query_str.lower()
        if checking[0:6]=='select':
            check_phrase = ['drop','grant','alter','create','update','insert','delete']
            for wrong_word in check_phrase:
                if checking.find(' '+wrong_word+' ') != -1 or checking.find('\n'+wrong_word+' ') != -1\
                    or checking.find(' '+wrong_word+'\n') != -1 or checking.find('\n'+wrong_word+'\n') != -1:
                    error_message = u'Запрос содержит не должен содержать слово %s' % (wrong_word) 
                    return OperationResult.by_message(error_message) 
            try:  
                rows, error, colm_name = admin_helpers.query_result_list(context.query_str) 
                if error==None:
                    return PreJsonResult({'total': len(rows), 'rows': list(rows), 'column': list(colm_name)})                                
                else:
                    return OperationResult.by_message(error)
            except Exception, e:
                return OperationResult.by_message(u'' +e.args[0])
        else:
            error_message = u'Запрос должен начинаться с SELECT.'
        return OperationResult.by_message(error_message)            

class NewQuerySaveWinAction(Action):
    '''
    Окно для ввод нового запроса
    '''
    
    url = '/new_query_save_window'
    
    def context_declaration(self):
        return [ActionContextDeclaration('query_name', default = '', type = str, required = True)]
    
    def run(self, request, context):
        window_params = {'new_query_save_url': 
                         self.parent.new_query_save_action.get_absolute_url()}
        window_params.update(context.__dict__)
        win = forms.ExtNewQueryWindow(window_params)
        
        return OperationResult(code=win.get_script()) 
    
class NewQuerySaveAction(Action):
    '''
    Сохранение нового запроса
    '''
    
    url = '/new_query_save'
    
    def context_declaration(self):
        return [ActionContextDeclaration('query_str', default = '', type = str, required = True),
                ActionContextDeclaration('query_name', default = '', type = str, required = True)]
    
    def run(self, request, context):
        error_message = ''            
        try:
            admin_helpers.new_query_save(context.query_name, context.query_str)
        except:
                error_message = u'Не удалось сохранить запрос. Вероятно запрос неверный.'
                logger.exception(error_message)
        return OperationResult.by_message(error_message)
    
class LoadSelectedQuery(Action):
    '''
    Загрузка выбранного запроса
    '''
    
    url = '/load_selected_query'
    
    def contect_declaration(self):
        return [ActionContextDeclaration('query_id', default = '', required = True)]
    
    def run(self, request, context):
        error_message = ''
        try:
            rows = admin_helpers.load_query(context.query_id, False)
            return PreJsonResult({'rows': rows})
        except:
            error_message = u'Не удалось загрузить запрос'
        return OperationResult.by_message(error_message)
#===============================================================================
# Справочник запросов
#===============================================================================    
class CustomQueries_DictPack(BaseDictionaryModelActions):
    url = '/custom_queries'
    model = models.CustomQueries
    title = u'Пользовательские запросы'
    list_columns = [('code', u'Код', 15),
                    ('name', u'Наименование'),
                    ('query', u'SQL запрос')]

    filter_fields = ['name']
    
    def get_select_window(self, win):
        ''' Возвращает настроенное окно типа "Список" справочника '''
        win.grid.top_bar.items[0].disabled = True        
        win.grid.top_bar.items[1].disabled = True
        win.grid.handler_rowcontextmenu.items[0].disabled = True
        win.grid.handler_rowcontextmenu.items[1].disabled = True
        
        win.grid.handler_contextmenu.items[0].disabled = True
        return win
