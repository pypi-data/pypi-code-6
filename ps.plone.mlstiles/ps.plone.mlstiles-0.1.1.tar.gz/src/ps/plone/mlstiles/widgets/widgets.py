# -*- coding: utf-8 -*-
"""Custom widget implementations."""

# zope imports
from z3c.form import interfaces
from z3c.form.browser.text import TextWidget
from z3c.form.widget import FieldWidget
import zope.component
import zope.interface
import zope.schema

# local imports
from .interfaces import IListingTextWidget


@zope.interface.implementer_only(IListingTextWidget)
class ListingTextWidget(TextWidget):
    """Listing text widget implementation."""


@zope.component.adapter(
    zope.schema.interfaces.IChoice,
    zope.interface.Interface,
    interfaces.IFormLayer,
)
@zope.interface.implementer(interfaces.IFieldWidget)
def ListingTextFieldWidget(field, request=None):
    """IFieldWidget factory for TextWidget."""
    return FieldWidget(field, ListingTextWidget(request))
