#-*- coding: utf-8 -*-

import json

from django.views.generic import DetailView, ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import Http404, HttpResponse
from django.conf import settings
from django.contrib import messages

from spirit import utils
from spirit.models.topic import Topic
from spirit.utils.paginator.infinite_paginator import paginate

from spirit.models.topic_notification import TopicNotification
from spirit.forms.topic_notification import NotificationForm, NotificationCreationForm


@require_POST
@login_required
def notification_create(request, topic_id):
    topic = get_object_or_404(Topic.objects.for_access(request.user),
                              pk=topic_id)
    form = NotificationCreationForm(user=request.user, topic=topic, data=request.POST)

    if form.is_valid():
        form.save()
        return redirect(request.POST.get('next', topic.get_absolute_url()))
    else:
        messages.error(request, utils.render_form_errors(form))
        return redirect(request.POST.get('next', topic.get_absolute_url()))


@require_POST
@login_required
def notification_update(request, pk):
    notification = get_object_or_404(TopicNotification, pk=pk, user=request.user)
    form = NotificationForm(data=request.POST, instance=notification)

    if form.is_valid():
        form.save()
        return redirect(request.POST.get('next', notification.topic.get_absolute_url()))
    else:
        messages.error(request, utils.render_form_errors(form))
        return redirect(request.POST.get('next', notification.topic.get_absolute_url()))


@login_required
def notification_ajax(request):
    if not request.is_ajax():
        return Http404()

    notifications = TopicNotification.objects.for_access(request.user)\
        .order_by("is_read", "-date")\
        .select_related('comment__user', 'comment__topic')[:settings.ST_NOTIFICATIONS_PER_PAGE]

    notifications = [{'user': n.comment.user.username, 'action': n.action,
                      'title': n.comment.topic.title, 'url': n.get_absolute_url(),
                      'is_read': n.is_read}
                     for n in notifications]

    return HttpResponse(json.dumps({'n': notifications, }), content_type="application/json")


@login_required
def notification_list_unread(request):
    notifications = TopicNotification.objects.for_access(request.user)\
        .filter(is_read=False)

    page = paginate(request, query_set=notifications, lookup_field="date",
                    page_var='notif', per_page=settings.ST_NOTIFICATIONS_PER_PAGE)
    next_page_pk = None

    if page:
        next_page_pk = page[-1].pk

    return render(request, 'spirit/topic_notification/list_unread.html', {'page': page,
                                                                          'next_page_pk': next_page_pk})


@login_required
def notification_list(request):
    notifications = TopicNotification.objects.for_access(request.user)
    return render(request, 'spirit/topic_notification/list.html', {'notifications': notifications, })