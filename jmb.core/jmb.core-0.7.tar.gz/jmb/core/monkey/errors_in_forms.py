"""
.. _monkey-errors:

Errors in forms
================

When running the development server, print in the console which errors have been 
raised when saveing an object. This in necessary when not all fields are used
in a form and Django just says "Fix errors below"

This will work if you have a variable called RUNNING_DEVSERVER that can be 
initialized as follows::

  import sys
  try:
     RUNNING_DEVSERVER = (sys.argv[1] == 'runserver')
  except KeyError:
     RUNNING_DEVSERVER = False

"""


from django.conf import settings 
from django import forms
from django.utils import six
from django.contrib.admin import helpers

class AdminErrorList(forms.util.ErrorList):
    """
    Stores all errors for the form/formsets in an add/change stage view.
    """
    def __init__(self, form, inline_formsets):
        if form.is_bound:
            print "FORM_ERRORS", form.errors
            self.extend(list(six.itervalues(form.errors)))
            for inline_formset in inline_formsets:
                self.extend(inline_formset.non_form_errors())
                for errors_in_inline_form in inline_formset.errors:
                    self.extend(list(six.itervalues(errors_in_inline_form)))

def fix_error_list():

    if getattr(settings, 'RUNNING_DEVSERVER', False):
        helpers.AdminErrorList = AdminErrorList

