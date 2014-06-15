# -*- coding: utf-8 -*-
import re
from functools import partial, reduce, update_wrapper

from django import template
from django.core.urlresolvers import reverse
from django.db import models, transaction, router
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext as ugt
from django.contrib.admin.util import unquote, lookup_field, display_for_field, get_deleted_objects
from django.utils.encoding import force_unicode, smart_unicode
from django.shortcuts import render_to_response
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.utils.html import escape, strip_tags
from django.views.decorators.csrf import csrf_protect
from django.conf import settings
from django.utils.decorators import method_decorator
from django.core.exceptions import PermissionDenied, ValidationError
from django.utils.http import urlquote
from django.contrib.admin.util import flatten_fieldsets
from django.contrib import messages
from django.conf.urls import patterns, url

#from jmb.core.forms.widgets import DateTimeWidget, DateWidget
from jmb.core.utils.functions import render_csv, render_xls
from jmb.core.db.utils import clone
from jmb.core.middleware.thread_local import get_request
from ajax_inlines import AjaxParentModelAdmin
from django_filters.admin.options import AdvancedSearchModelAdmin

csrf_protect_m = method_decorator(csrf_protect)

# GET parameter for the URL to return to after change/add views. This lets the
# admin save the state of the changelist page through the change/add page.
#RETURN_GET_PARAM = '_return_to'

def set_active(modeladmin, request, queryset):
    rows_updated = 0
    for obj in queryset:
        obj.status = 1
        obj.save()
        rows_updated += 1
    if rows_updated == 1:
        message_bit = ugt("1 object was")
    else:
        message_bit = ugt("%(row)s objects were") % {'row': rows_updated}
    modeladmin.message_user(request, ugt("%(msg)s successfully actived.") % \
                                                  {'msg': message_bit})
set_active.short_description = _("Set %(verbose_name_plural)s as active")
admin.site.add_action(set_active)


def set_disactive(modeladmin, request, queryset):
    rows_updated = 0
    for obj in queryset:
        obj.status = 0
        obj.save()
        rows_updated += 1
    if rows_updated == 1:
        message_bit = ugt("1 object was")
    else:
        message_bit = ugt("%(row)s objects were") % {'row': rows_updated}
    modeladmin.message_user(request, ugt("%(msg)s successfully disactived.") % \
                                                  {'msg': message_bit})
set_disactive.short_description = _("Set %(verbose_name_plural)s as disactive")
admin.site.add_action(set_disactive)


def _export_data(modeladmin, request=None, queryset=None):
    """
    ritorna un generatore di liste contenenti i valori degli item del queryset
    :arg modeladmin: the modeladmin. 
    :arg request: the request, not used
    :arg queryset: the queryset or a list of
    """
    if hasattr(modeladmin, 'list_display_csv'):
        fields_list = modeladmin.list_display_csv
    else:
        fields_list = modeladmin.list_display

    plural_name = ugt(modeladmin.model._meta.verbose_name_plural)

    title = list(fields_list)
    title.append('\n')
    if 'action_checkbox' in title:
        title.remove('action_checkbox')
    yield title

    for obj in queryset:
        row = []
        for field_name in fields_list:
                
            if field_name == 'action_checkbox':
                continue
            field, attr, value = lookup_field(field_name, obj, modeladmin)
            if not field:
                # try to interpret it as a modeladmin's function
                if hasattr(modeladmin, field_name):
                    result_repr = getattr(modeladmin, field_name)(obj)
                elif hasattr(obj, field_name):
                    result_repr = getattr(obj, field_name)()
            elif value is None:
                if isinstance(field, (models.DecimalField, models.IntegerField, 
                                      models.FloatField, models.NullBooleanField)):
                    result_repr = ''
                elif field is None:
                    result_repr = strip_tags(smart_unicode(value))
            else:
                if isinstance(field, (models.NullBooleanField, models.BooleanField)):
                    result_repr = False and _('No') or _('Yes')
                else:
                    result_repr = display_for_field(value, field)

            # Tolgo eventuali 'a capo'
            row.append(unicode(result_repr))
        yield row

class ExportData(object):
    def __init__(self, modeladmin, request=None, queryset=None):
        """
        ritorna un generatore di liste contenenti i valori degli item del queryset
        :arg modeladmin: the modeladmin. 
        :arg request: the request, not used
        :arg queryset: the queryset or a list of
        """
        # Attempt to split into a simple part that uses modelaldimn that is difficult to 
        # serialize and another that can be serialized so as to use it when passing over
        # to celery
        self.fields_list = self.get_field_list()

        if hasattr(modeladmin, 'list_display_csv'):
            fields_list = modeladmin.list_display_csv
        else:
            fields_list = modeladmin.list_display

        plural_name = ugt(modeladmin.model._meta.verbose_name_plural)

        title = list(fields_list)
        title.append('\n')
        if 'action_checkbox' in title:
            title.remove('action_checkbox')
        yield title

        for obj in queryset:
            row = []
            for field_name in fields_list:

                if field_name == 'action_checkbox':
                    continue
                field, attr, value = lookup_field(field_name, obj, modeladmin)
                if not field:
                    # try to interpret it as a modeladmin's function
                    if hasattr(modeladmin, field_name):
                        result_repr = getattr(modeladmin, field_name)(obj)
                elif value is None:
                    if isinstance(field, (models.DecimalField, models.IntegerField, 
                                          models.FloatField, models.NullBooleanField)):
                        result_repr = ''
                    elif field is None:
                        result_repr = strip_tags(smart_unicode(value))
                else:
                    if isinstance(field, (models.NullBooleanField, models.BooleanField)):
                        result_repr = False and _('No') or _('Yes')
                    else:
                        result_repr = display_for_field(value, field)

                # Tolgo eventuali 'a capo'
                row.append(unicode(result_repr))
            yield row



def clone_action(modeladmin, request, queryset):
    verbose_name = ugt(modeladmin.model._meta.verbose_name)
    verbose_name_plural = ugt(modeladmin.model._meta.verbose_name_plural)
    cloned = 0
    not_cloned = 0

    for obj in queryset:
        # TODO: da trasformare in funzione
        cloned_obj, result = clone(obj)
        # TODO: da fixare in funzione di cosa restituisce la funzione
        if result != True:
            not_cloned += 1
            messages.error(request, _("%(name)s not cloned: %(id)d") % {
                    'name': verbose_name,
                    'id': obj.pk
                 }
            )
            continue
        else:
            cloned += 1

    if not_cloned:
        name = verbose_name
        if not_cloned > 1:
            name = verbose_name_plural
        messages.error(request, _("%(name)s not cloned: %(number)s") % {'name': name, 'number': not_cloned})
    if cloned:
        name = verbose_name
        if cloned > 1:
            name = verbose_name_plural
        messages.info(request, _("%(name)s cloned: %(number)s") % {'name': name, 'number': cloned})
    else:
        name = verbose_name_plural
        messages.error(request, _("%(name)s cloned: %(number)s") % {'name': name, 'number': cloned})
clone_action.short_description = _("Clone selected %(verbose_name_plural)s")
#admin.site.add_action(clone_action)

def export_csv(modeladmin, request, queryset):
    """
    action per esportazione elementi selezionati changelist_view in .csv
    """
    plural_name = ugt(modeladmin.model._meta.verbose_name_plural)
    return render_csv(_export_data(modeladmin, request, queryset), '%s.csv' % plural_name)
export_csv.short_description = _("Export selected %(verbose_name_plural)s in csv")
admin.site.add_action(export_csv)


def export_xls(modeladmin, request, queryset):
    """
    action per esportazione elementi selezionati changelist_view in .xls
    """
    plural_name = ugt(modeladmin.model._meta.verbose_name_plural)
    return render_xls(_export_data(modeladmin, request, queryset), '%s.xls' % plural_name)
export_xls.short_description = _("Export selected %(verbose_name_plural)s in xls")
admin.site.add_action(export_xls)


class SettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('general admin'), {'fields': (('name', 'type'), 'value',
                                          'description')}),
    )
    list_display = ('name', 'value', 'type', 'description')
    list_display_links = ('name', )
    list_per_page = 30


class ExtendibleModelAdmin(AjaxParentModelAdmin):
    class Media:

        js = ['jmb/js/collapsed_stacked_inlines.js',
              #'jmb/js/detail_fancybox.js'
              ]

    #: tabs: show tabs even if they're empty
    tabs_show_empty = True

    #: tabs: show tab lables sticky on top of the page
    tabs_sticky_on_top = False

    no_display_links = True
    list_per_page = 20
    save_on_top = True
    use_fancybox = False
    father_foreignkey_fancybox  = None

    def get_list_display_links(self, request, list_display):
        return ('get_edit_icon',)

    def get_readonly_fields(self, request, obj=None):
        readonly = ()
        fields = []
        if self.declared_fieldsets:
            fields = flatten_fieldsets(self.declared_fieldsets)

        if 'creator' in fields:
            readonly = readonly + ('creator',)
        if 'date_create' in fields:
            readonly = readonly + ('date_create',)
        if 'last_modifier' in fields:
            readonly = readonly + ('last_modifier',)
        if 'date_last_modify' in fields:
            readonly = readonly + ('date_last_modify',)
        return self.readonly_fields + readonly

    def get_changelist_instance(self, request):
        """Return a chagelist instance suitable to find out the real queryset represented bu result_list
        This function can be used in actions when the queryset is much faster then
        using the list of single ids
        """
        kw = dict(model=self.model, list_display=self.list_display,
            list_display_links=self.list_display_links, list_filter=self.list_filter,
            date_hierarchy=self.date_hierarchy, search_fields=self.search_fields, list_select_related=self.list_select_related,
            list_per_page=self.list_per_page, list_max_show_all=self.list_max_show_all,
            list_editable=self.list_editable, model_admin=self)
        return self.get_changelist(request)(request, **kw)

    def _getobj(self, request, object_id):
            opts = self.model._meta
            app_label = opts.app_label

            try:
                obj = self.queryset(request).get(pk=unquote(object_id))
            except self.model.DoesNotExist:
                obj = None

            if obj is None:
                raise Http404(_('%(name)s object with primary key %(key)r does not exist.') % {'name': force_unicode(opts.verbose_name), 'key': escape(object_id)})
            return obj

    def _wrap(self, view):
        def wrapper(*args, **kwargs):
            return self.admin_site.admin_view(view)(*args, **kwargs)
        return update_wrapper(wrapper, view)

    def _view_name(self, name):
        info = self.model._meta.app_label, self.model._meta.module_name, name
        return '%s_%s_%s' % info

    def has_change_permission(self, request, obj=None):
        has_change_permission = super(ExtendibleModelAdmin, self).has_change_permission(request, obj)
        if obj is None:
            if (
                has_change_permission or
                request.user.has_perm(self.model._meta.app_label + '.' + 'view_%s' % self.model._meta.module_name) or
                request.user.has_perm(self.model._meta.app_label + '.' + 'list_%s' % self.model._meta.module_name)
            ):
                return True
            return False
        else:
            if hasattr(obj, "can_be_modified"):
                if obj.can_be_modified():
                    return True
                else:
                    return False
            return has_change_permission

    def has_delete_permission(self, request, obj=None):
        has_delete_permission = super(ExtendibleModelAdmin, self).has_delete_permission(request, obj)
        if hasattr(obj, "can_be_delete"):
            if obj.can_be_delete():
                return True
            else:
                return False

        return has_delete_permission

    def get_value_obj(self, obj, attribute):
        value = None
        try:
            value = getattr(obj, attribute)
        except:
            try:
                if hasattr(self, attribute):
                    value = getattr(self, attribute)(obj)
            except Exception, e:
                pass
        return value

    def detail_view(self, request, object_id, **kwargs):
        obj = self._getobj(request, object_id)
        opts = self.model._meta
        verbose_name = opts.verbose_name
        app_label = opts.app_label.lower()
        object_name = opts.object_name.lower()

        detail_fields = []
        d_values = {}
        #ricordarsi di aggiungere nel progetto
        #(r'^comments/', include('django.contrib.comments.urls')), 
        template_name = kwargs.get('template_name', 'detail.html')

        if hasattr(self, 'detail_display'):
            for f in self.detail_display:
                # Se e' una lista aggiunga tt i suoi campi ai detail_fields
                if type(f) == type([]) or type(f) == type(()):
                    detail_fields.append(f)
                    for subf in f:
                        d_values[subf] = self.get_value_obj(obj, subf)
                # Se la funzione e' presente nell'admin la chiamo e aggiungo il
                # valore ai detail fields
                elif hasattr(self, f):
                    detail_fields.append([f])
                    d_values[f] = getattr(self, f)(obj)
                # altrimenti cerco il valore dell'oggetto in maniera normale
                else:
                    detail_fields.append([f])
                    d_values[f] = self.get_value_obj(obj, f)

        context = {
            'title': _('Detail %s') % force_unicode(verbose_name),
            'object_id': object_id,
            'obj': obj,
            'is_popup': request.REQUEST.has_key('_popup'),
            'app_label': app_label,
            'opts': opts,
            'detail_fields': detail_fields,
            'd_values': d_values,
            'has_change_permission': self.has_change_permission(request, obj),
        }
        context_instance = template.RequestContext(request, current_app=self.admin_site.name)

        return render_to_response([
            "admin/%s/%s/%s" % (app_label, object_name, template_name),
            "admin/%s/%s" % (app_label, template_name),
            "admin/%s" % template_name
        ], context, context_instance=context_instance)

    #nuovo nome, retrocompatibilità
    detail = detail_view

    @csrf_protect_m
    @transaction.commit_on_success
    def import_data_view(self, request, form_url='', extra_context=None, **kwargs):
        "The 'import data' admin view for this model."
        from jmb.core.admin.forms import ImportDataForm
        from jmb.core.admin.import_data import ImportData
        from django.contrib import messages

        model = self.model
        opts = model._meta
        app_label = opts.app_label
        verbose_name = force_unicode(opts.verbose_name)

#        if not self.has_change_permission(request, obj):
#            raise PermissionDenied

        template_name = kwargs.get('template_name', 'import_data.html')
        breadcrumbs = (
            (_('Home'), '/admin/'),
            (_(app_label), '/admin/%s/' % app_label),
            (_(verbose_name), '/admin/%s/%s/' % (app_label, verbose_name)),
        )

        if request.method == 'POST':
            form = ImportDataForm(request.POST, request.FILES)
            if form.is_valid():
                file_source = form.cleaned_data['import_file']
                import_data = ImportData(
                    file_contents=file_source.read(), auto=True, model=model
                )
                import_data.read()
                if import_data.messages['inserted'] > 0:
                    messages.success(request, "%s righe inserite correttamente" % import_data.messages['inserted'])
                if import_data.messages['modified'] > 0:
                    messages.warning(request, "%s righe modificate correttamente" % import_data.messages['modified'])
                if import_data.messages['errors']:
                    for error in import_data.messages['errors']:
                        messages.error(request, error)
            else:
                messages.error(request, "Correggi l'errore qui sotto")
        else:
            form = ImportDataForm()

        context = {
            'title': _('Import %s') % verbose_name,
            'is_popup': "_popup" in request.REQUEST,
            'app_label': opts.app_label,
            'breadcrumbs': breadcrumbs,
            'import_form': form
        }
        context.update(extra_context or {})
        context_instance = template.RequestContext(request, current_app=self.admin_site.name)
        return render_to_response(
            [
                "admin/%s/%s/%s" % (opts.app_label, opts.object_name.lower(), template_name),
                "admin/%s/%s" % (opts.app_label, template_name),
                "admin/%s" % template_name
            ],
            context,
            context_instance=context_instance
        )

    @csrf_protect_m
    @transaction.commit_on_success
    def export_data_view(self, request, form_url='', extra_context=None, **kwargs):
        "The 'export data' admin view for this model."
        from django.contrib import messages
        from jmb.core.admin.forms import ExportDataForm
        from jmb.core.admin import tasks

        model = self.model
        opts = model._meta
        app_label = opts.app_label
        verbose_name = force_unicode(opts.verbose_name)

        #        if not self.has_change_permission(request, obj):
        #            raise PermissionDenied

        template_name = kwargs.get('template_name', 'export_data.html')
        breadcrumbs = (
            (_('Home'), '/admin/'),
            (_(app_label), '/admin/%s/' % app_label),
            (_(verbose_name), '/admin/%s/%s/' % (app_label, verbose_name)),
        )

        if request.method == 'POST':
            form = ExportDataForm(request.POST, request.FILES)
            if form.is_valid():
                return tasks.create_xls(model)
            else:
                messages.error(request, "Correggi l'errore qui sotto")
        else:
            form = ExportDataForm()

        context = {
            'title': _('Export %s') % verbose_name,
            'is_popup': "_popup" in request.REQUEST,
            'app_label': opts.app_label,
            'breadcrumbs': breadcrumbs,
            'export_form': form
        }
        context.update(extra_context or {})
        context_instance = template.RequestContext(request, current_app=self.admin_site.name)
        return render_to_response(
            [
                "admin/%s/%s/%s" % (opts.app_label, opts.object_name.lower(), template_name),
                "admin/%s/%s" % (opts.app_label, template_name),
                "admin/%s" % template_name
            ],
            context,
            context_instance=context_instance
        )
    @csrf_protect_m
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['is_popup']= request.GET.get("_popup",False)
        return super(ExtendibleModelAdmin, self).changelist_view(request, extra_context)
    
    def get_urls(self):
        urls = super(ExtendibleModelAdmin, self).get_urls()

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            return update_wrapper(wrapper, view)

        info = self.model._meta.app_label, self.model._meta.module_name

        my_urls = patterns(
            '',
            url(
                r'^(.+)/detail/$',
                self._wrap(self.detail),
                name=self._view_name('detail')
            ),
            url(
                r'^import_data/$',
                self.admin_site.admin_view(self.import_data_view),
                name='%s_%s_import_data' % info
            ),
            url(
                r'export_data/$',
                self.admin_site.admin_view(self.export_data_view),
                name="%s_%s_export_data" % info
            ),
        )
        return my_urls + urls

#     def get_edit_icon(self, obj):

#         opts = self.model._meta
#         can_be_modified = False
#         # Se il modello ha la funzione can_be_modified la chiamo per fare
#         # i controlli relativi a quel modello
#         if hasattr(obj, "can_be_modified"):
#             if obj.can_be_modified():
#                 can_be_modified = True
#         # Se non ce l'ha non faccio controlli e visualizzo l'icona
#         else:
#             can_be_modified = True

#         request = get_request()
        
#         if can_be_modified:
#             dj_reverse_url = reverse('admin:%s_%s_change' % (opts.app_label, opts.object_name.lower()), args=(obj.pk,)) 
# ##            print "Debug: Puo essere modificato", obj
#             return "<a href=%(reverse_url)s><img src='%(url)sjmb/images/edit.gif' alt='%(window_title)s' title='%(window_title)s'/></a>" % {
#             'reverse_url': "%s" % (dj_reverse_url, ),
#             'url':settings.STATIC_URL,
#             'window_title':ugt("Edit %s" % opts.object_name.lower())
#         }
#         return ""
#     get_edit_icon.short_description = _("E")
#     get_edit_icon.allow_tags = True


#     def get_delete_icon(self, obj):
#         opts = self.model._meta
#         can_be_delete = False
#         # Se il modello ha la funzione can_be_modified la chiamo per fare
#         # i controlli relativi a quel modello
#         if hasattr(obj, "can_be_delete"):
#             if obj.can_be_delete():
#                 can_be_delete = True
#         # Se non ce l'ha non faccio controlli e visualizzo l'icona
#         else:
#             can_be_delete = True

#         if can_be_delete:
#             param = ""
#             if self.use_fancybox:
#                 param='?_popup=1&nobuttons=1'
#             return "<a href=%(reverse_url)s%(param)s><img src='%(url)sjmb/images/del.gif' alt='%(window_title)s' title='%(window_title)s'/></a>" % {
#                 'reverse_url':reverse('admin:%s_%s_delete' % (opts.app_label, opts.object_name.lower()), args=(obj.pk,)),
#                 'param': param,
#                 'url':settings.STATIC_URL,
#                 'window_title':ugt("Delete %s" % opts.object_name.lower())
#             }
#         return ""
#     get_delete_icon.short_description = _("D")
#     get_delete_icon.allow_tags = True

    def get_detail_icon(self, obj):
        opts = self.model._meta
        app_label = opts.app_label.lower()
        object_name = opts.object_name.lower()
        return """
            <a class='iframe' href=%(reverse_url)s?_popup=1&nobuttons=1>
                <img src='%(url)sjmb/images/search.png' alt='%(window_title)s' title='%(window_title)s'/>
            </a>""" % {
                'reverse_url':reverse('%s:%s_%s_detail' % (
                    self.admin_site.name, app_label, object_name), args=(obj.pk,)
                ),
                'url':settings.STATIC_URL,
                'window_title':ugt("Detail %s" % object_name)
            }
    get_detail_icon.allow_tags = True
    get_detail_icon.short_description = _("V")

    def get_status_icon(self, obj):
        return obj.status
    get_status_icon.short_description = _("ST")
    get_status_icon.boolean = True
    get_status_icon.admin_order_field = 'status'
            
class OrderedModelAdmin(admin.ModelAdmin):
    def _view_name(self, name):
        info = self.model._meta.app_label, self.model._meta.module_name, name
        return '%s_%s_%s' % info


    def _wrap(self, view):
        def wrapper(*args, **kwargs):
            return self.admin_site.admin_view(view)(*args, **kwargs)
        return update_wrapper(wrapper, view)


    def get_urls(self):
        from django.conf.urls import patterns, url
        urls = super(OrderedModelAdmin, self).get_urls()

        my_urls = patterns('',
            url(r'^(.+)/up/$',
                self._wrap(self.up),
                name=self._view_name('up')),
            url(r'^(.+)/down/$',
                self._wrap(self.down),
                name=self._view_name('down')),
            )
        return my_urls + urls


    def up(self, request, id):
        node = self.model._default_manager.get(pk=id)
        node.up()
        try:
            redirect_to = request.META['HTTP_REFERER']
        except:
            redirect_to = '../../'
        return HttpResponseRedirect(redirect_to)


    def down(self, request, id):
        node = self.model._default_manager.get(pk=id)
        node.down()
        try:
            redirect_to = request.META['HTTP_REFERER']
        except:
            redirect_to = '../../'
        return HttpResponseRedirect(redirect_to)

    def move_actions(self, node):
        info = self.admin_site.name, self.model._meta.app_label, self.model._meta.module_name
        data = []
        if not node.is_first(): # up node
            data.append(u'<a href="%s" class="nodes-up">%s</a>' % (reverse('%s:%s_%s_up' % info, node.id), _('up')))
        if not node.is_last() and not node.is_first():
            data.append(u'<span style="font-weight:normal"> | </span>')
        if not node.is_last(): # down node
            data.append(u'<a href="%s" class="nodes-down">%s</a>' % (reverse('%s:%s_%s_down' % info, node.id), _('down')))
        return u''.join(data)
    move_actions.short_description = _('move')
    move_actions.allow_tags = True
