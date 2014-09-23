# -*- coding: utf-8 -*-

from uuid import uuid4
import datetime
import os
import io
import importlib
import re
import sys

from m3 import M3JSONEncoder

from django.views.debug import ExceptionReporter
from django.conf import settings

try:
    from threading import local
except ImportError:
    from django.utils._threading_local import local
_thread_locals = local()


DUMP_EXT = '.ddump.txt'


def get_header(request):
    """
    Возвращает заголовок блока отладочной информации
    """
    if not getattr(_thread_locals, 'debug_header', None):
        _thread_locals.debug_header = {
            'time': datetime.datetime.now(),
            'url': request.path_info,
            'uid': str(uuid4()),
            'user': [request.user.username, request.user.id]
        }
    return _thread_locals.debug_header


def get_sys_info():
    """
    Возвращает дамп информации о системе
    на основе данных, возвращаемых функцией,
    указанной в settings.DEBUGGIE_SYSTEM_INFO_CALLBACK

    Важно:
    Информация получается путем вызова ф-ции один раз,
    и затем кэшируется!
    """
    info = get_sys_info.func_dict.get('_cache')
    if not info:
        info = get_default_system_info()
        try:
            module, fn = re.match(
                r'^(.*)\.(\w+)$',
                settings.DEBUGGIE_SYSTEM_INFO_CALLBACK
            ).groups()
        except AttributeError:
            pass
        else:
            module = importlib.import_module(module)
            info['custom'] = getattr(module, fn)()
        info = M3JSONEncoder().encode({'system_info': info})
        get_sys_info.func_dict['_cache'] = info
    return info


def get_fname(request):
    """
    Возвращает имя файла, в который происходит запись дампа
    """
    name = request.session.get('debug_out_file')
    if not name:
        name = os.path.join(
            settings.MEDIA_ROOT,
            '%s%s' % (uuid4(), DUMP_EXT)
        )
        request.session['debug_out_file'] = name
    return name


def get_download_url(request):
    """
    Возвращает url для загрузки дампа, если файл уже существует.
    В противном случае возвращает None
    """
    name = request.session.get('debug_out_file')
    if name:
        name = os.path.split(name)[1]
        name = '%s%s' % (settings.MEDIA_URL, name)
    return name


def get_status(request):
    """
    Вовращает признак: "режим отладки включен/выключен"
    """
    return request.session.get('debug_enabled', False)


def toggle_status(request):
    """
    Включает/выключает режим отладки для текущего пользователя
    """
    request.session['debug_enabled'] = not get_status(request)


def clear_records(request):
    """
    Сбрасывает дамп отладочной информации
    """
    try:
        os.remove(get_fname(request))
    except OSError as e:
        if e.errno == 2: # файл не найден
            pass
    request.session['debug_out_file'] = None


def tell(data, record_type='tell'):
    """
    Добавляет блоков отладочной информации новый блок,
    если режим отладки включен, в противном случае ничего не пишется
    """
    header = getattr(_thread_locals, 'debug_header', None)
    if header:
        record = header.copy()
        record['action'] = {
            'type': record_type,
            'data': data
        }
        text = M3JSONEncoder().encode(record)

        with io.FileIO(_thread_locals.debug_out_file, 'a') as f:
            if f.tell() == 0:
                # файл открыт по новой, значит пишем сведения о системе
                f.write(get_sys_info() + '\n')
            f.write(text + '\n')


def get_default_system_info():
    """
    Возвращает некоторрые сведения о системе
    """
    try:
        import pip
    except ImportError:
        packages = ['pip not installed!']
    else:
        packages = map(
            repr,
            pip.get_installed_distributions()
        )

    # К сожалению, os.uname работает только на Unix :(
    if 'win' in sys.platform:
        import platform
        uname = platform.uname()
    else:
        uname = os.uname()

    return {
        'uname': uname,
        'environ': dict(os.environ),
        'packages': packages
    }


class Debuggie(object):
    """
    Middleware, ведущая запись дампов отладочной информации
    """
    def _need_to_process(self, request):
        return (
			hasattr(request, 'session')
			and
            '/debug/' not in request.path_info
            and
            not request.path_info.endswith(DUMP_EXT)
            and
            get_status(request)
        )

    def process_request(self, request):
        if self._need_to_process(request):
            # в данных потока будет доступно имя текущего файла дампа
            _thread_locals.debug_out_file = get_fname(request)
            _thread_locals.debug_header = get_header(request)
            # сохранение контекста
            tell(
                {
                    'request': dict(request.REQUEST),
                    'cookies': dict(request.COOKIES),
                    'verb': request.method,
                    'body': request.raw_post_data,
                    'headers': {
                        'Content-Length': request.META.get('CONTENT_LENGTH'),
                        'Content-Type': request.META.get('CONTENT_TYPE'),
                    }
                },
                record_type='request'
            )
        else:
            # имя файла и заголовок записи зануляются на всякий случай
            _thread_locals.debug_out_file = None
            _thread_locals.debug_header = None

    def process_response(self, request, response):
        cls_to_status = {
            'HttpResponseServerError': 500,
            'HttpResponseGone': 410,
            'HttpResponseNotAllowed': 405,
            'HttpResponseForbidden': 403,
            'HttpResponseNotFound': 404,
            'HttpResponseBadRequest': 400,
            'HttpResponseNotModified': 304,
            'HttpResponsePermanentRedirect': 301,
            'HttpResponseRedirect': 302,
            'HttpResponse': 200
        }

        if self._need_to_process(request):
            tell({
                'content': response.content,
                'cookies': response.cookies,
                'verb': request.method,
                'status': cls_to_status[response.__class__.__name__]                
            }, 
            record_type='response')
        return response

    def process_exception(self, request, exception):	
        if self._need_to_process(request):
            reporter = ExceptionReporter(
                request, *sys.exc_info()
            )
            traceback = reporter.get_traceback_html()
            tell({'traceback': traceback}, record_type='catch')
