from __future__ import unicode_literals

from furl import furl
import requests

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from .literals import DATASOURCE_FORMAT_CHOICES, DATASOURCE_FORMAT_JSON

SMART_MODE = False


@python_2_unicode_compatible
class Host(models.Model):
    label = models.CharField(verbose_name=_('Label'), max_length=64)
    netloc = models.CharField(verbose_name=_('Network Location Part'), max_length=255, help_text=_('Enter the scheme, username, password, host and port. For example: http://username:password@host:port'))

    def __str__(self):
        return self.label

    class Meta:
        verbose_name = _('Host')
        verbose_name_plural = _('Hosts')


@python_2_unicode_compatible
class Datasource(models.Model):
    host = models.ForeignKey(Host, verbose_name=_('Host'))
    label = models.CharField(verbose_name=_('Label'), max_length=96)
    description = models.TextField(blank=True, verbose_name=_('Description'))
    path = models.TextField(verbose_name=_('Path'), help_text=_('Enter the URL path, query and fragment. For example: /very-long-url-path/?argument=value&second-argument=value'))
    data_format = models.PositiveIntegerField(choices=DATASOURCE_FORMAT_CHOICES, verbose_name=_('Data format'))
    python_code = models.TextField(blank=True, verbose_name=_('Python'), help_text=_('Python code block executed after fetching the data from the datasource. An "original_data" variable is passed to the script and a "python_data" variable is expected. This code is executed at the server.'))
    python_enabled = models.BooleanField(default=False, verbose_name=_('Python enabled'))

    def __str__(self):
        return self.label

    def get(self):
        response = requests.get(self.get_full_url())
        if self.data_format == DATASOURCE_FORMAT_JSON:
            data = response.json()
        else:
            data = response.content

        if self.python_enabled:
            result = {}
            exec(self.python_code, {'original_data': data}, result)
            data = result['python_data']

        return data

    def get_full_url(self):
        if SMART_MODE:
            f = furl(self.host.netloc)
            f.path = self.path
            f.path.normalize()
            return f.url
        else:
            return '{}{}'.format(self.host.netloc, self.path)

    class Meta:
        ordering = ('label',)
        verbose_name = _('Datasource')
        verbose_name_plural = _('Datasources')
