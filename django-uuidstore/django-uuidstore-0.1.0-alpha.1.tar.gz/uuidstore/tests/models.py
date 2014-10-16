from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django_extensions.db.fields import UUIDField


@python_2_unicode_compatible
class ModelWithDetatchedUUID(models.Model):

    title = models.CharField(max_length=60)

    def __str__(self):
        return self.title


@python_2_unicode_compatible
class ModelWithMonkeyPatchedUUID(models.Model):

    title = models.CharField(max_length=60)

    def __str__(self):
        return self.title


@python_2_unicode_compatible
class ModelWithDenormalisedCharField(models.Model):

    title = models.CharField(max_length=60)
    uuid = models.CharField(
        max_length=36,
        blank=True,
        editable=False,
        )

    def __str__(self):
        return self.title


@python_2_unicode_compatible
class ModelWithDenormalisedUUIDField(models.Model):

    title = models.CharField(max_length=60)
    uuid = UUIDField(
        auto=False,
        blank=True,
        null=True,
        unique=True,
        editable=False,
        )

    def __str__(self):
        return self.title


from uuidstore.registry import register
register(ModelWithDetatchedUUID)
register(ModelWithMonkeyPatchedUUID, uuid_descriptor='uuid')
register(ModelWithDenormalisedCharField, uuid_descriptor='uuid')
register(ModelWithDenormalisedUUIDField, uuid_descriptor='uuid')
