import functools
from django.template.loader import render_to_string
from django.conf import settings


def lazy_admin_column(*args, **kwargs):
    """
    A decorator for a custom change list column method of an admin class.
    You can optionally specify a template for the content to be displayed initially.

    The decorator can be invoked with or without parameters
    """
    no_params = False

    template = kwargs.get('template', 'lazy_admin/lazy_column.html')

    if (len(args) == 1) and (len(kwargs) == 0):
        if callable(args[0]):
            no_params = True
        else:
            template = args[0]

    def _dec(fn):

        @functools.wraps(fn)
        def wrapper(admin, obj, delay=True):
            # We have a settings based kill switch as well turning off all
            # lazy load columns.
            if obj and obj.pk and delay and getattr(settings, 'LAZY_ADMIN_ALLOW', True):
                klass = obj.__class__
                return render_to_string(template, {'app_name': klass._meta.app_label,
                                                    'class_name': klass.__name__,
                                                    'func_name': fn.__name__,
                                                    'obj_id': obj.pk})
            return fn(admin, obj)

        wrapper.allow_tags = True  # We need HTML output for the column
        return wrapper

    # Called directly as @lazy_admin_column ?
    if no_params:
        return _dec(args[0])

    # Called as @lazy_admin_column(template='something') ?
    return _dec
