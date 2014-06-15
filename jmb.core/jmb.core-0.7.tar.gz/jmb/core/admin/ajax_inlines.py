# coding: utf-8
""".. _ajax_inline:

AjaxInline
==========

.. image:: ../../images/ajax_inlines.png
   :align: right 

This is a very powerfull way to display children rows of a parent. It's use can be alternative 
to that of TabularInline but differs in many details:

1. Rows can be added only when the parent has already been saved. If you
   want to abort the creation of the father if the children are not created,
   this is not the correct tool.

2. Add/Change/Delete is done via iframe/ajax, that make it fast and 
   user-friendly. On the other hand ``Tabular/StakedInline`` use a single huge form.

3. Any row is displayed using official django result_list templatetag, the same used in
   changelist, the :class:`ChangeList` object used has a modified 
   :meth:`ChangeList.get_query_set` to filter children of a parent. You can customize it or
   simply customize :meth:`AjaxInline.get_queryset` method.

   All fields defined in ``AjaxInline``'s ``list_display`` attribute will be
   treated in the standard way for ``list_display`` on ``ModelForm`` i.e.:
   you can define functions and the like.

4. Layout can only be controlled via tabs

5. You need to register a ModelAdmin separately for the Child Model you want to edit
   See below for :ref:`row-customization`. 

6. DataTable jQuery plugin, take care of presenting data in an effective way, sorting is 
   done locally, searching is done by default on any field.

7. Only one ajax_inline can be registered for each model, that means that 
   you cannot use 2 different ajax_inlines to edit/delete records

To add AjaxInline to your ModelAdmin, resulting in something similar to what
is shown in the figure can be accomplished as follows:

.. code-block:: python

   from django.contrib import admin

   from jmb.core.admin import AjaxInline, ConstrainedModelForm, register_inline
   from jmb.core.admin.options import ExtendibleModelAdmin

   class ContactAjaxInline(AjaxInline):
       model = Contact
       fk_name = 'company'  
       list_display = ('title', 'first_name', 'role','user', )

   class CompanyModelAdmin(ExtendibleModelAdmin):
       ...
       tabs = (
            ('main', {}),
            ('contacts', {'items' : [ContactAjaxInline]}),
            ...
       )

    class ContactForm(ConstrainedModelForm):
       class Meta:
           model = Contact      
       hidden_fields = ('organization',) # ALTERNATIVELY you can use get_form below

    class ContactModelAdmin(ExtendibleModelAdmin):
       model = Contact
       # form = ContactForm
       def get_form(self, request, obj=None, **kwargs):
           '''
           Return a form that forces all fields in the GET as not changeable
           '''
           # Alternative to declaring hidden_fields in the ConstraintForm
           hidden_fields = [key for key in request.GET.keys() if not key.startswith('_')]
           name = "%sForm" % self.model.__name__

           return type(name, (ContactForm,), {
               'hidden_fields' : hidden_fields,
           })



    register_inline(ContactAjaxInline)
    admin.site.register(Contact, ContactModelAdmin)
    admin.site.register(Company, CompanyModelAdmin)


You need to use :class:`ConstrainedModelForm` to make sure foreign keys to 
the parent are not writeble

.. _row-customization:

Row customization
===================

``ajax_inline.html`` uses Django's ``result_list`` templatetag to render
the single object, so any standard way to customize the changelist can be used:
field_names in ``list_display`` can be functions defined on the ModelAdmin or 
on the model as described in django documentation.

When you add/modify a record you use the standard ModleAdmin called in an
iframe. After saving the obj the object itself is rendered in the same
way it would be in the chagelist, that implies you need to register which
AjaxInlines will be used so that redsponse_add/change can use it. This is
solved by registering the inlines via :func:`register_inline`

ConstraintForm
==============

When editing an inline you want to hide the foreign_key field: it simply isn't 
usefull and you want to prevent the used to change it. But it must be present in 
the form as HiddenField as it's needed when saving the record.

You can use set the widget to Hidden using a :class:`CostrainedForm` and declaring 
it as hidden in the class. If you plan to use the same form both as AjaxInlien and 
in a standard change_form, you can set hidden fields dinamically as shown in 
the example above

API
===

.. autoclass:: AjaxParentModelAdmin
   :members:

.. autoclass:: ConstrainedModelForm
   :members:

.. autoclass:: ChildrenChangeList
   :members:

.. autoclass:: AjaxInline
   :members:

"""

import re
import json

from django.utils.safestring import mark_safe
from django import forms
from django.contrib.admin import site
from django.db.models import ForeignKey
from django.contrib.admin import options
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.template.response import SimpleTemplateResponse
from django.template import Context, Template, loader
from django.template.loader import get_template
from django_filters.admin.options import AdvancedSearchModelAdmin
from django.contrib.admin.views.main import ChangeList
from django.forms.models import _get_foreign_key
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext as ugt
from django.contrib.admin.util import unquote, get_deleted_objects
from django.db import models, transaction, router
from django.utils.encoding import force_text
from pyquery import PyQuery as pq
from django.conf import settings

from jmb.core.middleware.thread_local import get_request

inlines_registry = {}

def register_inline(inline):
    "Register an Inline for a specific model"
    inlines_registry[inline.model] = inline

class ConfigurationError(Exception): pass

class AjaxParentModelAdmin(AdvancedSearchModelAdmin):
    """
    A ModelAdmin that provides handling for ``_hjson`` parameter that
    returns the object formatted according to a registered AjaxInline
    """
    

    def response_add(self, request, obj, post_url_continue=None):
        if  "_hjson" in request.GET:
            method = ""
            method = '_json_continue' if  request.POST.get("_json_continue", False) else method
            method = '_json' if  request.POST.get("_json", False) else method
            method = '_saveasnew' if  request.POST.get("_saveasnew", False) else method
            method = '_addanother' if  request.POST.get("_addanother", False) else method
            opts = obj._meta
            msg_dict = {'name': force_text(opts.verbose_name), 'obj': force_text(obj)}
            message = _('The %(name)s "%(obj)s" was added successfully.') % msg_dict
            inline = inlines_registry[self.model](admin_site=self.admin_site)
            inline.set_changelist(request, obj)
            html = inline.render_row(obj)
            pk_value = obj._get_pk_val()
            serialized = {'model': "", "pk": pk_value, "fields": html }
            return SimpleTemplateResponse('jmb/iframe.html', { 
                'action': 'add',
                'method': method,
                'message': message,
                'json': json.dumps([serialized])
            })
        return super(AjaxParentModelAdmin, self).response_add(request, obj, post_url_continue)
    
    def response_change(self, request, obj):

        if  "_hjson" in request.GET:
            method = ""
            method = '_json_continue' if  request.POST.get("_json_continue", False) else method
            method = '_json' if  request.POST.get("_json", False) else method
            method = '_saveasnew' if  request.POST.get("_saveasnew", False) else method
            method = '_addanother' if  request.POST.get("_addanother", False) else method
            opts = obj._meta
            msg_dict = {'name': force_text(opts.verbose_name), 'obj': force_text(obj)}
            message = _('The %(name)s "%(obj)s" was changed successfully.') % msg_dict
            

            if "origin=change-list" in request.META['HTTP_REFERER']:
                model_admin = self.admin_site._registry[self.model]
                kw = dict(model=self.model, list_display=self.list_display, single_child = obj,
                list_display_links=self.list_display_links, list_filter=None, 
                date_hierarchy=None, search_fields=(), list_select_related=True,
                list_per_page=self.list_per_page, list_max_show_all=self.list_max_show_all, 
                      list_editable=None, model_admin=model_admin, ajax_inline=model_admin)
                self.cl = ChildrenChangeList(request, model_admin, **kw)
                self.cl.ajax_inline = model_admin
                opts = self.model._meta
                app_label = opts.app_label
                template_list = [
                    "admin/%s/%s/%s" % (app_label, opts.object_name.lower(), 'ajax_inline.html'),
                    "admin/%s/%s" % (app_label, 'ajax_inline.html'),
                    "admin/%s" % 'ajax_inline.html',
                ]
                context = {
                    'ajax_inline' : self,
                }
                t = loader.select_template(template_list)
                table = loader.render_to_string(template_list, context) 
                html = table
                d = pq(html)
                html = d('tbody').html()
            else:
                inline = inlines_registry[self.model](admin_site=self.admin_site)
                inline.set_changelist(request, obj)
                html = inline.render_row(obj)
                
            pk_value = obj._get_pk_val()
            serialized = {'model': "", "pk": pk_value, "fields": html }
            return SimpleTemplateResponse('jmb/iframe.html', {
                'action': 'change',
                'message': message,
                'method': method,
                'json': json.dumps([serialized])
            })
        return super(AjaxParentModelAdmin, self).response_change(request, obj)

    def delete_view(self, request, object_id, extra_context=None):
        "The 'delete' admin view for this model."

        extra_context = (extra_context or {})
        extra_context.update({
             'is_popup': "_popup" in request.REQUEST,})
    
        # The user has already confirmed the deletion.
        if not request.POST or not ("_hjson" in request.GET): 
            return super(AjaxParentModelAdmin, self).delete_view(
                request, object_id, extra_context)

        opts = self.model._meta
        app_label = opts.app_label

        obj = self.get_object(request, unquote(object_id))

        if not self.has_delete_permission(request, obj):
            raise PermissionDenied

        if obj is None:
            raise Http404(_('%(name)s object with primary key %(key)r does not exist.') % {'name': force_text(opts.verbose_name), 'key': escape(object_id)})

        using = router.db_for_write(self.model)

        # Populate deleted_objects, a data structure of all related objects that
        # will also be deleted.
        (deleted_objects, perms_needed, protected) = get_deleted_objects(
            [obj], opts, request.user, self.admin_site, using)

        if request.POST: # The user has already confirmed the deletion.
            if perms_needed:
                raise PermissionDenied
            obj_display = force_text(obj)
            self.log_deletion(request, obj, obj_display)
            self.delete_model(request, obj)

            message = _('The %(name)s "%(obj)s" was deleted successfully.') % {'name': force_text(opts.verbose_name), 'obj': force_text(obj_display)}

            if not self.has_change_permission(request, None):
                return HttpResponseRedirect(reverse('admin:index',
                                                    current_app=self.admin_site.name))

            return SimpleTemplateResponse('jmb/iframe.html', {
                'action': 'delete',
                'message': message
            })
    
    def get_delete_icon(self, obj):
        opts = self.model._meta
        can_be_delete = False
        # Se il modello ha la funzione can_be_modified la chiamo per fare
        # i controlli relativi a quel modello
        if hasattr(obj, "can_be_delete"):
            if obj.can_be_delete():
                can_be_delete = True
        # Se non ce l'ha non faccio controlli e visualizzo l'icona
        else:
            can_be_delete = True

        if can_be_delete:
            param = ""
            if self.use_fancybox:
                param='?_popup=1&nobuttons=1'
            return "<a name='delete' href=%(reverse_url)s%(param)s><img src='%(url)sjmb/images/del.gif' alt='%(window_title)s' title='%(window_title)s'/></a>" % {
                'reverse_url':reverse('admin:%s_%s_delete' % (opts.app_label, opts.object_name.lower()), args=(obj.pk,)),
                'param': param,
                'url':settings.STATIC_URL,
                'window_title':ugt("Delete %s" % opts.object_name.lower())
            }
        return ""
    get_delete_icon.short_description = _("D")
    get_delete_icon.allow_tags = True

    def get_edit_icon(self, obj, querystring=''):

        opts = self.model._meta
        can_be_modified = False
        # Se il modello ha la funzione can_be_modified la chiamo per fare
        # i controlli relativi a quel modello
        if hasattr(obj, "can_be_modified"):
            if obj.can_be_modified():
                can_be_modified = True
        # Se non ce l'ha, non faccio controlli e visualizzo l'icona
        else:
            can_be_modified = True

        request = get_request()
        
        if can_be_modified:
            dj_reverse_url = reverse('admin:%s_%s_change' % (opts.app_label, opts.object_name.lower()), args=(obj.pk,))
            if querystring:
                dj_reverse_url += "?%s" % querystring
            return "<a name='edit' href=%(reverse_url)s><img src='%(url)sjmb/images/edit.gif' alt='%(window_title)s' title='%(window_title)s'/></a>" % {
            'reverse_url': "%s" % (dj_reverse_url, ),
            'url':settings.STATIC_URL,
            'window_title':ugt("Edit %s" % opts.object_name.lower())
        }
        return ""
    get_edit_icon.short_description = _("E")
    get_edit_icon.allow_tags = True


    def get_edit_icon_iframe(self, obj):
        # FIXME: this way to get the inline limits to 1 ajax_inline per model!!!

        inline = inlines_registry[self.model](admin_site=self.admin_site)
        querystring = "%s=%s"  % (inline.fk_name, obj.pk)
        txt = self.get_edit_icon(obj, querystring=querystring)
        return re.sub('href=', 'class="iframe hjson edit " width="%s" height="%s" href=' % (
                      inline.width, inline.height), txt)

    get_edit_icon_iframe.short_description = _("E")
    get_edit_icon_iframe.allow_tags = True

    def get_delete_icon_iframe(self, obj):
        txt = self.get_delete_icon(obj)
        return re.sub('href=', 'class="iframe hjson delete" href=', txt)

    get_delete_icon_iframe.short_description = _("X")
    get_delete_icon_iframe.allow_tags = True

class ConstrainedModelForm(forms.ModelForm):
    """A ModelForm that forces HiddenInput on fields declared in :attr:`hidden_fields`
    
    It's main goal is to be used when a child is edited and the parent must be forced 
    without giving the user the opportunity to alter it.

    It's :meth:`__init__` calls hide_field() for any field declared in
    :attr:`hidden_fields`.  If you need to implement more logic in your
    ``__init__`` you can simply call :meth:`hide_field` by youself.

    We use it along with a javascript code (``jmb.hide_input()``) that hide the
    label of the relative fields called from within ``change_form.html``

    """
    hidden_fields = ()

    def __init__(self, *args, **kwargs):
        super(ConstrainedModelForm, self).__init__(*args, **kwargs)

        for field_name in self.hidden_fields:
            self.hide_field(field_name)
    
    def hide_field(self, field_name):
        if self.initial.get(field_name, False):
            hidden_id = self.initial.get(field_name, False)
            
        if  self.data.get(field_name, False):
            contratto_id = self.data.get(field_name, False)
        
        if field_name:
            field = self.Meta.model._meta.get_field_by_name(field_name)[0]
            if not isinstance(field, ForeignKey):
                return
                # msg = ("Hiding only implemented for ForeignKey (here: %s)" % field_name)
                # return NotImplementedError(msg)

            related_model = field.rel.get_related_field().model
            self.fields[field_name]  = forms.ModelChoiceField(
                queryset=related_model.objects.all(), required=False,
                widget=forms.widgets.HiddenInput()
            )
        

class ChildrenChangeList(ChangeList):
    """A ChangeList that has as queryset the children of a parent
    
    This is used to represent all children of a parent using the same
    features used in a normal changelist but when using AjaxInline

    """
    def __init__(self, request, parent=None, fk_name=None, 
                 model=None, list_display=(),
                 list_display_links=(), list_filter=None, 
                 date_hierarchy=None, search_fields=(), list_select_related=True,
                 list_per_page=200, list_max_show_all=200, single_child = None,
                 list_editable=None, model_admin=None, ajax_inline=None):

        self.ajax_inline = ajax_inline  # needed fo get the queryset
        self.parent = parent
        self.fk_name = fk_name
        self.single_child = single_child
        self.model = model
        self.opts = model._meta
        self.lookup_opts = self.opts
        self.model_admin = model_admin or site._registry[self.model]
        try:
            self.root_query_set = self.model_admin.queryset(request)
        except AttributeError:  # django >= 1.6
            self.root_queryset = self.model_admin.queryset(request)
        self.list_display = list_display
        self.add_edit_delete_icons()  # TO_DOC
        self.list_display_links = list_display_links or ('get_edit_icon_iframe',)
        self.list_filter = list_filter
        self.date_hierarchy = date_hierarchy
        self.search_fields = search_fields
        self.list_select_related = list_select_related
        self.list_per_page = list_per_page
        self.list_max_show_all = list_max_show_all
        self.formset = None

        # # Get search parameters from the query string.
        # try:
        #     self.page_num = int(request.GET.get(PAGE_VAR, 0))
        # except ValueError:
        #     self.page_num = 0
        self.show_all = False   # ALL_VAR in request.GET
        self.is_popup = False   # IS_POPUP_VAR in request.GET
        self.to_field = None   # request.GET.get(TO_FIELD_VAR)
        self.params = {}       # dict(request.GET.items())
        # if PAGE_VAR in self.params:
        #     del self.params[PAGE_VAR]
        # if ERROR_FLAG in self.params:
        #     del self.params[ERROR_FLAG]

        self.list_editable = ()
        # if self.is_popup:
        #     self.list_editable = ()
        # else:
        #     self.list_editable = list_editable
        # self.query = request.GET.get(SEARCH_VAR, '')

        try:
            self.query_set = self.get_query_set(request)
        except AttributeError:
            self.queryset = self.get_queryset(request)
            
        self.preserved_filters = False
        self.get_results(request)

        # if self.is_popup:
        #     title = ugettext('Select %s')
        # else:
        #     title = ugettext('Select %s to change')
        # self.title = title % force_text(self.opts.verbose_name)
        self.pk_attname = self.lookup_opts.pk.attname


        # super(ChildrenChangeList, self).__init__(request, **kw)

        
    def get_query_set(self, request):

        return self.get_queryset(request)
     
    def get_queryset(self, request):
        try:
            return self.ajax_inline.get_queryset(request)
        except AttributeError:
            return self.model.objects.filter(pk=self.single_child.pk)
        
    def add_edit_delete_icons(self):
        for name in ('get_edit_icon_iframe', 'get_delete_icon_iframe'):
            if not name in self.list_display:
                self.list_display = list(self.list_display or []) + [name]
    
        
class AjaxInline(object):
    """
    Options for inline editing of ``model`` instances.

    This is an ``inline`` whose editing happens via separate iframes
    but that are displayed along with normal ones.
    """
    #: the model the ajax_inline refers to, similarly to what happens with tabular_inline
    model = None
    
    #: the field that links to the parent 
    fk_name = None

    verbose_name = None
    verbose_name_plural = None

    #: basename of the template used to rendere the whole section
    #: the search path follows the reuls of change_form
    template = 'ajax_inline.html'

    #: the basename of the template used to render the single row
    #: the search path follows the reuls of change_form
    line_template = 'line_render.html'
    list_display = ('__str__',)
    list_display_links = ()
    list_per_page = 200
    list_max_show_all = 200
    single_child = None
    #: width of the iframe
    width = 700
    height = 700

    def __init__(self, parent_model=None, admin_site=None, parent=None):
        """
        :arg parent_model: needed to get the foreign key
        :arg admin_site: the admin_site, needed to get the ModelAdmin (?)
        :arg parent: needed to get all children when rendering the changelist
        """
        self.admin_site = admin_site
        self.parent_model = parent_model
        self.opts = self.model._meta
        self.parent = parent
        if self.parent_model and not self.fk_name:
            self.fk_name = _get_foreign_key(self.parent_model, self.model).name

        if self.verbose_name is None:
            self.verbose_name = self.model._meta.verbose_name
        if self.verbose_name_plural is None:
            self.verbose_name_plural = self.model._meta.verbose_name_plural

    def set_changelist(self, request, obj=None):
        """Add a changelist to the inline so that rendering can occurre

        :arg request: An HttpRequest
        :arg obj: the only object that should be returned by this changelist
        """

        kw = dict(model=self.model, list_display=self.list_display,
            list_display_links=self.list_display_links, list_filter=None, 
            date_hierarchy=None, search_fields=(), list_select_related=True,
            list_per_page=self.list_per_page, list_max_show_all=self.list_max_show_all, 
                  list_editable=None, model_admin=None, ajax_inline=self)

        self.single_child = obj
        self.cl = ChildrenChangeList(request, self.parent, self.fk_name, **kw)
        self.cl.ajax_inline = self
        
    def get_queryset(self, request):
        """Return a queryset of all the objects to represent in this run
        
        :arg request: HttpRequest
        """
        if self.single_child:
            return self.model.objects.filter(pk=self.single_child.pk)
        
        return self.model.objects.filter(**{self.fk_name: self.parent})
        
    @property
    def add_link(self):
        # I only use this when self.parent is set
        link = reverse('admin:%s_%s_add' % (
            self.model._meta.app_label, self.model._meta.object_name.lower()))
        return link + "?%s=%d" % (self.fk_name, self.parent.pk)

    @classmethod
    def get_delete_link(self, obj):
        # used in line_render
        return reverse('admin:%s_%s_delete' % (
            self.model._meta.app_label, self.model._meta.object_name.lower()),
                       args=(obj.pk,))

    @classmethod
    def get_edit_link(self, obj):
        # used in line_render
        return reverse('admin:%s_%s_change' % (
            self.model._meta.app_label, self.model._meta.object_name.lower()), 
                       args=(obj.pk,))

    def get_rows(self, obj):
        """Return all the rows that should be displayed by this AjaxInLine

        :arg obj: the object whose row we want to fetch
        """
        ## This works correctly also with multi-table inherintance 
        return self.model.objects.filter(**{self.fk_name :obj})

    def get_rows_from_parent(self, obj):

        return self.get_rows(obj)

    def has_add_permission(self, request):
        if self.opts.auto_created:
            # We're checking the rights to an auto-created intermediate model,
            # which doesn't have its own individual permissions. The user needs
            # to have the change permission for the related model in order to
            # be able to do anything with the intermediate model.
            return self.has_change_permission(request)
        return request.user.has_perm(
            self.opts.app_label + '.' + self.opts.get_add_permission())

    def has_view_permission(self, request):
        ## FIXME chiarire con vittorino
        return True

    def has_change_permission(self, request, obj=None):
        opts = self.opts
        if opts.auto_created:
            # The model was auto-created as intermediary for a
            # ManyToMany-relationship, find the target model
            for field in opts.fields:
                if field.rel and field.rel.to != self.parent_model:
                    opts = field.rel.to._meta
                    break
        return request.user.has_perm(
            opts.app_label + '.' + opts.get_change_permission())

    def has_delete_permission(self, request, obj=None):
        if self.opts.auto_created:
            # We're checking the rights to an auto-created intermediate model,
            # which doesn't have its own individual permissions. The user needs
            # to have the change permission for the related model in order to
            # be able to do anything with the intermediate model.
            return self.has_change_permission(request, obj)
        return request.user.has_perm(
            self.opts.app_label + '.' + self.opts.get_delete_permission())

    def render_row(self, obj):
        """
        Return the single row inside a ``return_list`` output
        We know there is just one ``tr`` in this ``tbody``
        """

        html = self.render(obj)
        d = pq(html)
        return d('tbody').html()

    def render_row_old(self, obj):
        """
        Render the single line using ``self.line_render`` (default: ``line_render.html``) 
        The search path follows the same rules as ``change_form.html`` & similar.

        :arg obj: the obj to be rendered. If not present self.obj will be used
        """
        opts = self.model._meta
        app_label = opts.app_label
        template_list = [
            "admin/%s/%s/%s" % (app_label, opts.object_name.lower(), self.line_template),
            "admin/%s/%s" % (app_label, self.line_template),
            "admin/%s" % self.line_template,
        ]
        context = {
            'row' : obj,
            'ajax_inline' : self,
        }
        return loader.render_to_string(template_list, context)
        
    def clean_table_headers(self, html):
        """
        Return a table with js stripped from headers
        :arg html: the output of th template
        """
        d = pq(html)
        for link in pq(d).find(".sorted"):
            pq(link).removeClass("sorted")
            
        for idx, val in enumerate(pq(d).find(".sortable")):
            pq(val).removeClass("sortable")
            pq(val).removeClass("sorting")
            
        #import ipdb; ipdb.set_trace()  
        d(".sortoptions").replaceWith('')
        for link in d("a.toggle"):
            pq(link).replaceWith('')
        for link in d("th .text a"):
            pq(link).removeAttr('href')
            pq(link).replaceWith('<div>'+pq(link).html()+'</div>')

        return mark_safe(str(d))
        
    def render(self, parent=None):
        """
        Render the whole section using ``self.template`` (default: ``ajax_inline.html``) 
        The search path follows the same rules as ``change_form.html`` & similar.

        ``ajax_inline.html`` uses standard ``result_list`` used in ``change_list.html``

        """
        opts = self.model._meta
        app_label = opts.app_label
        template_list = [
            "admin/%s/%s/%s" % (app_label, opts.object_name.lower(), self.template),
            "admin/%s/%s" % (app_label, self.template),
            "admin/%s" % self.template,
        ]
        context = {
            'ajax_inline' : self,
        }
        
        t = loader.select_template(template_list)

        table = loader.render_to_string(template_list, context) 
        return self.clean_table_headers(table)
        
        
