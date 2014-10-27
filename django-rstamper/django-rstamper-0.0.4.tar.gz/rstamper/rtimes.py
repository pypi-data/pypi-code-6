# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

from django.utils.translation import ugettext_lazy as _
from django.utils import timezone


HOURS_DAY = 8
SECS_DAY = HOURS_DAY * 60 * 60
DATETIME_FORMAT = '%Y-%m-%d %H:%M'


def worktime(start, end):

    worktime = (datetime.strptime(end, DATETIME_FORMAT) -
                datetime.strptime(start, DATETIME_FORMAT))
    return worktime.seconds


def humanize_time(secs):
    mins, secs = divmod(secs, 60)
    hours, mins = divmod(mins, 60)

    return '%02d:%02d' % (hours, mins)


def humanize_time_day(secs):
    totalDays, remaining = divmod(secs, SECS_DAY)
    remainingMin, remainingSec = divmod(remaining, (60))
    remainingHr, remainingMin = divmod(remainingMin, (60))

    secs, sec = divmod(secs, 60)
    hr, min = divmod(secs, 60)
    return "%d:%02d hours. = %d days, remaining: %d:%02d (%d hours/day)" % (
        hr, min, totalDays, remainingHr, remainingMin, HOURS_DAY)


def date_range(start, end):
    r = (end+timedelta(days=1)-start).days
    return [start+timedelta(days=i) for i in range(r)]
