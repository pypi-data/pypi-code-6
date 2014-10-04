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
    INSTALLED_APPS=['robots'],
    ROOT_URLCONF='robots.urls',
    )


def runtests():
    import django
    import django.test.utils

    if hasattr(django, 'setup'):
        django.setup()

    runner_class = django.test.utils.get_runner(settings)
    test_runner = runner_class(verbosity=1, interactive=True)
    failures = test_runner.run_tests(['robots'])
    sys.exit(failures)
