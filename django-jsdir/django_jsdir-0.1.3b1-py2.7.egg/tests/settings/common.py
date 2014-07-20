import tempfile

# DEBUG is set afterwards in the test's setUp method as Django's testrunner
# initialisation sets it automatically to False

DATABASES = {
    'default': {
        'NAME': 'jsdir',
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

INSTALLED_APPS = (
    'django.contrib.staticfiles',
    'jsdir',
    'tests',
)

STATIC_URL = '/static/'
STATIC_ROOT = tempfile.mkdtemp('_jsdir')
