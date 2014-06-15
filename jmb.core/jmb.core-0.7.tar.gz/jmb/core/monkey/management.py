"""
.. _namespaces:

management commands
===================

Django ``find_management_module`` fails at finding modules when namespaces are used.

This version of ``find_management_module`` tries a real ``import`` when
django fails to find the module. The difference is that django only uses::

  imp.find_module(...)

that doesn't implement full module search algorithm.
We're going to place this code in :file:`settings/__init__.py, the older
way to place it in :file:`urls.py` doesn't work as is not found when calling
from command line as :file:`urls.py` is not called::

  from jmb.core import monkey
  monkey.patch()

At the moment there's an open ticket_

.. _ticket: https://code.djangoproject.com/ticket/14087



"""
import os
import imp


def find_management_module(app_name):
    """
    Determines the path to the management module for the given app_name,
    without actually importing the application or the management module.

    Raises ImportError if the management module cannot be found for any reason.
    """
    parts = app_name.split('.')
    parts.append('management')
    parts.reverse()
    part = parts.pop()
    path = None

    # When using manage.py, the project module is added to the path,
    # loaded, then removed from the path. This means that
    # testproject.testapp.models can be loaded in future, even if
    # testproject isn't in the path. When looking for the management
    # module, we need look for the case where the project name is part
    # of the app_name but the project directory itself isn't on the path.
    try:
        f, path, descr = imp.find_module(part, path)
    except ImportError as e:
        if os.path.basename(os.getcwd()) != part:
            raise e
    else:
        if f:
            f.close()

    while parts:
        part = parts.pop()

        try:
            f, path, descr = imp.find_module(part, path and [path] or None)
            if f:
                f.close()
        ## This par added by sandro
        except ImportError:
            if len(app_name.split('.')) >= 2:
                mod = __import__(app_name + '.management', {}, {}, [''], -1)
                return mod.__path__[0]
    return path


def fix_find_namespaces():
    from django.core import management

    management.find_management_module = find_management_module
