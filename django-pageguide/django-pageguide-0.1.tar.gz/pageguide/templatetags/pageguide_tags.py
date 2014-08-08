# Copyright (c) 2014 by Manuel Saelices
#
# This file is part of django-pageguide
#
# django-pageguide is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# django-pageguide is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with django-pageguide.  If not, see <http://www.gnu.org/licenses/>.

import re

from django import template
from django.conf import settings

from pageguide.models import PageGuide

register = template.Library()


@register.inclusion_tag('pageguide/pageguide_css.html', takes_context=True)
def pageguide_css(context):
    return {'STATIC_URL': settings.STATIC_URL}


@register.inclusion_tag('pageguide/pageguide_js.html', takes_context=True)
def pageguide_js(context):
    return {'STATIC_URL': settings.STATIC_URL}



@register.inclusion_tag('pageguide/pageguide.html', takes_context=True)
def pageguide(context):
    request = context['request']
    matched_pages = []
    for page in PageGuide.objects.all():
        if re.match(page.target_url, request.path):
            matched_pages.append(page)
    return {
        'pageguides': matched_pages,
        'STATIC_URL': settings.STATIC_URL,
    }
