# -*- coding: utf-8 -*-
from aldryn_blog.models import Post
from django import template
from django.core.urlresolvers import reverse

register = template.Library()


@register.filter
def posts(latest, objects):
    if latest:
        return latest
    return objects


@register.filter
def user_name(user):
    if user.get_full_name():
        return user.get_full_name()
    return user.username


@register.assignment_tag
def get_blog_post_tags(post):
    """
    Returns a list of tags for post, with an extra url attribute.
    """
    post_tags = list(post.tags.all())

    for tag in post_tags:
        tag.get_absolute_url = reverse('aldryn_blog:tagged-posts', kwargs={'tag': tag.slug})
    return post_tags


@register.assignment_tag
def get_related_posts(post, by_categories=True, by_tags=True, by_latest=True, order_by_relativity=True, count=5):
    """
    Returns a list of blog objects being related to the one given.

    "Related" can mean one or multiple of the following (being configurable by the arguements passed to this function):
    - In the same category
    - Having one or more tags in common
    - Just being released recently

    order_by_relativity will return the posts in an order in which they are relevant to the one given. (Same Category >
    tags in common, released recently). Passing False will cause the posts to be ordered by their publish date.
    """

    given_category = post.category_id
    given_tags = post.tags.values_list('pk', flat=True)
    given_language = post.language

    qs = Post.objects.filter(language=given_language)

    if by_categories:
        qs2 = qs.filter(category_id=given_category)

        if qs2.count == count:
            return qs2




    if len(found) >= count:
        return found[:count]

    if by_tags:
        found += list(qs.filter())

