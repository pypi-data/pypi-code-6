import sys
from django.conf import settings

if not settings.configured:
    settings.configure(
        DATABASES = {'default' : {'ENGINE' : 'sqlite3'}},
        NOSE_ARGS = ['--failed', '--stop', '--ipdb-failure', '-x'],
        TEST_RUNNER = 'django_nose.NoseTestSuiteRunner',  
        INSTALLED_APPS = [
            'jmb_default_prj',
            'django_nose',
        ],
    )
 
from django.test.simple import run_tests
 
def runtests():
    return
    failures = run_tests(('jmb.core',), verbosity=1, interactive=True)
    sys.exit(failures)
 
if __name__ == '__main__':
    runtests()
