# -*- coding: utf-8 -*-
import datetime
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

from jmb.core.middleware.thread_local import get_current_user
from jmb.core.db.fields import *

class DateModel(models.Model):

    date_create      = models.DateTimeField( verbose_name=_('date create'), blank=True, null=True)
    date_last_modify = models.DateTimeField( verbose_name=_('date last modify'), blank=True, null=True )

    class Meta:
        abstract = True

    def save(self, force_insert=False, force_update=False, using=None, **kw):
        now = datetime.datetime.now()
        if not self.pk:
            self.date_create = now
        self.date_last_modify = now
        super(DateModel, self).save(force_insert=force_insert, force_update=force_update, **kw)

STATUS_CODES = (
    (0, _('Inactive')),
    (1, _('Active')),
)
class StatusModel(models.Model):

    status = models.IntegerField(choices=STATUS_CODES, max_length=3, default=1, verbose_name=_('Status'), help_text=None, null=True)

    class Meta:
        abstract = True

class DefaultModel(models.Model):

    default = models.BooleanField( default=False, verbose_name=_('Default'), )

    class Meta:
        abstract = True

class OrderedModel(models.Model):

    ordering = models.IntegerField(
        default=0,
        verbose_name=_('ordering'),
    )

    class Meta:
        abstract = True

    def brothers_and_me(self):
        return self._default_manager.all()

    def brothers(self):
        return self.brothers_and_me().exclude(pk=self.id)

    def is_first(self):
        return self.brothers_and_me().order_by('ordering')[0:1][0] == self

    def is_last(self):
        return self.brothers_and_me().order_by('-ordering')[0:1][0] == self

    def _switch_node(self, other):
        self.ordering, other.ordering = other.ordering, self.ordering
        self.save()
        other.save()

    def up(self):
        brothers = self.brothers().order_by('-ordering').filter(ordering__lt=self.ordering+1)[0:1]
        if not brothers.count():
            return False
        if brothers[0].ordering == self.ordering:
            self._set_default_ordering()
            self.save()
        self._switch_node(brothers[0])
        return True

    def down(self):
        brothers = self.brothers().order_by('ordering').filter(ordering__gt=self.ordering-1)[0:1]
        if not brothers.count():
            return False
        brother = brothers[0]
        if brother.ordering == self.ordering:
            brother._set_default_ordering()
            brother.save()
        self._switch_node(brother)
        return True

    def _set_default_ordering(self):
        max = 0
        brothers = self.brothers()
        if brothers.count():
            for brother in brothers:
                if brother.ordering >= max:
                    max = brother.ordering
        self.ordering = max + 1

    def save(self, force_insert=False, force_update=False, using=None, **kw):
        if not self.ordering:
            self.ordering = 0
        super(OrderedModel, self).save(force_insert=force_insert, force_update=force_update, using=using, **kw)

class TreeOrderedModel(OrderedModel):

    parent = models.ForeignKey( 'self', db_index=True, blank=True, null=True,
                                related_name='children', verbose_name=_('parent node'),
                                help_text=_('parent node'),)

    class Meta:
        abstract = True

    def brothers_and_me(self):
        if self.parent:
            return self._default_manager.filter(parent=self.parent)
        else:
            return self._default_manager.filter(parent__isnull=True)

class UserModel(models.Model):

    creator        = models.ForeignKey( User, blank=True, null=True, db_index = True, related_name = "%(app_label)s_%(class)s_creator", verbose_name = _("creator"),)
    last_modifier  = models.ForeignKey( User, blank=True, null=True, db_index = True, related_name = '%(app_label)s_%(class)s_last_modifier', verbose_name = _("last modifier"),)

    class Meta:
        abstract = True

    def save(self, user=None, force_insert=False, force_update=False, using=None, **kw):
        if not isinstance(user, User):
            user = get_current_user()
        if isinstance(user, User):
            if not self.id:
                self.creator = user
            self.last_modifier = user
        super(UserModel, self).save(force_insert=force_insert, force_update=force_update, using=None, **kw)

class SEOModel(models.Model):
    meta_description = models.TextField(
        _("description"), max_length=255, blank=True, null=True
    )
    meta_keywords = models.CharField(
        _("keywords"), max_length=255, blank=True, null=True
    )
    page_title = models.CharField(
        _("title"), max_length=255, blank=True,
        null=True, help_text=_("overwrite the title (html title tag)")
    )

    class Meta:
        abstract = True

