from django.conf import settings
from django.contrib.admin.util import lookup_field, display_for_field, label_for_field
from django.contrib.admin.views.main import ALL_VAR, EMPTY_CHANGELIST_VALUE
from django.contrib.admin.views.main import ORDER_VAR, ORDER_TYPE_VAR, PAGE_VAR, SEARCH_VAR
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.forms.forms import pretty_name
from django.utils import formats
from django.utils.html import escape, conditional_escape
from django.utils.safestring import mark_safe
from django.utils.text import capfirst
from django.utils.translation import ugettext as _
from django.utils.encoding import smart_unicode, force_unicode
from django.template import Library

from jmb.core.middleware.thread_local import get_request

register = Library()

def result_headers(cl):
    lookup_opts = cl.lookup_opts

    for i, field_name in enumerate(cl.list_display):
        header, attr = label_for_field(field_name, cl.model,
            model_admin = cl.model_admin,
            return_attr = True
        )
        if attr:
            # if the field is the action checkbox: no sorting and special class
            if field_name == 'action_checkbox':
                yield {
                    "text": header,
                    "class_attrib": mark_safe(' class="action-checkbox-column"')
                }
                continue
            header = pretty_name(header)

            # It is a non-field, but perhaps one that is sortable
            admin_order_field = getattr(attr, "admin_order_field", None)
            if not admin_order_field:
                yield {"text": header,
                       "class_attrib": mark_safe(' class="fieldname_%s"' % field_name)}
                continue

            # So this _is_ a sortable non-field.  Go to the yield
            # after the else clause.
        else:
            admin_order_field = None

        th_classes = ['fieldname_%s' % field_name]
        #th_classes = []
        new_order_type = 'asc'
        if field_name == cl.order_field or admin_order_field == cl.order_field:
            th_classes.append('sorted %sending' % cl.order_type.lower())
            new_order_type = {'asc': 'desc', 'desc': 'asc'}[cl.order_type.lower()]

        yield {
            "text": header,
            "sortable": True,
            "url": cl.get_query_string({ORDER_VAR: i, ORDER_TYPE_VAR: new_order_type}),
            "class_attrib": mark_safe(th_classes and ' class="%s"' % ' '.join(th_classes) or '')
        }

def _boolean_icon(field_val):
    BOOLEAN_MAPPING = {True: 'yes', False: 'no', None: 'unknown'}
    return mark_safe(u'<img src="%simg/admin/icon-%s.gif" alt="%s" />' % (settings.ADMIN_MEDIA_PREFIX, BOOLEAN_MAPPING[field_val], field_val))


class Item(object):
    def __init__(self):
        self.request_get = get_request().GET.copy()
        self.last_orderby_value = None
        self.row_classes = []

    def items_for_result(self, cl, result, form):
        first = True
        pk = cl.lookup_opts.pk.attname
        num_col = len(cl.list_display)
        last_value = None

        if hasattr(cl.model_admin, 'default_group_by') and cl.model_admin.default_group_by:
            groupby = cl.model_admin.default_group_by
            if self.request_get.has_key('groupby'):
                groupby = self.request_get['groupby']
            groupby = groupby.replace("-", "")
            orderby_value = self._get_field_value(cl, groupby, result)
            if self.last_orderby_value != orderby_value:
                groupby_header, attr = label_for_field(groupby, cl.model,
                    model_admin = cl.model_admin,
                    return_attr = True
                )
                yield mark_safe(u'</tr></tbody><tbody><tr class="group_tr"><th class="" colspan="%s"><div class="group_div">%s: %s</div></th></tr><tr class="row1">' % (num_col, groupby_header, orderby_value))
                self.last_orderby_value = orderby_value

        for field_name in cl.list_display:
            self.row_classes = ['fieldname_%s' % field_name]
            result_repr = self._get_field_value(cl, field_name, result)

            if force_unicode(result_repr) == '':
                result_repr = mark_safe('&nbsp;')

            row_class = ' class="%s"' % ' '.join(self.row_classes)
            # If list_display_links not defined, add the link tag to the first field
            if (first and not cl.list_display_links) or field_name in cl.list_display_links:
                table_tag = {True:'th', False:'td'}[first]
                first = False
                url = cl.url_for_result(result)
                # Convert the pk to something that can be used in Javascript.
                # Problem cases are long ints (23L) and non-ASCII strings.
                if cl.to_field:
                    attr = str(cl.to_field)
                else:
                    attr = pk
                value = result.serializable_value(attr)
                result_id = repr(force_unicode(value))[1:]
                if cl.is_popup or not getattr(cl.model_admin, 'no_display_links', False):
                    yield mark_safe(u'<%s%s><a href="%s"%s>%s</a></%s>' % \
                    (table_tag, row_class, url, (cl.is_popup and ' onclick="opener.dismissRelatedLookupPopup(window, %s); return false;"' % result_id or ''), conditional_escape(result_repr), table_tag))
                else:
                    yield mark_safe(u'<td%s>%s</td>' % \
                        (row_class, conditional_escape(result_repr)))
            else:
                # By default the fields come from ModelAdmin.list_editable, but if we pull
                # the fields out of the form instead of list_editable custom admins
                # can provide fields on a per request basis
                if form and field_name in form.fields:
                    bf = form[field_name]
                    result_repr = mark_safe(force_unicode(bf.errors) + force_unicode(bf))
                else:
                    result_repr = conditional_escape(result_repr)
                if result_repr == EMPTY_CHANGELIST_VALUE:
                    result_repr = ''
                yield mark_safe(u'<td%s>%s</td>' % (row_class, result_repr))
        if form:
            yield mark_safe(force_unicode(form[cl.model._meta.pk.name]))


    def _get_field_value(self, cl, field_name, result):
        try:
            f, attr, value = lookup_field(field_name, result, cl.model_admin)
        except (AttributeError, ObjectDoesNotExist):
            result_repr = EMPTY_CHANGELIST_VALUE
        else:
            if f is None:
                allow_tags = getattr(attr, 'allow_tags', False)
                boolean = getattr(attr, 'boolean', False)
                if boolean:
                    allow_tags = True
                    result_repr = _boolean_icon(value)
                else:
                    result_repr = smart_unicode(value)
                # Strip HTML tags in the resulting text, except if the
                # function has an "allow_tags" attribute set to True.
                if not allow_tags:
                    result_repr = escape(result_repr)
                else:
                    result_repr = mark_safe(result_repr)
            else:
                if value is None:
                    result_repr = EMPTY_CHANGELIST_VALUE
                if isinstance(f.rel, models.ManyToOneRel):
                    if getattr(result, f.name):
                        result_repr = escape(getattr(result, f.name))
                    else:
                        result_repr = EMPTY_CHANGELIST_VALUE
                else:
                    result_repr = display_for_field(value, f)
                if isinstance(f, models.DateField) or isinstance(f, models.TimeField):
                    row_class = ' class="nowrap"'
        return result_repr

def results(cl):
    if cl.formset:
        item = Item()
        for res, form in zip(cl.result_list, cl.formset.forms):
            yield list(item.items_for_result(cl, res, form))
    else:
        item = Item()
        for res in cl.result_list:
            yield list(item.items_for_result(cl, res, None))

def result_list(cl):
    return {'cl': cl,
            'result_headers': list(result_headers(cl)),
            'results': list(results(cl))}
result_list = register.inclusion_tag("admin/change_list_results.html")(result_list)
