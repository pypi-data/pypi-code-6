import os
import sys

path = '/srv/www/d1_gazetteer/application/'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'd1_gazetteer.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()


