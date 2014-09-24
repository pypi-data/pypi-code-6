#coding:utf-8
#!/usr/bin/env python

# Добавляем путь до django
import sys
import os


source_project_path = os.getenv('PROJECT_FOR_DESIGNER', None)
if source_project_path is not None:
    sys.path.insert(0, os.path.join(source_project_path, '../env'))

project_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join( project_path, '../env'  ))

from django.core.management import execute_manager
try:
    import settings # Assumed to be in the same directory.
except ImportError:
    import sys
    sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n(If the file settings.py does indeed exist, it's causing an ImportError somehow.)\n" % __file__)
    sys.exit(1)

if __name__ == "__main__":
    execute_manager(settings)
