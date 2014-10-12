from django.db import models
from django.contrib.contenttypes.generic import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.timezone import now


class TimeStamped(models.Model):
    """ Provides created and updated timestamps on models. """

    created = models.DateTimeField(null=True, editable=False)
    updated = models.DateTimeField(null=True, editable=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        _now = now()
        self.updated = _now
        if not self.id:
            self.created = _now
        super(TimeStamped, self).save(*args, **kwargs)


class Tag(TimeStamped):
    key = models.CharField(max_length=50, db_index=True)

    def __unicode__(self):
        return u"%s %d" % (self.key, self.pk)


class KeyValue(models.Model):
    tag = models.ForeignKey(Tag, related_name='kv_pairs', db_index=True)
    key = models.CharField(max_length=50, db_index=True)
    value = models.CharField(max_length=100)

    def __unicode__(self):
        return u"%s:%s" % (self.key, self.value)

    class Meta:
        unique_together = (('tag', 'key'),)


class TaggedItem(TimeStamped):
    """ Binds tags with generic models. """
    tag = models.ForeignKey(Tag, related_name='items', null=True)
    object_id = models.IntegerField(db_index=True)
    content_type = models.ForeignKey(ContentType)
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        unique_together = (('tag', 'object_id', 'content_type'),)

    def __unicode__(self):
        return u"%s - %s" % (self.content_object, self.tag)