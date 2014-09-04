# Copyright (C) 2012 by Dr. Dieter Maurer <dieter@handshake.de>
# All rights resevered -- see "LICENSE.txt" for details.
"""Wrapping necessary to work around `formlib` integration weaknesses."""

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from ..search import SimpleSearch as BaseSimpleSearch


class SimpleSearch(BaseSimpleSearch):
  base_template = BaseSimpleSearch.template
  template = ViewPageTemplateFile("form_template.pt")
