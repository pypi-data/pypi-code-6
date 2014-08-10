import datetime

from django.contrib.auth.models import User, UserManager
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _

from dynamic_search.api import register
from photos.models import GenericPhoto


class Location(models.Model):
    name = models.CharField(max_length=32, verbose_name=_(u'Name'))
    address_line1 = models.CharField(max_length=64, null=True, blank=True, verbose_name=_(u'Address'))
    address_line2 = models.CharField(max_length=64, null=True, blank=True, verbose_name=_(u'Address'))
    address_line3 = models.CharField(max_length=64, null=True, blank=True, verbose_name=_(u'Address'))
    address_line4 = models.CharField(max_length=64, null=True, blank=True, verbose_name=_(u'Address'))
    phone_number1 = models.CharField(max_length=32, null=True, blank=True, verbose_name=_(u'Phone number'))
    phone_number2 = models.CharField(max_length=32, null=True, blank=True, verbose_name=_(u'Phone number'))

    class Meta:
        ordering = ['name']
        verbose_name = _(u'Location')
        verbose_name_plural = _(u'Locations')

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('location_view', [str(self.id)])


class ItemTemplate(models.Model):
    description = models.CharField(verbose_name=_(u'Description'), max_length=64)
    brand = models.CharField(verbose_name=_(u'Brand'), max_length=32, null=True, blank=True)
    model = models.CharField(verbose_name=_(u'Model'), max_length=32, null=True, blank=True)
    part_number = models.CharField(verbose_name=_(u'Part number'), max_length=32, null=True, blank=True)
    notes = models.TextField(verbose_name=_(u'Notes'), null=True, blank=True)
    supplies = models.ManyToManyField('self', null=True, blank=True, verbose_name=_(u'Supplies'))
    suppliers = models.ManyToManyField('Supplier', null=True, blank=True, verbose_name=_(u'Suppliers'))

    class Meta:
        ordering = ['description']
        verbose_name = _(u'Item template')
        verbose_name_plural = _(u'Item templates')

    @models.permalink
    def get_absolute_url(self):
        return ('template_view', [str(self.id)])

    def __unicode__(self):
        return self.description


class Log(models.Model):
    timedate = models.DateTimeField(auto_now_add=True, verbose_name=_(u'Date & time'))
    action = models.CharField(max_length=32, verbose_name=_(u'Action'))
    description = models.TextField(verbose_name=_(u'Description'), null=True, blank=True)

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()

    def __unicode__(self):
        return '%s, %s - %s' % (self.timedate, self.action, self.content_object)

    @models.permalink
    def get_absolute_url(self):
        return ('log_view', [str(self.id)])


class Inventory(models.Model):
    name = models.CharField(max_length=32, verbose_name=_(u'Name'))
    location = models.ForeignKey(Location, verbose_name=_(u'Location'))

    class Meta:
        verbose_name = _(u'Inventory')
        verbose_name_plural = _(u'Inventories')

    @models.permalink
    def get_absolute_url(self):
        return ('inventory_view', [str(self.id)])

    def __unicode__(self):
        return self.name


class InventoryCheckPoint(models.Model):
    inventory = models.ForeignKey(Inventory, verbose_name=_(u'Inventory'))
    datetime = models.DateTimeField(default=datetime.datetime.now(), verbose_name=_(u'Date & time'))
    supplies = models.ManyToManyField(ItemTemplate, null=True, blank=True, through='InventoryCPQty', verbose_name=_(u'Supplies'))


class InventoryCPQty(models.Model):
    supply = models.ForeignKey(ItemTemplate, verbose_name=_(u'Supply'))
    check_point = models.ForeignKey(InventoryCheckPoint, verbose_name=_(u'Check point'))
    quantity = models.IntegerField(verbose_name=_(u'Quantity'))


class InventoryTransaction(models.Model):
    inventory = models.ForeignKey(Inventory, related_name='transactions', verbose_name=_(u'Inventory'))
    supply = models.ForeignKey(ItemTemplate, verbose_name=_(u'Supply'))
    quantity = models.IntegerField(verbose_name=_(u'Quantity'))
    date = models.DateField(default=datetime.date.today(), verbose_name=_(u'Date'))
    notes = models.TextField(null=True, blank=True, verbose_name=_(u'Notes'))

    class Meta:
        verbose_name = _(u'Inventory transaction')
        verbose_name_plural = _(u'Inventory transactions')
        ordering = ['-date', '-id']

    @models.permalink
    def get_absolute_url(self):
        return ('inventory_transaction_view', [str(self.id)])

    def __unicode__(self):
        return "%s: '%s' qty=%s @ %s" % (self.inventory, self.supply, self.quantity, self.date)


class Supplier(models.Model):
    name = models.CharField(max_length=32, verbose_name=_(u'Name'))
    address_line1 = models.CharField(max_length=64, null=True, blank=True, verbose_name=_(u'Address'))
    address_line2 = models.CharField(max_length=64, null=True, blank=True, verbose_name=_(u'Address'))
    address_line3 = models.CharField(max_length=64, null=True, blank=True, verbose_name=_(u'Address'))
    address_line4 = models.CharField(max_length=64, null=True, blank=True, verbose_name=_(u'Address'))
    phone_number1 = models.CharField(max_length=32, null=True, blank=True, verbose_name=_(u'Phone number'))
    phone_number2 = models.CharField(max_length=32, null=True, blank=True, verbose_name=_(u'Phone number'))
    notes = models.TextField(null=True, blank=True, verbose_name=(u'Notes'))

    class Meta:
        ordering = ['name']
        verbose_name = _(u'Supplier')
        verbose_name_plural = _(u'Suppliers')

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('supplier_view', [str(self.id)])


register(ItemTemplate, _(u'Templates'), ['description', 'brand', 'model', 'part_number', 'notes'])
register(Location, _(u'Locations'), ['name', 'address_line1', 'address_line2', 'address_line3', 'address_line4', 'phone_number1', 'phone_number2'])
register(Inventory, _(u'Inventory'), ['name', 'location__name'])
register(Supplier, _(u'Supplier'), ['name', 'address_line1', 'address_line2', 'address_line3', 'address_line4', 'phone_number1', 'phone_number2', 'notes'])
