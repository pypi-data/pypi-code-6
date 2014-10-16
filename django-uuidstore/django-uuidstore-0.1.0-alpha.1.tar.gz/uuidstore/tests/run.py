"""
Test support harness to make setup.py test work.
"""

import sys
from django.conf import settings

settings.configure(
    DATABASES={
        'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory;'}
        },
    MIDDLEWARE_CLASSES=(
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        ),
    INSTALLED_APPS=[
        'django.contrib.contenttypes',
        'uuidstore.tests',  # Because we have models to use!
        'uuidstore',
        ],
    ROOT_URLCONF='uuidstore.tests.urls',
    USE_TZ = True
    )


def runtests():
    import django
    import django.test.utils

    print('# runtests: Django version: {}'.format(django.VERSION))

    if django.VERSION[:2] < (1, 6):
        print('# runtests: Using DiscoverRunner')
        settings.INSTALLED_APPS.append('discover_runner')
        settings.TEST_RUNNER = 'discover_runner.DiscoverRunner'

    if hasattr(django, 'setup'):
        django.setup()

    runner_class = django.test.utils.get_runner(settings)
    test_runner = runner_class(verbosity=1, interactive=True)
    failures = test_runner.run_tests(['uuidstore'])
    sys.exit(failures)
