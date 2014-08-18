from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from .literals import DEFAULT_ELEMENT_HEIGHT
from .managers import DashboardElementManager

from widgets.models import WidgetBase


@python_2_unicode_compatible
class Dashboard(models.Model):
    label = models.CharField(max_length=96, verbose_name=_('Label'))
    description = models.TextField(blank=True, verbose_name=_('Description'))
    full_screen = models.BooleanField(default=False, verbose_name=_('Full screen'))
    order = models.PositiveIntegerField(blank=True, null=True, default=0, verbose_name=_('Order'))

    def __str__(self):
        return self.label

    def get_absolute_url(self):
        return reverse('dashboards:dashboard_view', args=[str(self.pk)])

    def get_element_rows(self):
        rows = []
        row = []
        spans = 0
        for element in self.elements.enabled():
            spans += element.span
            if spans > 12:
                rows.append(row)
                spans = element.span
                row = []

            row.append(element)

        if row:
            rows.append(row)

        return rows

    class Meta:
        ordering = ('order',)
        verbose_name = _('Dashboard')
        verbose_name_plural = _('Dashboards')


@python_2_unicode_compatible
class DashboardElement(models.Model):
    dashboard = models.ForeignKey(Dashboard, verbose_name=_('Dashboard'), related_name='elements')
    enabled = models.BooleanField(default=True, verbose_name=_('Enabled'))
    span = models.PositiveIntegerField(help_text=_('The amount of columns in a 12 columns layout that this element should occupy.'), verbose_name=_('Span'))
    height = models.PositiveIntegerField(default=DEFAULT_ELEMENT_HEIGHT, verbose_name=_('Height'))
    order = models.PositiveIntegerField(blank=True, null=True, default=0, verbose_name=_('Order'))
    widget = models.ForeignKey(WidgetBase, verbose_name=_('Widget'))

    objects = DashboardElementManager()

    def __str__(self):
        return self.widget.label

    class Meta:
        verbose_name = _('Dashboard element')
        verbose_name_plural = _('Dashboard elements')
        ordering = ('order',)
