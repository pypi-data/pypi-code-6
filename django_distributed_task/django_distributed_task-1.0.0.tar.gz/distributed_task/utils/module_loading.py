from django.utils import six
from importlib import import_module
import sys


def import_string(dotted_path):
    """
    This is copied from Django framework 1.7 to keep backward compatibility.
    Source: https://github.com/django/django/blob/master/django/utils/module_loading.py

    Code is owned by their respective owners.
    """
    try:
        module_path, class_name = dotted_path.rsplit('.', 1)
    except ValueError:
        msg = "%s doesn't look like a module path" % dotted_path
        six.reraise(ImportError, ImportError(msg), sys.exc_info()[2])

    module = import_module(module_path)

    try:
        return getattr(module, class_name)
    except AttributeError:
        msg = 'Module "%s" does not define a "%s" attribute/class' % (
            dotted_path, class_name)
        six.reraise(ImportError, ImportError(msg), sys.exc_info()[2])