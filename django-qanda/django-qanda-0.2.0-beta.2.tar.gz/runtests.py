#!/user/bin/env python

import sys

try:
    import django
except ImportError:
    print("Error: missing test dependency:")
    print("  django library is needed to run test suite")
    print("  you can install it with 'pip install django'")
    print("  or use tox to automatically handle test dependencies")
    sys.exit(1)

from django.conf import settings


def main():
    settings.configure(
        INSTALLED_APPS=[
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.sitemaps',
            'qanda',
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
            'django.middleware.clickjacking.XFrameOptionsMiddleware',
            ]
        )

    if django.VERSION[:2] >= (1, 7):
        django.setup()

    apps = ['qanda']
    # if django.VERSION[:2] >= (1, 6):
    #    apps.append('qanda.tests')

    from django.core.management import call_command
    from django.test.utils import get_runner

    try:
        from django.contrib.auth import get_user_model
    except ImportError:
        USERNAME_FIELD = 'username'
    else:
        USERNAME_FIELD = get_user_model().USERNAME_FIELD

    DjangoTestRunner = get_runner(settings)

    class TestRunner(DjangoTestRunner):
        def setup_databases(self, *args, **kwargs):
            result = super(TestRunner, self).setup_databases(*args, **kwargs)
            kwargs = {
                'interactive': False,
                'email': 'admin@doesnotexit.com',
                USERNAME_FIELD: 'admin',
                }
            call_command("createsuperuser", **kwargs)
            return result

    failures = TestRunner(verbosity=2, interactive=True).run_tests(apps)
    sys.exit(failures)
