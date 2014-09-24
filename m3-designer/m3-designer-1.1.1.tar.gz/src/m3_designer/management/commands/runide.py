# coding: utf-8
'''
Created on 29.03.2011

@author: prefer
'''

import os
import subprocess
from optparse import make_option
import pickle
from django.conf import settings
from django.utils.importlib import import_module
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    '''
    Позволяет запускать сервер дизайнера командой manage.py runide
    В INSTALLED_APPS приложения должно быть m3.Scontrib.designer
    Пример добавления опции запуска
    make_option('--noreload', action='store_false', dest='use_reloader', default=True,
                help='Tells Django to NOT use the auto-reloader.'),
    '''

    # Подсказка        
    help = u'Запускает сервер для дизайнера'

    # Список опции для запуска
    option_list = BaseCommand.option_list + (
    )

    def handle(self, addrport='', *args, **options):
        '''
        Обработчик запуска команды: python manage.py <<command>>
        '''
        
        # Устанавливаем в переменную среды путь до проекта, откуда запущена runide
        os.putenv('PROJECT_FOR_DESIGNER', settings.PROJECT_ROOT)

        try:
            version = import_module('version')
            requires = {
                'requires' : version.__require__,
                'requires_local' : version.__require_local__
            }

            serialized = pickle.dumps(requires)
            os.putenv('PROJECT_FOR_DESIGNER_DEPENDENCY', serialized)

        except ImportError:
            self.stdout.write('version.py is not located in project folder')

        self.stdout.write('M3 Designer IDE starting... \n')
        
        # Путь до сервера дизайнера
        cwd = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        print cwd
        def_port = '7777'
        def_ip = '127.0.0.1'

        if not addrport:
            addr = def_ip
            port = def_port
        else:
            try:
                addr, port = addrport.split(':')
            except ValueError:
                addr, port = def_ip, addrport

        if not port.isdigit():
            raise CommandError("%r is not a valid port number." % port)
        print addr, int(port)
        popen = subprocess.Popen(
                    'python manage.py runserver ' + ':'.join([addr, port]),
                    shell = True,
                    cwd = cwd)

        popen.wait()