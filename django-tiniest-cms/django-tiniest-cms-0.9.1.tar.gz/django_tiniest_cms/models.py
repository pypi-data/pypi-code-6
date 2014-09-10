from django.db import models
from django.core.cache import cache

class Content(models.Model):
    name = models.CharField(max_length=512, unique=True)
    content = models.TextField()

    def save(self, *args, **kwargs):
        key = 'tiniest-content-{0}'.format(self.name)
        cache.delete(key)
        return super(Content, self).save(*args, **kwargs)
