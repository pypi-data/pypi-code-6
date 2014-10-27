# -*- coding: utf-8 -*-

import json
from datetime import datetime, timedelta

from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.contrib.sites.models import Site
from django.contrib import messages
from django.utils import timezone
import models as mymodels

from django.conf import settings as conf
from django.views.generic import DetailView, ListView

from rest_framework_bulk import ListBulkCreateAPIView, BulkDestroyAPIView

from rtimes import worktime, humanize_time, humanize_time_day, date_range


class Stamps(ListView):

    model = mymodels.Stamp

    def get_context_data(self, **kwargs):
        context = super(Stamps, self).get_context_data(**kwargs)
        customers = mymodels.Customer.objects.all()
        context.update({
            'customers': customers,
        })
        return context


class Refresh(ListView):

    model = mymodels.Stamp

    def get_context_data(self, **kwargs):
        if self.request.is_ajax() and self.request.method == 'GET':
            values = json.loads(self.request.GET.get('values', None))
            start = "%s 00:00:00" % self.request.GET.get('start', None)
            end = "%s 23:59:59" % self.request.GET.get('end', None)

            start = datetime.strptime(start, '%d/%m/%Y %H:%M:%S')
            start=timezone.make_aware(start, timezone.get_current_timezone())
            #start = start.strftime('%Y-%m-%d %H:%M:%S')

            end = datetime.strptime(end, '%d/%m/%Y %H:%M:%S')
            end=timezone.make_aware(end, timezone.get_current_timezone())
            #end = end.strftime('%Y-%m-%d %H:%M:%S')

            stamps = mymodels.Stamp.objects.filter(
                customer_id__in=values,
                start__gte=start,
                end__lte=end).order_by('start')

            # Total times
            totals = 0
            totals_customer = {}
            for v in values:
                tot = 0
                customer = mymodels.Customer.objects.get(pk=v)
                for st in stamps.filter(customer__id=v):
                    tot += worktime(st.start.strftime("%Y-%m-%d %H:%M"),
                                    st.end.strftime("%Y-%m-%d %H:%M"))
                totals += tot
                totals_customer[customer] = humanize_time(tot)

            # Total per day
            days = date_range(start, end)
            totals_day = {}
            stamps_day = {}
            for day in days:
                tot = 0
                tomorrow = day + timedelta(days=1)
                stamps_day[day.strftime("%Y-%m-%d")] = stamps.filter(
                    start__gte=day,
                    end__lte=tomorrow)
                for st in stamps_day[day.strftime("%Y-%m-%d")]:
                    tot += worktime(st.start.strftime("%Y-%m-%d %H:%M"),
                                    st.end.strftime("%Y-%m-%d %H:%M"))
                totals_day[day.strftime("%Y-%m-%d")] = humanize_time(tot)

        context = super(Refresh, self).get_context_data(**kwargs)
        context.update({
            'stamps': stamps,
            'totals_customer': totals_customer,
            'totals': humanize_time(totals),
            'totals_humanize_day': humanize_time_day(totals),
            'days': days,
            'stamps_day': stamps_day,
            'totals_day': totals_day,
        })
        return context

    def get_template_names(self):
        if self.request.is_ajax():
            return ['rstamper/stamp_tabs.html']


class CustomersApi(ListBulkCreateAPIView):

    model = mymodels.Customer
    paginate_by = 10


class CustomersDelApi(BulkDestroyAPIView):

    model = mymodels.Customer

    def allow_bulk_destroy(self, qs, filtered):
        return qs is filtered


class StampsApi(ListBulkCreateAPIView):

    model = mymodels.Stamp
    paginate_by = 10
