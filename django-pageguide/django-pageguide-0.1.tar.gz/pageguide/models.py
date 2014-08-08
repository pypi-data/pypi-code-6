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

from django.db import models
from django.utils.translation import ugettext_lazy as _


class PageGuide(models.Model):
    target_url = models.CharField(max_length=200, verbose_name=_(u'Target URL'),
                                  help_text=_('Should be a regular expression, like ^/pages/\w+/$'))
    title = models.CharField(max_length=200, verbose_name=_(u'Title'))

    class Meta:
        verbose_name = _('Page guide')

    def __unicode__(self):
        return self.title


class PageGuideStep(models.Model):
    pageguide = models.ForeignKey(PageGuide, verbose_name=_('Page guide'))
    order = models.PositiveIntegerField(verbose_name=u'Order in the guide')
    css_selector = models.CharField(max_length=200, verbose_name=_(u'CSS selector'))
    html_content = models.TextField(verbose_name=_(u'Help content'))

    class Meta:
        verbose_name = _('Page guide')
        ordering = ('order', )

    def __unicode__(self):
        return self.css_selector
