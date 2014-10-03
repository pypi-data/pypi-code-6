# Python
from decimal import Decimal

# Django
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.functional import cached_property
from django.utils.translation import ugettext as _

try:
    from django.contrib.contenttypes.fields import GenericForeignKey
except ImportError:
    from django.contrib.contenttypes.generic import GenericForeignKey


@python_2_unicode_compatible
class SitemapEntry(models.Model):

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    CHANGEFREQS = (
        (10, 'always'),
        (20, 'hourly'),
        (30, 'daily'),
        (40, 'weekly'),
        (50, 'monthly'),
        (60, 'yearly'),
        (70, 'never'),
    )
    changefreq = models.PositiveSmallIntegerField(
        _('Change frequency'),
        choices=CHANGEFREQS,
        )

    PRIORITY_CHOICES = (
        (Decimal('0.0'), '0.0'),
        (Decimal('0.1'), '0.1'),
        (Decimal('0.2'), '0.2'),
        (Decimal('0.3'), '0.3'),
        (Decimal('0.4'), '0.4'),
        (Decimal('0.5'), '0.5'),
        (Decimal('0.6'), '0.6'),
        (Decimal('0.7'), '0.7'),
        (Decimal('0.8'), '0.8'),
        (Decimal('0.9'), '0.9'),
        (Decimal('1.0'), '1.0'),
        )
    priority = models.DecimalField(
        _('priority'),
        max_digits=2, decimal_places=1,
        choices=PRIORITY_CHOICES
        )

    class Meta:
        unique_together = (['content_type', 'object_id'],)
        verbose_name = _('Sitemap entry')
        verbose_name_plural = _('Sitemap entries')

    def __str__(self):
        return str(self.content_object)


class SitemappedModel(object):

    @cached_property
    def sitemap_entry(self):
        ctype = ContentType.objects.get_for_model(self.__class__)
        try:
            sitemap = SitemapEntry.objects.get(
                content_type__pk=ctype.id,
                object_id=self.id
                )
        except:
            sitemap = None
        return sitemap
