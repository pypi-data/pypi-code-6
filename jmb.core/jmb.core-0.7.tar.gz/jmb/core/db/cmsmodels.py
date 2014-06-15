# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

class StatusModel(models.Model):
    """
    Abstract class that add a status field to CMSPlugin subclasses. To be inherited
    while subclassing CMSPlugin class
    """
    status = models.BooleanField(
        verbose_name=_("Active"),
        default=True,
        help_text=_("if not checked, plugin content will not be rendered"))

    class Meta:
        abstract = True


class WrapModel(models.Model):
    """
    Abstract class that add a wrap field to CMSPlugin subclasses. To be inherited
    while subclassing CMSPlugin class
    """
    wrap = models.BooleanField(
        verbose_name=_("Wrap content"),
        default=False,
        help_text=_("if checked, plugin content will be rendered inside a container div"))

    container_id = models.SlugField(
        verbose_name=_("id"),
        max_length=150,
        null=True, blank=True,
        default=None,
        help_text=_("(Optional) if populated, the container will have this id instead of the default")
    )

    container_classes = models.CharField(
        verbose_name=_("classes"),
        max_length=200,
        null=True, blank=True,
        default=None,
        help_text=_("(Optional) if populated, these classes will be added to container"),
    )

    class Meta:
        abstract = True
