# -*- coding: utf-8 -*-
"""
.. _oo-create-file:

Utilizzo
========

Un esempio semplice di utilizzo::

  from jmb.core.views.generic.create_oo_file import create_file
  extra_context = {'to_company' : self.get_to_company, }
  str_oofile = create_file(None, file_name=pdf_cover_name, 
                           file_model='admin/fax/fax/cover.odt',
                           file_type="pdf", save_in="/tmp/", extra_context=extra_context)

.. autofunction: create_file
"""

import os
import datetime

from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render_to_response

from jmb.core.utils.ooutils import OOUtils

def create_file(request, model=None, obj_id=None, queryset=None, file_name=None,
                file_model=None, file_type=None, get_raw_string=False, language=None,
                save_in=None, extra_context={}):
    """Return an HttpResponse with an attachment that is the pdf/odt file

    it uses :attr:`OOUtils.save_odt` and :attr:`OOUtils.save_pdf`
    """
    # Creazione di un file OpenOffice
    if obj_id and queryset:
        return render_to_response('jmb/generic_error.html', error=_("Error: ambiguos"))

    if obj_id and not model:
        return render_to_response('jmb/generic_error.html', error=_("Model param is required."))

    if not model and not file_model:
        return render_to_response('jmb/generic_error.html', error=_("File Model param is required if model param is not set."))

    obj = queryset
    if obj_id:
        try:
            obj = model.objects.get(pk=obj_id)
        except model.DoesNotExists:
            return render_to_response('jmb/generic_error.html', error=_("The object does not exists."))
    if not file_type:
        file_type = 'odt'

    if not file_name:
        file_name = "default_name"
        if model:
            file_name = "%s" % (model._meta.object_name.lower())
    if not file_model:
        file_model = "%s/%s.%s" % (model._meta.app_label, model._meta.object_name.lower(), file_type)

    if request and request.GET:
        extra_context.update(request.GET)
    o = OOUtils()
    if file_type == 'odt':
        response = o.save_odt(request, file_model, file_name, obj=obj, get_raw_string=get_raw_string, language=language, save_in=save_in, extra_context=extra_context)
    if file_type == 'ods':
        response = o.save_ods(request, file_model, file_name, obj=obj, get_raw_string=get_raw_string, language=language, save_in=save_in, extra_context=extra_context)
    elif file_type == 'pdf':
        response = o.save_pdf(request, file_model, file_name, obj=obj, get_raw_string=get_raw_string, language=language, save_in=save_in, extra_context=extra_context)
    return response
