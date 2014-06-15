# -*- coding: utf-8 -*-
"""
.. _admin_tabs:

Admin Tabs in change form
=========================


A templatetag to create a tabbed layout in a change_form.
It looks in ModelAdmin for method :ref:`get_tabs`. 

that means you can just set :attr:`tabs` in you ModelAdmin.


Tabs is a tuple of tuples. An example of a hypothetical 
Company model whose Inlines are ``Contacts`` and ``Banks``::

  tabs = (
    (_('Company'), {'items': [_('general_info')]}),
    (_('Contacts'), {'items': [Contact, ], 'active': True}),
    (_('Addresses'), {'items': [AddressInline, Banks], 'active': True}),
    (_('Banks'), {'items': [BankInline], 'active': True}),
  )

.. image:: ../../images/admin_tabs.png
   :align: right

Resulting in 4 tabs with labels  as shown in the figure. 
Each element of tabs is a tuple composed of:

* a label

* a list of elements (possibly empty). Each element can be eather a

  * :string: that will be interpreted as the name of a fieldset declared in
      fieldsets 

  * :(django) Inline: whose inline must be declared in the standard way. 
      (In this case a models can also be used)

  * :AjaxInline: whose inline must be declared as defined ref:`here <ajax_inline>`

  * :empty list: the first one that is left as an
       empty **list** will be filled with all fieldsets as in::

        (_('Author'), {}),

This grants the ability to place all peaces in any fancy way

.. _get_tabs:

get_tabs
--------

The signature if function :func:`get_tabs` is as follows::

  def get_tabs(self, request, obj):
     return self.tabs

.. note:: to use ``get_tabs`` returning different tabs depending on 
   obj requires you also create inlines with the same logic.

   That means you have at least django 1.5 when kw ``obj`` was added to 
   ``get_inline_instances``!!

Note that if your ``get_tabs`` changes the number of Inlines used you need to 
prepare a similar ``get_inline_instances`` that must on turn call super as in::

    def get_tabs(self, request, obj=None):
        if obj and obj.id:
            tabs = self.tabs
        else:
            tabs = (
                ('Contratto' , {}),
                )
        return tabs

    def get_inline_instances(self, request, obj=None):
 
        if obj and obj.id:
            self.inlines = self.inlines
        else:
            self.inlines = []
        return super(self.__class__, self).get_inline_instances(request, obj)
        

"""
import inspect
from copy import deepcopy

from django.template import Library
from django.db.models import Model

from jmb.core.admin.ajax_inlines import AjaxInline

register = Library()

class Tab(object):

    def __init__(self, name, info, adminform, obj, inline_admin_formsets, idx):
        self.name = name
        self.obj = obj
        self.inline_admin_formsets = inline_admin_formsets
        self.adminform = adminform
        self.items = [Item(item, self) for item in info.get('items', [])]
        self.active = info.get('active', False)
        if not self.items and idx == 1:
            if isinstance(self.items, list):
                for formset in adminform:
                    self.items += [Item(formset.name, self)]
        if not obj:
            self.items = [item for item in self.items
                         if not (inspect.isclass(item) and issubclass(item, AjaxInline))
                             ]
    def css(self):
        return 'active' if self.active else ''

    def enabled(self):
        # If a tab contains an ajax_inline and we are in add_view, 
        # tab must be disabled. If tab contains also something else no
        val = bool(self.obj or sum(not item.is_ajax_inline for item in self.items))
        return val

    def __repr__(self):
        return u'<Tab: %s (%r)>' % (self.name, self.items)

class Item(object):
    """
    An item displayed by an admin_tab layout
    """
    #: True if item is a fieldset. If True self.fieldset points to the fieldset
    is_fieldset = False
    #: True if item is a Tabular/Stacked inline. If True, self.formset point to the
    #: formset
    is_django_inliline = True

    def __init__(self, item, tab):

        self.item = item
        self.tab = tab
        self.is_ajax_inline = inspect.isclass(item) and issubclass(item, AjaxInline)
        self.is_fieldset = isinstance(item, basestring)
        self.is_django_inline = not (self.is_ajax_inline or self.is_fieldset)

        if self.is_fieldset:
            self.fieldset = self.get_fieldset_by_name(item, tab.adminform)

        if self.is_django_inline:
            if issubclass(self.item, Model):
                self.formset = self.get_inline_formset_by_model(tab.inline_admin_formsets, item)
            else:
                self.formset = self.get_inline_formset_by_model(tab.inline_admin_formsets, item.model)

    def get_fieldset_by_name(self, name, adminform):
        for fieldset in adminform:
            if fieldset.name == name:
                return fieldset
        
    def get_inline_formset_by_model(self, inline_admin_formsets, model):

        for inline_admin_formset in inline_admin_formsets:
            if inline_admin_formset.opts.model == model:
                return inline_admin_formset

    def render(self):
        if self.is_ajax_inline and self.tab.obj:
            return self.instance.render(self.tab.obj)

    def __repr__(self):
        if self.is_ajax_inline:
            t = "AjI"
        elif self.is_fieldset:
            t = "Fst"
        else:
            t = "DjI"
        return "<%s %s>" % (t, self.item)

@register.inclusion_tag("jmb/admin_tabs.html", takes_context = True)
def create_tabs(context, adminform):

    request = context['request']    
    obj = context.get('original')
    
    if hasattr(adminform.model_admin, 'get_tabs'):
        tabs = adminform.model_admin.get_tabs(request, obj)
    else:
        tabs = getattr(adminform.model_admin, 'tabs', {})

    adminform.has_tabs = bool(tabs)
    inline_admin_formsets = context.get('inline_admin_formsets')

    tabs = manage_tabs(tabs, adminform, request, obj, inline_admin_formsets)

    return {
        'tabs' : tabs,
        'adminform': adminform,
        'original' : obj,
        'inline_admin_formsets': context.get('inline_admin_formsets')
    }

def manage_tabs(tabs, adminform, request, obj, inline_admin_formsets):
    
    model_admin = adminform.model_admin
    if not tabs:
        return tabs
    tabs = deepcopy(tabs) # Item_dict deve essere dereferenziato!!!
    new_tabs = []
    active_tab_exists = False
    idx = 1
    for tab_name, item_dict in tabs:
        tab = Tab(tab_name, item_dict, adminform, obj, inline_admin_formsets, idx)
        idx += 1
        if tab.items or model_admin.tabs_show_empty:
            new_tabs += [tab]
        active_tab_exists = active_tab_exists or tab.active

    if not active_tab_exists:
        new_tabs[0].active = True
    
    # Add an instance to be rendered
    for tab in new_tabs:
        for j, item in enumerate(tab.items):
            if inspect.isclass(item.item) and issubclass(item.item, AjaxInline):
                instance = item.item(model_admin.model, model_admin.admin_site, obj)
                instance.set_changelist(request)

                tab.items[j].instance = instance
    return new_tabs


