#coding: utf-8
"""
Результаты выполнения действий
"""

import json
import abc
from copy import copy

from django import http

from context import ActionContext


class ActionResult(object):
    __metaclass__ = abc.ABCMeta
    """
    Класс описывает результат выполнения Action'а
    Данный класс является абстрактным.
    """

    def __init__(self, data=None, http_params={}):
        """
        *data* - данные, на основе которых будет сформирован
        результат выполнения действия.
        Тип объекта, передаваемого через data
        зависит от дочернего результата.
        *http_params* - параметры http,
        которые будут помещены в ответ сервера
        """
        self.data = data
        self.http_params = (http_params is None and {}) or http_params

    @abc.abstractmethod
    def get_http_response(self):
        """
        Возвращает объект django.http.HttpResponse,
        соответствующий данном результату выполнения действия
        """
        pass

    def process_http_params(self, response):
        if self.http_params:
            for k, v in self.http_params.items():
                response[k] = v
        return response


class PreJsonResult(ActionResult):
    """
    Результат выполнения операции в виде, например, списка объектов, готовых к
    сериализации в JSON формат и отправке в HttpResponse.
    В *data* передается объект для сериализации.
    В *dict_list* указывается список объектов
    и/или атрибутов вложенных объектов для
    более глубокой сериализации. Смотри класс т3.core.json.M3JSONEncoder.
    Параметр специфичный для проекта *secret_values*
    - используется чтобы указать,
    что передаются персональные обезличенные данные
    и их расшифровать перед отправкой клиенту.
    """
    def __init__(self, data=None, secret_values=False, dict_list=None):
        super(PreJsonResult, self).__init__(data)
        from m3 import M3JSONEncoder
        self.encoder_clz = M3JSONEncoder
        self.secret_values = secret_values
        self.dict_list = dict_list

    def get_http_response(self):
        encoder = self.encoder_clz(dict_list=self.dict_list)
        result = encoder.encode(self.data)
        response = http.HttpResponse(result, mimetype='application/json')
        if self.secret_values:
            response['secret_values'] = True
        return response


class JsonResult(ActionResult):
    """
    Результат выполнения операции
    в виде готового JSON объекта для возврата в response.
    Для данного класса в *data* храниться строка с данными JSON объекта.
    """
    def get_http_response(self):
        return http.HttpResponse(self.data, mimetype='application/json')


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
        return http.HttpResponse(
            self.data,
            mimetype='application/xml',
            content_type='text/xml; charset=utf-8'
        )


#==============================================================================
# Результаты выполнения операции с заданным контекстом
#==============================================================================
class BaseContextedResult(ActionResult):
    """
    Абстрактный базовый класс, который оперирует понятием результата
    выполнения операции, 'отягощенного некоторым контектом'
    """
    def __init__(self, data=None, context=None, http_params={}):
        super(BaseContextedResult, self).__init__(data, http_params)
        self.set_context(context)

    def set_context(self, context):
        if isinstance(context, ActionContext):
            # в случае если задан реальный
            # результат выполнения операции,
            # то его и регистрируем
            self.context = context
        elif context is None:
            # Пустой контекст
            self.context = ActionContext()
        else:
            raise TypeError('context must be a ActionContext instance')


class OperationResult(ActionResult):
    """
    Результат выполнения операции,
    описанный в виде Ajax результата ExtJS: success или failure.
    В случае если операция выполнена успешно,
    параметр *success* должен быть True, иначе False.
    *message* - сообщение, поясняющее результат выполнения операции.
    *code* - текст javascript, который будет выполнен на клиенте в результате
    обработки результата операции.
    """

    def __init__(
            self, success=True, code='', message='', *args, **kwargs):
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
        Возвращает экземпляр OperationResult
        построенный исходя из сообщения *message*.
        Если сообщение не пустое,
        то операция считается проваленной и success=False,
        иначе операция считается успешной success=True.
        """
        result = OperationResult()
        if message:
            result.success = False
            result.message = message
        return result

    def get_http_response(self):
        """
        Возвращает объект HttpResponse,
        соответствующий данному результату выполнения операции
        """
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
    Экшен предварительно находится с помощью метода
    ActionController.get_action_url()
    """
    def __init__(self, action, context=None):
        self.action = action
        self.context = context

    def prepare_request(self, request):
        if self.context:
            new_post = copy(request.POST)
            for k, v in new_post.__dict__.iteritems():
                new_post[k] = getattr(self.context, k, v)
            request.POST = new_post
            del request._request
        return request
