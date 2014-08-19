import operator
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.shortcuts import resolve_url

from feincms.models import create_base_model
from feincms.utils.managers import ActiveAwareContentManagerMixin
from feincms.module.mixins import ContentModelMixin


@python_2_unicode_compatible
class AbstractBlog(models.Model):
    class Meta(object):
        abstract = True
        ordering = 'name',

    name = models.CharField(_('name'), max_length=255, unique=True)
    slug = models.SlugField(_('slug'), unique=True)

    def __str__(self):
        return self.name


class PostManager(ActiveAwareContentManagerMixin, models.Manager):
    def after(self, post):
        filters = [Q(date__gt=post.date)]
        if post.time is not None:
            filters.append(Q(date=post.date, time__gt=post.time))
            filters.append(Q(date=post.date, time=post.time, id__gt=post.id))
        else:
            filters.append(Q(date=post.date, time__isnull=False))
            filters.append(Q(date=post.date, time__isnull=True, id__gt=post.id))

        return self.filter(reduce(operator.or_, filters))

    def before(self, post):
        filters = [Q(date__lt=post.date)]
        if post.time is not None:
            filters.append(Q(date=post.date, time__isnull=True))
            filters.append(Q(date=post.date, time__lt=post.time))
            filters.append(Q(date=post.date, time=post.time, id__lt=post.id))
        else:
            filters.append(Q(date=post.date, time__isnull=True, id__lt=post.id))

        return self.filter(reduce(operator.or_, filters))

PostManager.add_to_active_filters(Q(published=True))


@python_2_unicode_compatible
class AbstractPost(create_base_model(), ContentModelMixin):
    class Meta(object):
        abstract = True
        unique_together = (
            ('blog', 'slug', 'date'),
        )
        ordering = '-date', '-time', '-id'

    blog = models.ForeignKey(
        'Blog',
        related_name='posts',
        verbose_name=_('blog'),
        on_delete=models.PROTECT,
    )
    title = models.CharField(_('title'), max_length=255)
    slug = models.SlugField(_('slug'))
    published = models.BooleanField(_('published'), default=True)
    date = models.DateField(
        _('date'),
        default=lambda: timezone.localtime(timezone.now()).date(),
    )
    time = models.TimeField(
        _('time'),
        default=lambda: timezone.localtime(timezone.now()).time(),
        null=True, blank=True
    )

    objects = PostManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return resolve_url("blogs:post_permalink", pk=self.pk)

    def get_pretty_url(self):
        return reverse(
            "blogs:post",
            args=[
                self.blog.slug,
                self.date.year,
                self.date.month,
                self.date.day,
                self.slug,
            ]
        )

    def next(self):
        return self.blog.posts.after(self).last()

    def previous(self):
        return self.blog.posts.before(self).first()
