#!/user/bin/env python

import sys

try:
    import django
    print('Django version: {}'.format(django.VERSION))
except ImportError:
    print("Error: missing test dependency:")
    print("  django library is needed to run test suite")
    print("  you can install it with 'pip install django'")
    print("  or use tox to automatically handle test dependencies")
    sys.exit(1)

from django.conf import settings

settings.configure(
    INSTALLED_APPS=[
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sitemaps',
        'qanda',
        'qanda.tests',
        ],
    # Django replaces this, but it still wants it. *shrugs*
    DATABASE_ENGINE='django.db.backends.sqlite3',
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
            }
        },
    MEDIA_ROOT='/tmp/qanda_test_media/',
    MEDIA_PATH='/media/',
    ROOT_URLCONF='qanda.tests.urls',
    DEBUG=True,
    TEMPLATE_DEBUG=True,
    MIDDLEWARE_CLASSES=[
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        ],
    USE_TZ=True,
    TIME_ZONE='UTC'
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
    test_runner = runner_class(verbosity=2, interactive=True)
    failures = test_runner.run_tests(['qanda'])
    sys.exit(failures)
