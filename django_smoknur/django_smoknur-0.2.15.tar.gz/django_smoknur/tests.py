# coding: utf-8

"""
модуль базового теста
"""

import json
import os

from django.conf import settings
from django.test import TransactionTestCase


def test_runner(self):
    """smoke test"""

    # авторизуем пользователя
    if (hasattr(settings, 'SMOKNUR_USERNAME') 
        and hasattr(settings, 'SMOKNUR_PASSWORD')):
        self.assertTrue(
            self.client.login(
                username=settings.SMOKNUR_USERNAME,
                password=settings.SMOKNUR_PASSWORD))

    # отправляем пост запросы
    for f in sorted(os.listdir(self.smoknur_path)):
        if f.endswith('.dbg'):
            with open(os.path.join(self.smoknur_path, f)) as f_dbg:
                for line in f_dbg:
                    if not line.startswith('#'):
                        req = json.loads(line)
                        print req['url'], req['params']
                        resp = self.client.post(
                            req['url'],
                            req['params']
                        )
                        self.assertTrue(
                            resp.status_code in (200, 302))

# нужно так, чтобы не было задвоение имени приложения в пути, src/epk/epk/core
root_path = settings.PROJECT_ROOT.rsplit('/', 1)[0]

# добавляем в глобал тесткейсы
for app in settings.PROJECT_APPS:

    # формируем путь к папкам с тестами по приложениям
    paths = [root_path]
    paths.extend(app.split('.'))
    paths.append('smoknur')

    path = os.path.join(*paths)

    if os.path.exists(path):

        test_name = app.replace('.', '_').upper()
        
        attrs = {
            'fixtures': [],
            'smoknur_path': path,
            'test': test_runner,
            'reset_sequences': True
        }
        for file_ in sorted(os.listdir(path)):
            if file_.endswith('.json'):
                attrs['fixtures'].append(os.path.join(path, file_))

        globals()[test_name] = type(
            test_name, 
            (TransactionTestCase, ), 
            attrs)    
