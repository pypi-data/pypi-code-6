# coding: utf-8

"""
модуль представлений приложения
"""

from cStringIO import StringIO
import os
import time

from django.core import management
from django.conf import settings
from django.shortcuts import render_to_response, redirect


def debug(request):
    """
    обработчик страницы информации приложения

    также обрабатывает гет запросы включения, выключения
        записи отладочной информации
    удаления файла отладки
    """
    if not request.user.is_superuser:
        return redirect('/')

    action = request.GET.get('action', None)

    if action == 'activate':
        # активация отладчика
        prefix = str(time.time()) + '.dbg'
        request.session['debug_on'] = True
        request.session['debug_file_path'] = os.path.join(settings.MEDIA_ROOT,
                                                          prefix)
        request.session['debug_file_url'] = os.path.join(settings.MEDIA_URL,
                                                         prefix)
        open(request.session['debug_file_path'], 'w')

    elif action == 'deactivate':
        # выключение отладчика
        request.session['debug_on'] = False

    elif (action == 'delete'
          and 'debug_file_path' in request.session
          and os.path.exists(request.session['debug_file_path'])):
        # удаление файла дампа
        os.remove(request.session['debug_file_path'])
        request.session['debug_on'] = False
        del request.session['debug_file_path']
        del request.session['debug_file_url']
    elif action == 'dump_data':
        # выгрузка дампа БД
        buf = StringIO()
        management.call_command(
            'dumpdata',
            stdout=buf,
            indent=4,
            exclude=getattr(settings, 'SMOKNUR_EXCLUDE_APP_DUMPDATA', ()))
        prefix = str(time.time()) + '.json'
        buf.seek(0)
        open(os.path.join(settings.MEDIA_ROOT, prefix), 'w').write(buf.read())
        return redirect('/media/' + prefix)
    else:
        return render_to_response(
            'debug.html',
            {
                'debug_on': request.session.get('debug_on', None),
                'debug_file_path': request.session.get('debug_file_path', None),
                'debug_file_url': request.session.get('debug_file_url', None)
            })
    return redirect('/smoknur')
