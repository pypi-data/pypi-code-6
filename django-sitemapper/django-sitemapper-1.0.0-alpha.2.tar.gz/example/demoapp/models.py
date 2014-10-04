from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext as _


@python_2_unicode_compatible
class Demo(models.Model):

    title = models.CharField(_('title'), max_length=60)
    slug = models.SlugField(_('slug'), unique=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('demoapp.views.detail', kwargs={
            'slug': self.slug,
            })
