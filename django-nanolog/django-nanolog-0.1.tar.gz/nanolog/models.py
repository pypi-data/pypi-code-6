from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.generic import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User


class Nanolog(models.Model):
    user = models.ForeignKey(User, verbose_name=_(u"User"), blank=True, null=True, on_delete=models.SET_NULL, db_index=True)
    log_type = models.CharField(_('Log type'), max_length=255, db_index=True)
    details = models.CharField(_('Details'), max_length=255)
    ip = models.GenericIPAddressField(_('Ip'), null=True, blank=True)
    note = models.TextField(_('Note'), null=True, blank=True)

    content_type = models.ForeignKey(ContentType, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    created_date = models.DateTimeField(_('created date'), auto_now_add=True)

    class Meta:
        ordering = ['-created_date']

    def __unicode__(self):
        return " - ".join((unicode(self.school), unicode(self.created_date)))
