# -*- coding: utf-8 -*-
"""
.. module:: huron.pages.views
   :platform: Unix
   :synopsis: Pages application for Django - views module

.. moduleauthor:: Thomas Durey <tominardi@gmail.com>
"""
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404

from huron.pages.models import Page
from huron.pages import get_page_by_slug


def page(request, page_slug):
    """

    Render a page with the page template ``page.html`` from the website with
    the page context of the page asked.

    :param slug: Slug of the page asked
    :type slug: str
    :returns: page
    :rtype: Page object

    .. note::
        To know more about context informations send, please check the
        model :py:class:`huron.pages.models.Page`

    """
    variables = {}
    select_page = get_page_by_slug(page_slug)

    variables['page'] = select_page
    request_context = RequestContext(request, variables)

    return render_to_response('pages/single.html',
                              context_instance=request_context)
