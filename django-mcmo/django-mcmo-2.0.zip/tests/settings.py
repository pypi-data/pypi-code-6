DEBUG = True
SECRET_KEY = 'secret'

DATABASES = {
    'default': {
        'NAME': 'django_mcmo',
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

INSTALLED_APPS = ['mcmo',
                  'django_nose']

MIDDLEWARE_CLASSES = ()  # Django 1.7 needs that to be happy :)

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
