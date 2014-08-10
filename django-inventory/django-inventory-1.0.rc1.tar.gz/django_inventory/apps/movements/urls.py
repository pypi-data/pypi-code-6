from __future__ import absolute_import

from django.conf.urls import patterns, url

from django.utils.translation import ugettext_lazy as _

from generic_views.views import generic_assign_remove

from . import purchase_order_state_filter, purchase_request_state_filter
from .forms import PurchaseOrderForm, PurchaseOrderItemForm, PurchaseRequestForm
from .models import (PurchaseOrder, PurchaseOrderItem, PurchaseOrderItemStatus,
                     PurchaseOrderStatus, PurchaseRequest, PurchaseRequestItem,
                     PurchaseRequestStatus)
from .views import (PurchaseRequestCreateView, PurchaseRequestDeleteView,
                    PurchaseRequestListView, PurchaseRequestUpdateView,
                    PurchaseRequestStateCreateView,
                    PurchaseRequestStateDeleteView,
                    PurchaseRequestStateUpdateView,
                    PurchaseRequestStateListView,
                    PurchaseRequestStateUpdateView,
                    PurchaseRequestItemDeleteView,
                    PurchaseRequestItemUpdateView,
                    PurchaseOrderCreateView, PurchaseOrderDeleteView,
                    PurchaseOrderListView, PurchaseOrderUpdateView,
                    PurchaseOrderItemDeleteView, PurchaseOrderItemUpdateView,
                    PurchaseOrderItemStatusCreateView,
                    PurchaseOrderItemStatusDeleteView,
                    PurchaseOrderItemStatusListView,
                    PurchaseOrderItemStatusUpdateView,
                    PurchaseOrderStatusCreateView,
                    PurchaseOrderStatusDeleteView, PurchaseOrderStatusListView,
                    PurchaseOrderStatusUpdateView)

urlpatterns = patterns('movements.views',
    url(r'^purchase/request/state/list/$', PurchaseRequestStateListView.as_view(), name='purchase_request_state_list'),
    url(r'^purchase/request/state/create/$', PurchaseRequestStateCreateView.as_view(), name='purchase_request_state_create'),
    url(r'^purchase/request/state/(?P<pk>\d+)/update/$', PurchaseRequestStateUpdateView.as_view(), name='purchase_request_state_update'),
    url(r'^purchase/request/state/(?P<pk>\d+)/delete/$', PurchaseRequestStateDeleteView.as_view(), name='purchase_request_state_delete'),

    url(r'^purchase/request/list/$', PurchaseRequestListView.as_view(), name='purchase_request_list'),
    url(r'^purchase/request/(?P<object_id>\d+)/$', 'purchase_request_view', (), 'purchase_request_view'),
    url(r'^purchase/request/create/$', PurchaseRequestCreateView.as_view(), name='purchase_request_create'),
    url(r'^purchase/request/(?P<pk>\d+)/update/$', PurchaseRequestUpdateView.as_view(), name='purchase_request_update'),
    url(r'^purchase/request/(?P<pk>\d+)/delete/$', PurchaseRequestDeleteView.as_view(), name='purchase_request_delete'),
    url(r'^purchase/request/(?P<object_id>\d+)/close/$', 'purchase_request_close', (), 'purchase_request_close'),
    url(r'^purchase/request/(?P<object_id>\d+)/open/$', 'purchase_request_open', (), 'purchase_request_open'),
    url(r'^purchase/request/(?P<object_id>\d+)/purchase_order_wizard/$', 'purchase_order_wizard', (), 'purchase_order_wizard'),

    url(r'^purchase/request/(?P<object_id>\d+)/add_item/$', 'purchase_request_item_create', (), 'purchase_request_item_create'),
    url(r'^purchase/request/item/(?P<pk>\d+)/update/$', PurchaseRequestItemUpdateView.as_view(), name='purchase_request_item_update'),
    url(r'^purchase/request/item/(?P<pk>\d+)/delete/$', PurchaseRequestItemDeleteView.as_view(), name='purchase_request_item_delete'),

    url(r'^purchase/order/status/list/$', PurchaseOrderStatusListView.as_view(), name='purchase_order_state_list'),
    url(r'^purchase/order/status/create/$', PurchaseOrderStatusCreateView.as_view(), name='purchase_order_state_create'),
    url(r'^purchase/order/status/(?P<pk>\d+)/update/$', PurchaseOrderStatusUpdateView.as_view(), name='purchase_order_state_update'),
    url(r'^purchase/order/status/(?P<pk>\d+)/delete/$', PurchaseOrderStatusDeleteView.as_view(), name='purchase_order_state_delete'),

    url(r'^purchase/order/list/$', PurchaseOrderListView.as_view(), name='purchase_order_list'),
    url(r'^purchase/order/(?P<object_id>\d+)/$', 'purchase_order_view', (), 'purchase_order_view'),
    url(r'^purchase/order/create/$', PurchaseOrderCreateView.as_view(), name='purchase_order_create'),
    url(r'^purchase/order/(?P<pk>\d+)/update/$', PurchaseOrderUpdateView.as_view(), name='purchase_order_update'),
    url(r'^purchase/order/(?P<pk>\d+)/delete/$', PurchaseOrderDeleteView.as_view(), name='purchase_order_delete'),
    url(r'^purchase/order/(?P<object_id>\d+)/close/$', 'purchase_order_close', (), 'purchase_order_close'),
    url(r'^purchase/order/(?P<object_id>\d+)/open/$', 'purchase_order_open', (), 'purchase_order_open'),
    url(r'^purchase/order/(?P<object_id>\d+)/add_item/$', 'purchase_order_item_create', (), 'purchase_order_item_create'),
    url(r'^purchase/order/(?P<object_id>\d+)/transfer/$', 'purchase_order_transfer', (), 'purchase_order_transfer'),

    url(r'^purchase/order/item/status/list/$', PurchaseOrderItemStatusListView.as_view(), name='purchase_order_item_state_list'),
    url(r'^purchase/order/item/status/create/$', PurchaseOrderItemStatusCreateView.as_view(), name='purchase_order_item_state_create'),
    url(r'^purchase/order/item/status/(?P<pk>\d+)/update/$', PurchaseOrderItemStatusUpdateView.as_view(), name='purchase_order_item_state_update'),
    url(r'^purchase/order/item/status/(?P<pk>\d+)/delete/$', PurchaseOrderItemStatusDeleteView.as_view(), name='purchase_order_item_state_delete'),

    url(r'^purchase/order/item/(?P<pk>\d+)/update/$', PurchaseOrderItemUpdateView.as_view(), name='purchase_order_item_update'),
    url(r'^purchase/order/item/(?P<pk>\d+)/delete/$', PurchaseOrderItemDeleteView.as_view(), name='purchase_order_item_delete'),
    url(r'^purchase/order/item/(?P<object_id>\d+)/close/$', 'purchase_order_item_close', (), 'purchase_order_item_close'),
    url(r'^purchase/order/item/(?P<object_id>\d+)/transfer/$', 'purchase_order_item_transfer', (), 'purchase_order_item_transfer'),
)
