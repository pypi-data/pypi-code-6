"""
Jumbo relies on some patches to the official django version that can be applied using the 
function :func:`jmb.core.monkey.patch` in ``settings/__init__.py``::

   # place these lines after any other code!!!
   from jmb.core import monkey
   monkey.patch()


.. autofunction:: patch

.. automodule:: jmb.core.monkey.management

.. automodule:: jmb.core.monkey.conf

.. automodule:: jmb.core.monkey.errors_in_forms


.. _timepicker_patch:

timepicker
==========

Datetime and time widgets in Django are pretty poor ones.

Html widgets used by admin are defined in ``django.contrib.admin.options`` 
in a dict named ``FORMFIELD_FOR_DBFIELD_DEFAULTS``.

We overwrite it in ``jmb.core.admin.options`` and define a widget that is
derived from ``jQuery.ui``'s default one.

.. _monkey-autocomplete:

autocomplete_light
===================

A monkey patch vs autocomplete_light (rel 1.4.9) is applied from within our
``change_form.html`` so that :ref:`dynamic-autocompletion` capabilities are added
to standard autocomplete_light.

It's called from *extrahead block*.


"""
from django.conf import settings

from .management import fix_find_namespaces
from .conf import patch_cms_page_not_to_overwrite_jquery
from .errors_in_forms import fix_error_list

MONKEY_PATCHES = ['namespaces', 'widgets', 'jquery', 'form_errors']

def patch_widgets_mapping():
    """
    Modify options.FORMFIELD_FOR_DBFIELD_DEFAULTS to use :ref:`timepicker`
    """

    from jmb.core.forms import widgets
    from django.contrib.admin import options
    from django.db import models

    options.FORMFIELD_FOR_DBFIELD_DEFAULTS[models.DateTimeField] = {
        'widget': widgets.DateTimePicker}
    options.FORMFIELD_FOR_DBFIELD_DEFAULTS[models.TimeField] = {
        'widget': widgets.TimePicker}
    options.FORMFIELD_FOR_DBFIELD_DEFAULTS[models.DateField] = {
        'widget': widgets.DatePicker}


def patch(exclude=None):
    """
    Apply all patches Jumbo relyes on. Currently :ref:`namespaces`, :ref:`jquery <jquery_cms>`,
    and :ref:`timepicker <timepicker_patch>`

    :arg exclude: a list of strings naming the patches that will not be applied.
       'jquery' patch will only be applied if ``cms`` is in ``INSTALLED_APPS``
    """
    global MONKEY_PATCHES  # non dovrebbe essere necessaria...

    MONKEY_PATCHES = [item for item in MONKEY_PATCHES if not item in (exclude or [])]
    for item in MONKEY_PATCHES:
        if item == 'namespaces':
            fix_find_namespaces()
        if item == 'widgets':
            patch_widgets_mapping()
        if item == 'jquery' and 'cms' in settings.INSTALLED_APPS:
            patch_cms_page_not_to_overwrite_jquery()
        if item == 'form_errors':
            fix_error_list()
