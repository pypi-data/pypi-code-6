#coding: utf-8
'''
Результаты выполнения действий

@author: akvarats
'''

import json
from copy import copy

from django import http

from m3.core.json import M3JSONEncoder
from m3.helpers import ui as ui_helpers

from context import ActionContext

class ActionResult(object):
    '''
    Класс описывает результат выполнения Action'а
    
    Данный класс является абстрактным.
    '''
    
    def __init__(self, data = None, http_params = {}):
        """
        *data* - данные, на основе которых будет сформирован результат выполнения действия.
        Тип объекта, передаваемого через data зависит от дочернего результата.
        *http_params* - параметры http, которые будут помещены в ответ сервера
        """
        self.data = data
        self.http_params = http_params
        
    def get_http_response(self):
        '''
        Возвращает объект django.http.HttpResponse, соответствующий данном результату выполнения действия
        '''
        raise NotImplementedError()
    
    def process_http_params(self, response):
        for k, v in self.http_params.items():
            response[k] = v
        return response
              
        
    
class PreJsonResult(ActionResult):
    """
    Результат выполнения операции в виде, например, списка объектов, готовых к
    сериализации в JSON формат и отправке в HttpResponse.
    В *data* передается объект для сериализации.
    В *dict_list* указывается список объектов и/или атрибутов вложенных объектов для
    более глубокой сериализации. Смотри класс т3.core.json.M3JSONEncoder.
    Параметр специфичный для проекта *secret_values* - используется чтобы указать,
    что передаются персональные обезличенные данные и их расшифровать перед отправкой клиенту. 
    """
    def __init__(self, data = None, secret_values = False, dict_list = None):
        super(PreJsonResult, self).__init__(data)
        self.secret_values = secret_values
        self.dict_list = dict_list 
    
    def get_http_response(self):
        encoder = M3JSONEncoder(dict_list = self.dict_list)
        result = encoder.encode(self.data)
        response = http.HttpResponse(result, mimetype='application/json')
        if self.secret_values:
            response['secret_values'] = True
        return response

class JsonResult(ActionResult):
    '''
    Результат выполнения операции в виде готового JSON объекта для возврата в response.
    Для данного класса в *data* храниться строка с данными JSON объекта.
    '''
    def get_http_response(self):
        return http.HttpResponse(self.data, mimetype='application/json')

class ExtGridDataQueryResult(ActionResult):
    '''
    Результат выполнения операции, который выдает данные в формате, пригодном для 
    отображения в гриде
    '''
    def __init__(self, data=None, start = -1, limit = -1):
        super(ExtGridDataQueryResult, self).__init__(data)
        self.start = start
        self.limit = limit
        
    def get_http_response(self):
        return http.HttpResponse(ui_helpers.paginated_json_data(self.data, self.start, self.limit))

class HttpReadyResult(ActionResult):
    '''
    Результат выполнения операции в виде готового HttpResponse. 
    Для данного класса в *data* храниться объект класса HttpResponse.
    '''
    def get_http_response(self):
        return self.data
    
class TextResult(ActionResult):
    '''
    Результат, данные *data* которого напрямую передаются в HttpResponse
    '''
    def get_http_response(self):
        return http.HttpResponse(self.data)

class XMLResult(ActionResult):
    '''
    Результат в формате xml, данные которого напрямую передаются в HttpResponse
    '''
    def get_http_response(self):
        return http.HttpResponse(self.data,mimetype='application/xml',
                                 content_type='text/xml; charset=utf-8')


class ExtAdvancedTreeGridDataQueryResult(ActionResult):
    '''
    Результат выполнения операции в формате, удобным для отображения в 
    Ext.m3.AdvancedTreeGrid
    '''
    def __init__(self, data=None, start = -1, limit = -1):
        super(ExtAdvancedTreeGridDataQueryResult, self).__init__(data)
        self.start = start
        self.limit = limit
    
    def get_http_response(self):
        return http.HttpResponse(ui_helpers.mptt_json_data(query = self.data, 
                                                           start = self.start, 
                                                           limit = self.limit),
                                 mimetype='application/json')

#===============================================================================
# Результаты выполнения операции с заданным контекстом 
#===============================================================================

class BaseContextedResult(ActionResult):
    '''
    Абстрактный базовый класс, который оперирует понятием результата 
    выполнения операции, 'отягощенного некоторым контектом'
    '''
    def __init__(self, data = None, context = None, http_params = {}):
        super(BaseContextedResult, self).__init__(data, http_params)
        self.set_context(context)
            
    def set_context(self, context):
        if isinstance(context, ActionContext):
            # в случае если задан реальный результат выполнения операции, то его и регистрируем
            self.context = context
        elif context is None:
            # Пустой контекст
            self.context = ActionContext()
        else:
            raise TypeError('context must be a ActionContext instance')


class ExtUIComponentResult(BaseContextedResult):
    '''
    Результат выполнения операции, описанный в виде отдельного компонента пользовательского интерфейса.
    В self.data хранится некоторый наследник класса m3.ui.ext.ExtUiComponent.
    Метод get_http_response выполняет метод render у объекта в self.data.
    '''
    def get_http_response(self):
        self.data.action_context = self.context
        return http.HttpResponse(self.data.render())



class ExtUIScriptResult(BaseContextedResult):
    '''
    По аналогии с ExtUiComponentResult, представляет собой некоторого наследника класса ExtUiComponent.
    Единственное отличие заключается в том, что get_http_response должен сформировать
    готовый к отправке javascript. Т.е. должен быть вызван метод self.data.get_script()
    '''
    def __init__(self, data = None, context = None, http_params = {}, secret_values = False):
        super(ExtUIScriptResult, self).__init__(data, context, http_params)
        self.secret_values = secret_values
    
    def get_http_response(self):
        self.data.action_context = self.context
        response = http.HttpResponse(self.data.get_script())
        
        response = self.process_http_params(response)
        
        if self.secret_values:
            response['secret_values'] = True
        return response
    
class OperationResult(ActionResult):
    """
    Результат выполнения операции, описанный в виде Ajax результата ExtJS: success или failure.
    В случае если операция выполнена успешно, параметр *success* должен быть True, иначе False.
    *message* - сообщение, поясняющее результат выполнения операции.
    *code* - текст javascript, который будет выполнен на клиенте в результате
    обработки результата операции.
    """
    def __init__(self, success = True, code = '', message = '', *args, **kwargs):
        super(OperationResult, self).__init__(*args, **kwargs)
        # Результат выполнения операции: успех/неудача
        self.success = success
        # Сообщение об ошибке выводимое при неудаче
        self.message = message
        # Произвольный JS код, который выполняется в любом случае если задан
        self.code = code
    
    @staticmethod
    def by_message(message):
        """
        Возвращает экземпляр OperationResult построенный исходя из сообщения *message*.
        Если сообщение не пустое, то операция считается проваленной и success=False,
        иначе операция считается успешной success=True.
        """
        result = OperationResult()
        if message:
            result.success = False
            result.message = message
        return result
    
    def get_http_response(self):
        '''
        Возвращает объект HttpResponse, соответствующий данному результату выполнения операции
        '''
        result = {
            'message': self.message,
            'success': True if self.success else False
        }
        result = json.JSONEncoder().encode(result)
        
        # Вставляем функцию прямо в JSON без кодирования
        if self.code:
            self.code = self.code.strip()
            if self.code[len(self.code)-2:len(self.code)] == '()':
                code = ' ,"code": %s' % self.code[:-2]
            else:
                code = ' ,"code": %s' % self.code
            result = result[:-1] + code + result[-1]
        
        repsonse = http.HttpResponse(result)
        repsonse = self.process_http_params(repsonse)
        return repsonse


class ActionRedirectResult(object):
    """
    Перенаправляет обработку запроса на другой экшен.
    Экшен предварительно находится с помощью метода ActionController.get_action_url()
    """
    def __init__(self, action, context=None):
        self.action = action
        self.context = context
        
    def prepare_request(self, request):
        if self.context:
            new_post = copy(request.POST)
            for k,v in self.context.__dict__.iteritems():
                if not new_post.has_key(k):
                    new_post[k] = v
            request.POST = new_post
            del request._request
        return request
                
    