# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from filer.fields.image import FilerImageField
from cmsplugin_cascade.models import CascadeModelBase


class ABImageElement(CascadeModelBase):
    """
    A model class to refer to a Django-Filer image together with Bootstrap elements data.
    """
    class Meta:
        db_table = 'cmsplugin_cascade_imageelement'

    image = FilerImageField(null=True, blank=True, default=None, verbose_name=_("Image"))
