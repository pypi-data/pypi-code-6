from __future__ import absolute_import

import urllib

from django.core.urlresolvers import reverse, NoReverseMatch
from django.contrib import messages
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from .forms import (FilterForm, GenericConfirmForm, GenericAssignRemoveForm,
                    DetailForm)


class ExtraContextMixin(object):
    extra_context = {}

    def get_context_data(self, **kwargs):
        context = super(ExtraContextMixin, self).get_context_data(**kwargs)
        context.update(self.extra_context)
        return context


class GenericCreateView(ExtraContextMixin, CreateView):
    template_name = 'generic_views/generic_form.html'


class GenericDeleteView(ExtraContextMixin, DeleteView):
    template_name='generic_views/generic_confirm.html'

    def get_context_data(self, **kwargs):
        context = super(GenericDeleteView, self).get_context_data(**kwargs)
        context['delete_view'] = True
        return context

    #kwargs['post_delete_redirect'] = reverse(kwargs['post_delete_redirect'])


class GenericDetailView(ExtraContextMixin, DetailView):
    template_name = 'generic_views/generic_detail.html'

    def get_context_data(self, **kwargs):
        context = super(GenericDetailView, self).get_context_data(**kwargs)
        if hasattr(self, 'extra_fields'):
            context['form'] = self.form_class(instance=self.get_object(), extra_fields=getattr(self, 'extra_fields', None))
        else:
            context['form'] = self.form_class(instance=self.get_object())

        return context


class GenericListView(ExtraContextMixin, ListView):
    filter_form = None
    filters = None
    list_filters = None
    template_name = 'generic_views/generic_list.html'

    def get(self, request, *args, **kwargs):
        if self.list_filters:
            self.filter_form, self.filters = add_filter(self.request, self.list_filters)
        return super(GenericListView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(GenericListView, self).get_context_data(**kwargs)

        if self.filter_form:
            context['filter_form'] = self.filter_form

        return context

    def get_queryset(self):
        queryset = super(GenericListView, self).get_queryset()
        if self.filters:
            return queryset.filter(*self.filters)
        else:
            return queryset


class GenericUpdateView(ExtraContextMixin, UpdateView):
    template_name = 'generic_views/generic_form.html'


def add_filter(request, list_filters):
    filters = []
    filter_dict = dict([(f['name'], f) for f in list_filters])
    if request.method == 'GET':
        filter_form = FilterForm(list_filters, request.GET)
        if filter_form.is_valid():
            for name, data in filter_form.cleaned_data.items():
                if data:
                    filters.append(Q(**{filter_dict[name]['destination']: data}))

    else:
        filter_form = FilterForm(list_filters)

    return filter_form, filters


def generic_assign_remove(request, title, obj, left_list_qryset, left_list_title, right_list_qryset, right_list_title, add_method, remove_method, item_name, list_filter=None):
    left_filter = None
    filter_form = None
    if list_filter:
        filter_form, filters = add_filter(request, list_filter)
        if filters:
            left_filter = filters

    if request.method == 'POST':
        post_data = request.POST
        form = GenericAssignRemoveForm(left_list_qryset, right_list_qryset, left_filter, request.POST)
        if form.is_valid():
            action = post_data.get('action','')
            if action == 'assign':
                for item in form.cleaned_data['left_list']:
                    add_method(item)
                if form.cleaned_data['left_list']:
                    messages.success(request, _(u'The selected %s were added.') % unicode(item_name))

            if action == 'remove':
                for item in form.cleaned_data['right_list']:
                    remove_method(item)
                if form.cleaned_data['right_list']:
                    messages.success(request, _(u'The selected %s were removed.') % unicode(item_name))

    form = GenericAssignRemoveForm(left_list_qryset=left_list_qryset, right_list_qryset=right_list_qryset, left_filter=left_filter)

    return render_to_response('generic_views/generic_assign_remove.html', {
    'form': form,
    'object': obj,
    'title': title,
    'left_list_title': left_list_title,
    'right_list_title': right_list_title,
    'filter_form': filter_form,
    },
    context_instance=RequestContext(request))
