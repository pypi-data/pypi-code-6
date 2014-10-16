# Django
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext as _

try:
    from django.contrib.contenttypes.fields import GenericForeignKey
except ImportError:
    from django.contrib.contenttypes.generic import GenericForeignKey

# 3rd-party
from django_extensions.db.fields import UUIDField


class ObjectUUIDManager(models.Manager):

    def get_for_instance(self, instance):
        ctype = ContentType.objects.get_for_model(instance)
        try:
            obj = self.get(content_type=ctype, object_id=instance.id)
        except self.model.DoesNotExist:
            return
        return obj


@python_2_unicode_compatible
class ObjectUUID(models.Model):
    """Link a model instance with a UUID
    """

    uuid = UUIDField(verbose_name=_('UUID'), primary_key=True, auto=True)
    content_type = models.ForeignKey(
        ContentType,
        verbose_name=_('content type')
        )
    object_id = models.PositiveIntegerField(_('object id'))
    content_object = GenericForeignKey('content_type', 'object_id')

    # Managers
    objects = ObjectUUIDManager()

    class Meta:
        unique_together = (('object_id', 'content_type'),)

    def __str__(self):
        return str(self.uuid)
