import os.path
import sys
import uuid

sys.path = [
    os.path.join(os.path.dirname(__file__), '../../src')
] + sys.path

SECRET_KEY = str(uuid.uuid4())

INSTALLED_APPS = (
    'project.app.en',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'test'
    }
}
