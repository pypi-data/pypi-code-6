from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext as _


class EmailTemplate(models.Model):
    """
    The basic model is used to store the template email. Contains fields ``subject``. ``body``, ``slug``.
    Field ``slug`` is used as an identifier.
    """
    subject = models.TextField(verbose_name=_('subject'))
    body = models.TextField(verbose_name=_('body'))
    slug = models.SlugField(verbose_name=_('slug'))

    def __unicode__(self):
        return self.slug
