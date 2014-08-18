from __future__ import unicode_literals

import json

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from model_utils.managers import InheritanceManager

from datasources.models import Datasource


@python_2_unicode_compatible
class WidgetBase(models.Model):
    label = models.CharField(max_length=128, verbose_name=_('Label'))
    datasource = models.ForeignKey(Datasource, null=True, blank=True, verbose_name=_('Datasource'))

    python_code = models.TextField(blank=True, verbose_name=_('Python'), help_text=_('Python code block executed after fetching the data from the datasource. An "original_data" variable is passed to the script and a "python_data" variable is expected. This code is executed at the server.'))
    python_enabled = models.BooleanField(default=False, verbose_name=_('Python enabled'))
    javascript_code = models.TextField(blank=True, verbose_name=_('Javascript'), help_text=_('Javascript code block executed after the Python code executes. An "original_data" variable is passed to the script, and should return a "data" value. This code is executed at the browser.'))
    javascript_enabled = models.BooleanField(default=True, verbose_name=_('Javascript enabled'))

    objects = InheritanceManager()

    def __str__(self):
        subclass = WidgetBase.objects.get_subclass(pk=self.pk)
        return '%s (%s)' % (subclass.label, subclass.widget_type)

    def get_data(self):
        if self.datasource:
            original_data = self.datasource.get()
        else:
            original_data = {}

        if self.python_enabled:
            result = {}
            exec(self.python_code, {'original_data': original_data}, result)
            original_data = result['python_data']

        return original_data

    def get_context(self):
        context = {
            'javascript_code': self.javascript_code,
            'javascript_enabled': self.javascript_enabled,
            'original_data': self.get_data(),
            'original_data_json': json.dumps(self.get_data()),
        }
        return context

    class Meta:
        ordering = ('label',)


class ExpressionWidget(WidgetBase):
    template_name = 'widgets/expression/base.html'
    widget_type = _('Expression')


class WebsiteWidget(WidgetBase):
    template_name = 'widgets/website/base.html'
    widget_type = _('Website')

    load_content = models.BooleanField(default=False, verbose_name=_('Load content'), help_text=_('The widget will load the content of the website as pass it as a base64 encoded string to the iframe, relative asset path will not work.'))

    def get_context(self):
        context = {
            'content': self.datasource.get().content.encode('base64'),
            'javascript_code': self.javascript_code,
            'javascript_enabled': self.javascript_enabled,
            'load_content': self.load_content,
            'url': self.datasource.get_full_url(),
        }
        return context


class MessageWidget(WidgetBase):
    template_name = 'widgets/message/base.html'
    widget_type = _('Message')

    message = models.TextField(verbose_name=_('Message'))

    def get_context(self):
        context = {
            'message': self.message,
        }
        return context


class NovusLineChartWidget(WidgetBase):
    template_name = 'widgets/novus/linechart.html'
    widget_type = _('Novus line chart')


class JustgageWidget(WidgetBase):
    template_name = 'widgets/justgage/base.html'
    widget_type = _('Justgage gauge widget')

    title = models.CharField(blank=True, max_length=48, verbose_name=_('Title'))
    minimum = models.IntegerField(default=0, verbose_name=_('Minimum'))
    maximum = models.IntegerField(default=100, verbose_name=_('Maximum'))
    legend = models.CharField(max_length=48, verbose_name=_('Legend'))

    def get_context(self):
        context = super(JustgageWidget, self).get_context()
        context.update({
            'legend': self.legend,
            'maximum': self.maximum,
            'minimum': self.minimum,
            'title': self.title,
        })
        return context


class ChartJSWidget(WidgetBase):
    labels_element = models.CharField(blank=True, max_length=64, verbose_name=_('Labels element'))
    data_element = models.CharField(blank=True, max_length=64, verbose_name=_('Data element'))

    def get_context(self):
        context = super(ChartJSWidget, self).get_context()

        if self.datasource:
            result = {
                'labels': [result[self.labels_element] for result in context['original_data']],
                'datasets': [
                    {
                        'data': [result[self.data_element] for result in context['original_data']],
                   }
               ]
            }

            context.update({
                'original_data': json.dumps(result),
            })
        return context

    class Meta:
        abstract = True


class ChartJSLineWidget(ChartJSWidget):
    template_name = 'widgets/chartjs/line.html'
    widget_type = _('ChartJS line chart widget')


class ChartJSBarWidget(ChartJSWidget):
    template_name = 'widgets/chartjs/bar.html'
    widget_type = _('ChartJS bar chart widget')


class ChartJSRadarWidget(ChartJSWidget):
    template_name = 'widgets/chartjs/radar.html'
    widget_type = _('ChartJS radar chart widget')


class ChartJSPieWidget(ChartJSWidget):
    template_name = 'widgets/chartjs/pie.html'
    widget_type = _('ChartJS pie chart widget')

    def get_context(self):
        context = {
            'javascript_code': self.javascript_code,
            'javascript_enabled': self.javascript_enabled,
            'original_data': self.get_data(),
            'original_data_json': json.dumps(self.get_data()),
        }

        if self.datasource:
            result = [{'label': result[self.labels_element], 'value': result[self.data_element]} for result in context['original_data']]

            context.update({
                'original_data': json.dumps(result),
            })
        return context


class ChartJSDoughnutWidget(ChartJSPieWidget):
    template_name = 'widgets/chartjs/doughnut.html'
    widget_type = _('ChartJS doughnut chart widget')
