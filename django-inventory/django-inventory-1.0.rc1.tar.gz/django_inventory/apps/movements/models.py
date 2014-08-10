from django.db import models
from django.utils.translation import ugettext_lazy as _

from dynamic_search.api import register
from inventory.models import Supplier, ItemTemplate


class PurchaseRequestStatus(models.Model):
    name = models.CharField(verbose_name=_(u'Name'), max_length=32)

    class Meta:
        verbose_name = _(u'Purchase request status')
        verbose_name_plural = _(u'Purchase request status')

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('purchase_request_state_list', [])


class PurchaseRequest(models.Model):
    user_id = models.CharField(max_length=32, null=True, blank=True, verbose_name=_(u'User defined ID'))
    issue_date = models.DateField(auto_now_add=True, verbose_name=_(u'Issue date'))
    required_date = models.DateField(null=True, blank=True, verbose_name=_(u'Date required'))
    budget = models.PositiveIntegerField(null=True, blank=True, verbose_name=_(u'Budget'))
    active = models.BooleanField(default=True, verbose_name=_(u'Active'))
    status = models.ForeignKey(PurchaseRequestStatus, null=True, blank=True, verbose_name=_(u'Status'))
    originator = models.CharField(max_length=64, null=True, blank=True, verbose_name=_(u'Originator'))
    notes = models.TextField(null=True, blank=True, verbose_name=_(u'Notes'))

    class Meta:
        verbose_name = _(u'Purchase request')
        verbose_name_plural = _(u'Purchase requests')

    def __unicode__(self):
        return '#%s (%s)' % (self.user_id if self.user_id else self.id, self.issue_date)

    @models.permalink
    def get_absolute_url(self):
        return ('purchase_request_view', [str(self.id)])


class PurchaseRequestItem(models.Model):
    purchase_request = models.ForeignKey(PurchaseRequest, related_name='items', verbose_name=_(u'Purchase request'))
    item_template = models.ForeignKey(ItemTemplate, verbose_name=_(u'Item template'))
    qty = models.PositiveIntegerField(verbose_name=_(u'Quantity'))
    notes = models.TextField(null=True, blank=True, verbose_name=_(u'Notes'))

    class Meta:
        verbose_name = _(u'Purchase request item')
        verbose_name_plural = _(u'Purchase request items')

    def __unicode__(self):
        return unicode(self.item_template)

    @models.permalink
    def get_absolute_url(self):
        return ('purchase_request_view', [str(self.purchase_request.id)])


class PurchaseOrderStatus(models.Model):
    name = models.CharField(verbose_name=_(u'Name'), max_length=32)

    class Meta:
        verbose_name = _(u'Purchase order status')
        verbose_name_plural = _(u'Purchase order status')

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('purchase_order_state_list', [])


class PurchaseOrder(models.Model):
    user_id = models.CharField(max_length=32, null=True, blank=True, verbose_name=_(u'User defined ID'))
    purchase_request = models.ForeignKey(PurchaseRequest, null=True, blank=True, verbose_name=_(u'Purchase request'))
    supplier = models.ForeignKey(Supplier, related_name='purchase_orders', verbose_name=_(u'Supplier'))
    issue_date = models.DateField(auto_now_add=True, verbose_name=_(u'Issue date'))
    required_date = models.DateField(null=True, blank=True, verbose_name=_(u'Date required'))
    active = models.BooleanField(default=True, verbose_name=_(u'Active'))
    notes = models.TextField(null=True, blank=True, verbose_name=_(u'Notes'))
    status = models.ForeignKey(PurchaseOrderStatus, null=True, blank=True, verbose_name=_(u'Status'))

    class Meta:
        verbose_name = _(u'Purchase order')
        verbose_name_plural = _(u'Purchase orders')

    def __unicode__(self):
        return '#%s (%s)' % (self.user_id if self.user_id else self.id, self.issue_date)

    @models.permalink
    def get_absolute_url(self):
        return ('purchase_order_view', [str(self.id)])


class PurchaseOrderItemStatus(models.Model):
    name = models.CharField(verbose_name=_(u'Name'), max_length=32)

    class Meta:
        verbose_name = _(u'Purchase order item status')
        verbose_name_plural = _(u'Purchase order item status')

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('purchase_order_item_state_list', [])


class PurchaseOrderItem(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, related_name='items', verbose_name=_(u'Purchase order'))
    item_template = models.ForeignKey(ItemTemplate, verbose_name=_(u'Item template'))
    agreed_price = models.PositiveIntegerField(null=True, blank=True, verbose_name=_(u'Agreed price'))
    active = models.BooleanField(default=True, verbose_name=_(u'Active'))
    status = models.ForeignKey(PurchaseOrderItemStatus, null=True, blank=True, verbose_name=_(u'Status'))
    qty = models.PositiveIntegerField(verbose_name=_(u'Quantity'))
    received_qty = models.PositiveIntegerField(default=0, null=True, blank=True, verbose_name=_(u'received'))

    class Meta:
        verbose_name = _(u'Purchase order item')
        verbose_name_plural = _(u'Purchase order items')

    def __unicode__(self):
        return unicode(self.item_template)

    @models.permalink
    def get_absolute_url(self):
        return ('purchase_order_view', [str(self.purchase_order.id)])


register(PurchaseRequestStatus, _(u'Purchase request status'), ['name'])
register(PurchaseRequest, _(u'Purchase request'), ['user_id', 'id', 'budget', 'required_date', 'status__name', 'originator'])
register(PurchaseRequestItem, _(u'Purchase request item'), ['item_template__description', 'qty', 'notes'])
register(PurchaseOrderStatus, _(u'Purchase order status'), ['name'])
register(PurchaseOrderItemStatus, _(u'Purchase order item status'), ['name'])
register(PurchaseOrder, _(u'Purchase order'), ['user_id', 'id', 'required_date', 'status__name', 'supplier__name', 'notes'])
register(PurchaseOrderItem, _(u'Purchase order item'), ['item_template__description', 'qty'])
