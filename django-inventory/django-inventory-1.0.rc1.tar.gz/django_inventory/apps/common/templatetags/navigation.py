from __future__ import absolute_import

import types

from django.conf import settings
from django.core.urlresolvers import resolve, reverse, NoReverseMatch
from django.core.urlresolvers import (RegexURLResolver, RegexURLPattern,
                                      Resolver404, get_resolver)
from django.template import (TemplateSyntaxError, Library,
                             VariableDoesNotExist, Node, Variable)
from django.utils.text import unescape_string_literal

from ..api import object_navigation, menu_links as menu_navigation

register = Library()


def process_links(links, view_name, url):
    items = []
    active_item = None
    for item, count in zip(links, range(len(links))):
        item_view = 'view' in item and item['view']
        item_url = 'url' in item and item['url']
        if view_name == item_view or url == item_url:
            active = True
            active_item = item
        else:
            active = False
            if 'links' in item:
                for child_link in item['links']:
                    child_view = 'view' in child_link and child_link['view']
                    child_url = 'url' in child_link and child_link['url']
                    if view_name == child_view or url == child_url:
                        active = True
                        active_item = item

        items.append(
            {
                'first': count == 0,
                'active': active,
                'url': item_view and reverse(item_view) or item_url or '#',
                'text': unicode(item['text']),
                'famfam': 'famfam' in item and item['famfam'],
            }
        )
    return items, active_item


class NavigationNode(Node):
    def __init__(self, navigation, *args, **kwargs):
        self.navigation = navigation

    def render(self, context):
        request = Variable('request').resolve(context)
        view_name = resolve(request.META['PATH_INFO']).view_name

        main_items, active_item = process_links(links=self.navigation, view_name=view_name, url=request.META['PATH_INFO'])
        context['navigation_main_links'] = main_items
        if active_item and 'links' in active_item:
            secondary_links, active_item = process_links(links=active_item['links'], view_name=view_name, url=request.META['PATH_INFO'])
            context['navigation_secondary_links'] = secondary_links
        return ''


@register.tag
def main_navigation(parser, token):
    args = token.split_contents()
    return NavigationNode(navigation=menu_navigation)


def resolve_arguments(context, src_args):
    args = []
    kwargs = {}
    if type(src_args) == type([]):
        for i in src_args:
            val = resolve_template_variable(context, i)
            if val:
                args.append(val)
    elif type(src_args) == type({}):
        for key, value in src_args.items():
            val = resolve_template_variable(context, value)
            if val:
                kwargs[key] = val
    else:
        val = resolve_template_variable(context, src_args)
        if val:
            args.append(val)

    return args, kwargs


def resolve_links(context, links, current_view, current_path):
    context_links = []
    for link in links:
        args, kwargs = resolve_arguments(context, link.get('args', {}))

        if 'view' in link:
            link['active'] = link['view'] == current_view
            args, kwargs = resolve_arguments(context, link.get('args', {}))

            try:
                if kwargs:
                    link['url'] = reverse(link['view'], kwargs=kwargs)
                else:
                    link['url'] = reverse(link['view'], args=args)
            except NoReverseMatch, err:
                link['url'] = '#'
                link['error'] = err
        elif 'url' in link:
            link['active'] = link['url'] == current_path
        else:
            link['active'] = False
        context_links.append(link)

    return context_links


def _get_object_navigation_links(context, menu_name=None):
    current_path = Variable('request').resolve(context).META['PATH_INFO']
    current_view = resolve(current_path).view_name
    context_links = []

    try:
        object_name = Variable('navigation_object_name').resolve(context)
    except VariableDoesNotExist:
        object_name = 'object'

    try:
        obj = Variable(object_name).resolve(context)
    except VariableDoesNotExist:
        obj = None

    try:
        links = object_navigation[menu_name][current_view]['links']
        for link in resolve_links(context, links, current_view, current_path):
            context_links.append(link)
    except KeyError:
        pass

    try:
        links = object_navigation[menu_name][type(obj)]['links']
        for link in resolve_links(context, links, current_view, current_path):
            context_links.append(link)
    except KeyError:
        pass

    return context_links


def resolve_template_variable(context, name):
    try:
        return unescape_string_literal(name)
    except ValueError:
        return Variable(name).resolve(context)
    except TypeError:
        return name


class GetNavigationLinks(Node):
    def __init__(self, *args):
        self.menu_name = None
        if args:
            self.menu_name = args[0]

    def render(self, context):
        menu_name = resolve_template_variable(context, self.menu_name)
        context['object_navigation_links'] = _get_object_navigation_links(context, menu_name)
        return ''


@register.tag
def get_object_navigation_links(parser, token):
    args = token.split_contents()
    return GetNavigationLinks(*args[1:])


@register.inclusion_tag('generic_views/generic_navigation.html', takes_context=True)
def object_navigation_template(context):
    return {
        'horizontal': True,
        'object_navigation_links': _get_object_navigation_links(context)
    }
    return new_context
