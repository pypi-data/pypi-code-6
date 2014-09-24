#coding:utf-8
'''
Created on 24.08.2010

@author: kir
'''
import datetime

from m3.ui.actions import ActionPack, Action, ExtUIScriptResult
from m3.ui.actions.context import ActionContextDeclaration
from m3_logview import forms
from m3_logview import helpers as admin_helpers
from m3.ui.ext.misc.store import ExtDataStore
from m3.ui.actions.results import OperationResult, PreJsonResult


class LogsAction(Action):
    '''
    Выводит наименование имеющихся файлов логирования
    '''
    url = '/logs'
    shortname='logview.main-window'
    
    def run(self, request, context):
        window_params = {
            'get_logs_url': self.parent.GetLogsAction.get_absolute_url(),
            'logs_list_by_date_url': self.parent.LogsDateChangeAction.get_absolute_url()
        }
        window_params.update(context.__dict__)
        
        win = forms.ExtLogsWindow(window_params)
        win.grid.action_data = GetLogsAction
        logs_array = admin_helpers.log_files_list()
        logs_store = ExtDataStore(logs_array)
        win.log_files_combo.set_store(logs_store)
        error_log = admin_helpers.ERROR
        if logs_array:
            for log_file in logs_array:
                if error_log in log_file:
                    win.log_files_combo.value = error_log
                    break
            else:
                win.log_files_combo.value = logs_array[0][1]
        return ExtUIScriptResult(win)

class LogsDateChangeAction(Action):
    '''
    Получает список лог файлов по дате
    '''
    url = '/logs-by-date'
    
    def context_declaration(self):
        return [ActionContextDeclaration('start_date', default='', type=str, required=True),
                ActionContextDeclaration('end_date', default='', type=str, required=True)]
    def run(self, request, context):
        start_date = datetime.datetime.strptime(context.start_date,'%Y-%m-%d').date()
        if start_date == datetime.date.today():
            return PreJsonResult(admin_helpers.log_files_list())
        logs = admin_helpers.log_files_list(context.start_date, context.end_date)
        return PreJsonResult(logs)
    
class GetLogsAction(Action):
    '''
    Получает файл логирования
    '''
    url = '/get-logs-file'
    
    def context_declaration(self):
        
        return [ActionContextDeclaration(name='start', type=int, required=True,
                                         default=0),
                ActionContextDeclaration(name='limit', type=int, required=True,
                                         default=0),
                ActionContextDeclaration('filename', default='', type=str, 
                                         required=True)]
        
    def run(self, request, context):
        if request.POST.get('filename'):
            file_content = admin_helpers.get_log_content(context.filename)
            return PreJsonResult({'total': len(file_content),
                                  'rows': file_content[context.start: context.start+context.limit]})
        return OperationResult.by_message('Ошибка при попытке чтения файла')

class Mis_Admin_ActionsPack(ActionPack):
    '''
    Набор действий для работы с административной панелью
    '''
    def __init__(self):
        super(self.__class__,self).__init__()
        self.LogsAction = LogsAction()
        self.GetLogsAction = GetLogsAction()
        self.LogsDateChangeAction = LogsDateChangeAction()
        
        self.actions = [ self.LogsAction, self.GetLogsAction
                        ,self.LogsDateChangeAction]
        
