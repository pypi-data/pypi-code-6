from django.db import models
from django_extensions.db.fields import UUIDField


class ModelWithDenormalisedChar(models.Model):

    title = models.CharField(max_length=60)
    uuid = models.CharField(max_length=36, blank=True, editable=False)

    def __unicode__(self):
        return self.title


class ModelWithMonkeyPatchedUUID(models.Model):

    title = models.CharField(max_length=60)

    def __unicode__(self):
        return self.title


class ModelWithDenormalisedUUID(models.Model):

    title = models.CharField(max_length=60)
    uuid = UUIDField(auto=False, blank=True, null=True, unique=True)


class ModelWithDetatchedUUID(models.Model):

    title = models.CharField(max_length=60)


import uuidstore.registry
uuidstore.registry.register(ModelWithDenormalisedChar, uuid_descriptor='uuid')
uuidstore.registry.register(ModelWithMonkeyPatchedUUID, uuid_descriptor='uuid')
uuidstore.registry.register(ModelWithDenormalisedUUID, uuid_descriptor='uuid')
uuidstore.registry.register(ModelWithDetatchedUUID)
