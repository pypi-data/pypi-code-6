from __future__ import absolute_import

from django.conf.urls import patterns, url
from django.utils.translation import ugettext_lazy as _

from photos.views import generic_photos

from .conf import settings as inventory_settings
from .forms import (LocationForm_view, LogForm, InventoryForm,
                    InventoryTransactionForm, ItemTemplateForm,
                    ItemTemplateForm_view, SupplierForm)
from .models import (Location, Log, Inventory, ItemTemplate,
                     InventoryTransaction, Supplier)
from .views import (InventoryCreateView, InventoryDeleteView,
                    InventoryDetailView, InventoryListView, InventoryUpdateView,
                    LocationCreateView, LocationDeleteView, LocationDetailView,
                    LocationListView, LocationUpdateView, SupplierCreateView,
                    SupplierDeleteView, SupplierDetailView, SupplierListView,
                    SupplierPurchaseOrdersListView, SupplierUpdateView,
                    TemplateCreateView, TemplateDeleteView,
                    TemplateDetailView, TemplateItemsListView, TemplateListView,
                    TemplateOrphanListView, TemplateUpdateView,
                    TransactionDeleteView, TransactionDetailView,
                    TransactionUpdateView)

urlpatterns = patterns('inventory.views',
    url(r'^template/list/$', TemplateListView.as_view(), name='template_list'),
    url(r'^template/create/$', TemplateCreateView.as_view(), name='template_create'),
    url(r'^template/(?P<pk>\d+)/update/$', TemplateUpdateView.as_view(), name='template_update'),
    url(r'^template/(?P<pk>\d+)/delete/$', TemplateDeleteView.as_view(), name='template_delete'),
    url(r'^template/orphans/$', TemplateOrphanListView.as_view(), name='template_orphans_list'),
    url(r'^template/(?P<object_id>\d+)/photos/$', generic_photos, {'model': ItemTemplate, 'max_photos': inventory_settings.MAX_TEMPLATE_PHOTOS, 'extra_context': {'object_name': _(u'item template')}}, 'template_photos'),
    url(r'^template/(?P<pk>\d+)/$', TemplateDetailView.as_view(), name='template_view'),
    url(r'^template/(?P<pk>\d+)/items/$', TemplateItemsListView.as_view(), name='template_items_list'),
    url(r'^template/(?P<object_id>\d+)/assign/supplies$', 'template_assign_remove_supply', (), name='template_assign_supply'),
    url(r'^template/(?P<object_id>\d+)/assign/suppliers/$', 'template_assign_remove_suppliers', (), name='template_assign_suppliers'),

    url(r'^inventory/list/$', InventoryListView.as_view(), name='inventory_list'),
    url(r'^inventory/create/$', InventoryCreateView.as_view(), name='inventory_create'),
    url(r'^inventory/(?P<pk>\d+)/$', InventoryDetailView.as_view(), name='inventory_view'),
    url(r'^inventory/(?P<pk>\d+)/update/$', InventoryUpdateView.as_view(), name='inventory_update'),
    url(r'^inventory/(?P<pk>\d+)/delete/$', InventoryDeleteView.as_view(), name='inventory_delete'),
    url(r'^inventory/(?P<object_id>\d+)/transaction/create/$', 'inventory_create_transaction', (), 'inventory_create_transaction'),
    url(r'^inventory/(?P<object_id>\d+)/transaction/list/$', 'inventory_list_transactions', (), 'inventory_list_transactions'),

    url(r'^transaction/(?P<pk>\d+)/$', TransactionDetailView.as_view(), name='inventory_transaction_view'),
    url(r'^transaction/(?P<pk>\d+)/update/$', TransactionUpdateView.as_view(), name='inventory_transaction_update'),
    url(r'^transaction/(?P<pk>\d+)/delete/$', TransactionDeleteView.as_view(), name='inventory_transaction_delete'),

    url(r'^location/list/$', LocationListView.as_view(), name='location_list'),
    url(r'^location/create/$', LocationCreateView.as_view(), name='location_create'),
    url(r'^location/(?P<pk>\d+)/update/$', LocationUpdateView.as_view(), name='location_update'),
    url(r'^location/(?P<pk>\d+)/delete/$', LocationDeleteView.as_view(), name='location_delete'),
    url(r'^location/(?P<pk>\d+)/$', LocationDetailView.as_view(), name='location_view'),

    url(r'^supplier/(?P<pk>\d+)/$', SupplierDetailView.as_view(), name='supplier_view'),
    url(r'^supplier/list/$', SupplierListView.as_view(), name='supplier_list'),
    url(r'^supplier/create/$', SupplierCreateView.as_view(), name='supplier_create'),
    url(r'^supplier/(?P<pk>\d+)/update/$', SupplierUpdateView.as_view(), name='supplier_update'),
    url(r'^supplier/(?P<pk>\d+)/delete/$', SupplierDeleteView.as_view(), name='supplier_delete'),
    url(r'^supplier/(?P<object_id>\d+)/assign/itemtemplates/$', 'supplier_assign_remove_itemtemplates', (), 'supplier_assign_itemtemplates'),
    url(r'^supplier/(?P<pk>\d+)/purchase/orders/$', SupplierPurchaseOrdersListView.as_view(), name='supplier_purchase_orders'),
)
