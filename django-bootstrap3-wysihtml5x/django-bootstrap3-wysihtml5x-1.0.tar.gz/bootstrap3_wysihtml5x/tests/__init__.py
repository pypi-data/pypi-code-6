#-*- coding: utf-8 -*-

import os
import sys
import unittest

def setup_django_settings():
    os.chdir(os.path.join(os.path.dirname(__file__), ".."))
    sys.path.insert(0, os.getcwd())
    os.environ["DJANGO_SETTINGS_MODULE"] = "tests.settings"


def run_tests():
    if not os.environ.get("DJANGO_SETTINGS_MODULE", False):
        setup_django_settings()

    import django
    django.setup()

    from django.conf import settings
    from django.test.utils import get_runner

    runner = get_runner(settings, "django.test.simple.DjangoTestSuiteRunner")
    test_suite = runner(verbosity=2, interactive=True, failfast=False)
    test_suite.run_tests(["bootstrap3_wysihtml5x"])


def suite():
    if not os.environ.get("DJANGO_SETTINGS_MODULE", False):
        setup_django_settings()
    else:
        from django.db.models.loading import load_app
        from django.conf import settings
        settings.INSTALLED_APPS = list(settings.INSTALLED_APPS) + ['bootstrap3_wysihtml5x.tests']
        map(load_app, settings.INSTALLED_APPS)

    from bootstrap3_wysihtml5x.tests import fields, widgets

    testsuite = unittest.TestSuite([
        unittest.TestLoader().loadTestsFromModule(fields),
        unittest.TestLoader().loadTestsFromModule(widgets),
    ])
    return testsuite


if __name__ == "__main__":
    run_tests()
