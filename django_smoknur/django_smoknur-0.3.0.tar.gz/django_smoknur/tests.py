# coding: utf-8

"""
модуль базового теста
"""

import json
import os

from django.conf import settings
from django.db.models import get_apps
from django.test import TransactionTestCase

ERROR_TEXT = u'line={0}, file={1}, url={2}, post_params={3}'
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
                for index, line in enumerate(f_dbg, 1):
                    if not line.startswith('#'):
                        req = json.loads(line)

                        try:
                            resp = self.client.post(
                                req['url'],
                                req['params']
                            )
                        except:
                            print ERROR_TEXT.format(
                                index,
                                f,
                                req['url'],
                                req['params'])
                            raise

                        self.assertTrue(
                            resp.status_code in (200, 302),
                            ERROR_TEXT.format(
                                index,
                                f,
                                req['url'],
                                req['params']))

exclude_apps = getattr(settings, 'SMOKNUR_EXCLUDE_APPS', ())

# добавляем в глобал тесткейсы
for app in get_apps():

    if app.__package__ in exclude_apps:
        continue

    path = os.path.join(
        os.path.dirname(app.__file__),
        'smoknur')

    if os.path.exists(path):

        test_name = app.__package__.replace('.', '_').upper()
        
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
