from __future__ import absolute_import

from django import forms
from django.utils.translation import ugettext_lazy as _

from generic_views.forms import DetailForm

from .models import (Inventory, InventoryTransaction, ItemTemplate, Location,
                     Log, Supplier)


class LocationForm_view(DetailForm):
    class Meta:
        model = Location


class ItemTemplateForm(forms.ModelForm):
    class Meta:
        model = ItemTemplate
        exclude = ('photos', 'supplies', 'suppliers')


class ItemTemplateForm_view(DetailForm):
    class Meta:
        model = ItemTemplate
        exclude = ('photos',)


class LogForm(forms.ModelForm):
    class Meta:
        model = Log


class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory


class InventoryForm_view(DetailForm):
    class Meta:
        model = Inventory


class InventoryTransactionForm(forms.ModelForm):
    class Meta:
        model = InventoryTransaction


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
