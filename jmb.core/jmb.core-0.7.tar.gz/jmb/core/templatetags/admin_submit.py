# -*- coding: utf-8 -*-
"""
.. _admin_submit:

Submit Row Improved
===================

We have created a new tag used in change_form and add_form,
that replace Django’s standard  submit_row.

This is necessary to have 'save and continue'
and 'save as' button in popup change and add form
since by default  Django limits popup form,
removing ``sav_as`` and ``save_and_continue`` button.

In order to have 'save as' button, you need set ``save_as`` attribute in
modelAdmin as usual.

'save and continue' button is enabled bydefault

This submit row is compatible with ajax inlines system
"""


from django.contrib.admin.util import quote
from django import template
from jmb.core.middleware.thread_local import get_request
register = template.Library()

'''
for compatibilty for django <1.5
'''
@register.filter
def admin_urlquote(value):
    return quote(value)
    
@register.inclusion_tag('admin/submit_line2.html', takes_context=True)
def submit_row2(context):
    opts = context['opts']
    change = context['change']
    is_popup = context['is_popup']
    save_as = context['save_as']
    request = get_request()
    is_hjson = request.GET.get("_hjson", False)
    submit_save_name = "_json" if is_hjson else '_save'
    submit_save_continue_name = "_json_continue" if is_hjson else '_continue'
    
    ctx = {
        'opts': opts,
        'show_delete_link': (not is_popup and context['has_delete_permission']
                              and change and context.get('show_delete', True)),
        'show_save_as_new':  change and save_as,
        'show_save_and_add_another': context['has_add_permission'] and
                            not is_popup and (not save_as or context['add']),
        'show_save_and_continue': (context['has_change_permission'] and is_hjson)
                                    or (context['has_change_permission'] and not is_popup),
        'is_popup': is_popup,
        'is_hjson': is_hjson,
        'show_save': True,
        'submit_save_name': submit_save_name,
        'submit_save_continue_name': submit_save_continue_name
    }
    try:
        ctx['onclick_attrib'] =  (opts.get_ordered_objects() and change
                                  and 'onclick="submitOrderForm();"' or '')
    except AttributeError:
        ## Django 1.6 does not have this parameter anymore
        pass
    if context.get('original') is not None:
        ctx['original'] = context['original']
    return ctx
