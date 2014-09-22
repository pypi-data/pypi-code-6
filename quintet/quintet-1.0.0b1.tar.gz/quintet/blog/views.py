from datetime import datetime
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from quintet.models import Page, Post, Section, Tag


def list_posts(request, section=None, contributor=None,
               day=None, month=None, year=None, tag=None):
    posts = Post.objects.filter(status='P')
    filter_title = None

    if section:
        section = get_object_or_404(Section, slug=section)
        posts = posts.filter(section=section)
        filter_title = section.name

    if contributor:
        contributor = get_object_or_404(User, username=contributor)
        posts = posts.filter(contributors__user=contributor)
        filter_title = "Contributor: %s" % contributor.get_full_name()

    if day:
        posts = posts.filter(date_published__day=day)

    if month:
        month_datetime = datetime.strptime(month, '%b')
        month = month_datetime.month
        display_month = datetime.strftime(month_datetime, '%b')
        posts = posts.filter(date_published__month=month)

    if month and not year:
        year = datetime.now().year

    if year:
        posts = posts.filter(date_published__year=year)
        filter_title = "Date: %s" % year

    if month and year:
        filter_title = "Date: %s %s" % (display_month, year)

    if day and month and year:
        filter_title = "Date: %s %s %s" % (day, display_month, year)

    if tag:
        tag = Tag.objects.filter(slug=tag)
        posts = posts.filter(tags__contains=tag)
        filter_title = "Tag: %s" % tag[0].title

    return render(request, 'list.html', {
        'pages': Page.objects.filter(status='P'),
        'sections': Section.objects.all(),
        'section': section,
        'posts': posts[:10],
        'filter_title': filter_title,
    })


def view_post(request, section, post):
    post = get_object_or_404(Post, section__slug=section, slug=post)

    return render(request, 'post.html', {
        'pages': Page.objects.filter(status='P'),
        'sections': Section.objects.all(),
        'current_section': post.section,
        'post': post,
    })


def view_page(request, slug):
    page = get_object_or_404(Page, slug=slug)

    return render(request, 'page.html', {
        'pages': Page.objects.filter(status='P'),
        'sections': Section.objects.all(),
        'page': page,
    })
