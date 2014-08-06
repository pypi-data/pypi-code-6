# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

import datetime

from django import template
from django.db.models import F
from django.utils.dateformat import format

from djapps.blogs.models import Blog, Post

register = template.Library()


@register.assignment_tag
def blog_years(blog, order='DESC'):
    if not blog:
        qsroot = Post.objects
    else:
        qsroot = blog.posts

    qs = qsroot.active().dates('date', 'year', order=order)
    return [dt.year for dt in qs]


@register.assignment_tag
def blog_months(blog, date=None, year=None, order='DESC'):
    if not blog:
        qsroot = Post.objects
    else:
        qsroot = blog.posts

    if date:
        year = date.year
    elif not year:
        return

    qs = qsroot.active().filter(
        date__year=year,
    ).dates('date', 'month', order=order)
    return [dt.month for dt in qs]


@register.assignment_tag
def blog_days(blog, date=None, year=None, month=None, order='DESC'):
    if not blog:
        qsroot = Post.objects
    else:
        qsroot = blog.posts

    if date:
        year = date.year
        month = date.month
    elif not year or not month:
        return

    qs = qsroot.active().filter(
        date__year=year,
        date__month=month,
    ).dates('date', 'day', order=order)
    return [dt.day for dt in qs]

@register.assignment_tag(takes_context=True)
def blogs_available(context):
    return Blog.objects.all()

@register.assignment_tag(takes_context=True)
def blogs_current_blog(context):
    try:
        return context['request']._blogs_current_blog
    except:
        pass

@register.assignment_tag(takes_context=True)
def blogs_current_date(context):
    try:
        return context['request']._blogs_current_date
    except:
        pass

@register.assignment_tag(takes_context=True)
def blogs_current_year(context):
    try:
        return context['request']._blogs_current_year
    except:
        pass

@register.assignment_tag(takes_context=True)
def blogs_current_month(context):
    try:
        return context['request']._blogs_current_month
    except:
        pass

@register.assignment_tag(takes_context=True)
def blogs_current_day(context):
    try:
        return context['request']._blogs_current_day
    except:
        pass

@register.filter()
def month_name(month_number):
    date = datetime.date(year=2000, month=int(month_number), day=1)
    return format(date, "F")
