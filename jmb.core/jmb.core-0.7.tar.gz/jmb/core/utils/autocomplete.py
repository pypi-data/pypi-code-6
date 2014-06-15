# coding: utf-8

"""

===============
Autocompletion
===============

Autocompletion is obtained throught autocomplete_light_ package.

A :ref:`patch is applied <monkey-autocomplete>` to the js code of the widget
to add the capability of filtering in a dynamic way, i.e. passing to the
function also the id of other elements in the page that have already being
selected.

.. _dynamic-autocompletion:

Dynamic Autocompletion
=======================

This module provides :class:`DynamicAutocompleteModelBase` a class that
inherits from ``autocomplete_light.AutocompleteModelBase``.

You can define a dictionary called ``filters`` whose keys are queryset filter 
keywords and whose values are dom id. The js widget will retrieve the values 
of the ids and send them along with the string used in the autocompletion
Foregin Key Examples::

    from jmb.core.utils.autocomplete import DynamicAutocompleteModelBase

    class MyAutocomplete(DynamicAutocompleteModelBase):
        filters = {
             'organization_id' : '#id_organization',
             'project_id'  : '#id_project',
        }

M2M examples::

    from jmb.core.utils.autocomplete import DynamicAutocompleteModelBase

    class MyAutocomplete(DynamicAutocompleteModelBase):
        filters = {
             'organizations' : '#id_organization',
             'projects'  : '#id_project',
        }

In TabularInline case, StackedInline and similar, you can't set the id of field, but use this syntax::

    filters = {
         'corporate_id' : '#id_car_details-x-corporate',
         'brand_id' : '#id_car_details-x-brand',
         'model_id' : '#id_car_details-x-model'
    }


In this situation the widget will call the url::

    /ticket/autocomplete/MyAutocomplete/?q=san&organization_id=1530&project_id=10

that will be handled automatically by ``choices_for_request``

To have the complete list of all choice set minimum_characters to 0 in autocomplete_js_attributes
dictionary, example::
    
    class CustomerContactAutocomplete(ContactAutocomplete):
        model = Contact
        filters = {
            'organization_id' : '#id_organization',
        }
        autocomplete_js_attributes = { 
            'minimum_characters': 0, 
        }

.. autoclass:: DynamicAutocompleteModelBase
   :members: filters, choices_for_request, get_filters

.. _autocomplete_light: http://django-autocomplete-light.readthedocs.org/en/latest/

"""
import autocomplete_light

class DynamicAutocompleteModelBase(autocomplete_light.AutocompleteModelBase):
    #: a dict. *Keys* must be keywords to filter a quesryset, e.g.: organization_id, 
    #: organization__address__country_id, and the *values* must be id in the html page
    #: whose value will be retrieved by javascript and sent along (e.g.: #organization_id)
    filters = {
        # 'organization_id' : '#id_organization',
    }
    def __init__(self, *args, **kw):

        self.autocomplete_js_attributes['filter_by'] = "||".join(
            ["%s|%s" % (key, val)  for key, val in self.filters.iteritems()])
        super(DynamicAutocompleteModelBase, self).__init__(*args, **kw)
        

    def choices_for_request(self):
        """Return all choices taking into account all dynamic filters

        you may need to customize this 
        """
        self.choices = self.model.objects.all()
        filters = self.get_filters()
        self.choices = self.choices.filter(**filters)

        return super(DynamicAutocompleteModelBase, self).choices_for_request()

    def get_filters(self):
        "Return  a dictionary suitable to filter self.choices using self.filters"
        filters = {}
        for key in self.filters:
            value = self.request.GET.get(key, '')
            if value:
                filters[key] = value
        return filters

